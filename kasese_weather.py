"""
kasese_weather.py — Kasese, Uganda Weather Data Pipeline.

Fetches:
  1. Live current conditions from Open-Meteo (Kasese coords).
  2. Historical hourly data (up to 90 days) for ML training/evaluation.

Kasese, Uganda: latitude=0.1833, longitude=30.0833
"""

import json
import os
import time
import logging
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional

import requests

logger = logging.getLogger(__name__)

KASESE_LAT = 0.1833
KASESE_LON = 30.0833
CACHE_FILE = os.path.join("data", "kasese_historical.json")
CACHE_TTL_HOURS = 6   # refresh historical cache every 6 hours

WMO_MAP: Dict[int, str] = {
    0: "Clear Sky", 1: "Mainly Clear", 2: "Partly Cloudy", 3: "Overcast",
    45: "Foggy", 48: "Icy Fog", 51: "Light Drizzle", 53: "Drizzle",
    55: "Heavy Drizzle", 61: "Light Rain", 63: "Rain", 65: "Heavy Rain",
    71: "Light Snow", 73: "Snow", 75: "Heavy Snow", 77: "Snow Grains",
    80: "Rain Showers", 81: "Rain Showers", 82: "Violent Showers",
    85: "Snow Showers", 86: "Heavy Snow Showers",
    95: "Thunderstorm", 96: "Thunderstorm w/ Hail", 99: "Thunderstorm w/ Heavy Hail",
}


def _get(url: str, params: Dict, timeout: int = 20) -> Optional[Dict]:
    """HTTP GET with timeout and error handling."""
    try:
        r = requests.get(url, params=params, timeout=timeout)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        logger.warning("Open-Meteo fetch failed: %s", e)
        return None


# ---------------------------------------------------------------------------
# 1. LIVE CURRENT CONDITIONS
# ---------------------------------------------------------------------------
def fetch_kasese_live() -> Dict[str, Any]:
    """Return current conditions for Kasese, Uganda from Open-Meteo."""
    data = _get(
        "https://api.open-meteo.com/v1/forecast",
        {
            "latitude": KASESE_LAT,
            "longitude": KASESE_LON,
            "current": "temperature_2m,relative_humidity_2m,precipitation,weathercode,windspeed_10m,apparent_temperature",
            "hourly": "precipitation_probability",
            "timezone": "Africa/Kampala",
            "forecast_days": 1,
        },
    )
    fallback = {
        "city": "Kasese, Uganda",
        "country": "Uganda",
        "iso": "UG",
        "latitude": KASESE_LAT,
        "longitude": KASESE_LON,
        "temperature_c": 24.0,
        "feels_like_c": 24.0,
        "humidity_pct": 68,
        "precipitation_mm": 0.0,
        "wind_speed_kmh": 6.0,
        "rain_prob_24h": 30,
        "condition": "Clear Sky",
        "icon": "sun",
        "api_source": "Open-Meteo (Kasese Offline Fallback)",
    }
    if not data or "current" not in data:
        return fallback

    cur = data["current"]
    code = int(cur.get("weathercode", 0))
    condition = WMO_MAP.get(code, "Clear Sky")

    # Average first 24h precipitation probability
    prob_list = data.get("hourly", {}).get("precipitation_probability", [])
    rain_prob = int(sum(prob_list[:24]) / max(len(prob_list[:24]), 1)) if prob_list else 25

    return {
        "city": "Kasese, Uganda",
        "country": "Uganda",
        "iso": "UG",
        "latitude": KASESE_LAT,
        "longitude": KASESE_LON,
        "temperature_c": round(float(cur.get("temperature_2m", 24.0)), 1),
        "feels_like_c": round(float(cur.get("apparent_temperature", 24.0)), 1),
        "humidity_pct": int(cur.get("relative_humidity_2m", 68)),
        "precipitation_mm": round(float(cur.get("precipitation", 0.0)), 2),
        "wind_speed_kmh": round(float(cur.get("windspeed_10m", 6.0)), 1),
        "rain_prob_24h": rain_prob,
        "condition": condition,
        "icon": _condition_to_icon(condition),
        "api_source": "Open-Meteo (Kasese, Uganda - Live)",
    }


def _condition_to_icon(condition: str) -> str:
    cl = condition.lower()
    if "thunder" in cl:
        return "cloud-lightning"
    if "rain" in cl or "drizzle" in cl or "shower" in cl:
        return "cloud-rain"
    if "cloud" in cl or "overcast" in cl or "fog" in cl:
        return "cloud"
    if "partly" in cl:
        return "cloud-sun"
    return "sun"


# ---------------------------------------------------------------------------
# 2. HISTORICAL HOURLY DATA (up to 90 days)
# ---------------------------------------------------------------------------
def fetch_kasese_historical(days: int = 90) -> Optional[List[Dict]]:
    """
    Fetch hourly historical weather for Kasese from Open-Meteo archive API.
    Returns list of hourly dicts sorted ascending by timestamp.
    Uses a local cache (CACHE_FILE) to avoid redundant API calls.
    """
    # Try local cache first
    if _cache_valid():
        return _load_cache()

    end = datetime.utcnow().date() - timedelta(days=1)   # yesterday (archive lag)
    start = end - timedelta(days=days - 1)

    data = _get(
        "https://archive-api.open-meteo.com/v1/archive",
        {
            "latitude": KASESE_LAT,
            "longitude": KASESE_LON,
            "start_date": str(start),
            "end_date": str(end),
            "hourly": (
                "precipitation,temperature_2m,relative_humidity_2m,"
                "windspeed_10m,pressure_msl,cloudcover,weathercode"
            ),
            "timezone": "Africa/Kampala",
        },
    )

    if not data or "hourly" not in data:
        logger.warning("Historical fetch failed; returning None.")
        return None

    h = data["hourly"]
    times = h.get("time", [])
    records = []
    for i, t in enumerate(times):
        records.append({
            "timestamp": t,
            "precipitation_mm": float(h.get("precipitation", [0.0] * len(times))[i] or 0.0),
            "temperature_c": float(h.get("temperature_2m", [24.0] * len(times))[i] or 24.0),
            "humidity_pct": float(h.get("relative_humidity_2m", [68.0] * len(times))[i] or 68.0),
            "wind_speed_kmh": float(h.get("windspeed_10m", [5.0] * len(times))[i] or 5.0),
            "pressure_hpa": float(h.get("pressure_msl", [1013.0] * len(times))[i] or 1013.0),
            "cloud_cover_pct": float(h.get("cloudcover", [50.0] * len(times))[i] or 50.0),
            "weather_code": int(h.get("weathercode", [0] * len(times))[i] or 0),
        })

    _save_cache(records)
    return records


# ---------------------------------------------------------------------------
# Cache helpers
# ---------------------------------------------------------------------------
def _cache_valid() -> bool:
    if not os.path.exists(CACHE_FILE):
        return False
    age_hours = (time.time() - os.path.getmtime(CACHE_FILE)) / 3600
    return age_hours < CACHE_TTL_HOURS


def _load_cache() -> Optional[List[Dict]]:
    try:
        with open(CACHE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return None


def _save_cache(records: List[Dict]) -> None:
    os.makedirs(os.path.dirname(CACHE_FILE), exist_ok=True)
    with open(CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump(records, f)
