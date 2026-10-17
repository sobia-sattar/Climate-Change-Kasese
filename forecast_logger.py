"""
forecast_logger.py - Forecast Collection, Archival & Logging Pipeline.

Collects and structures weather forecast data for:
- Kampala, Uganda (ECMWF IFS / Open-Meteo & TAHMO fallback)
- Lahore & Karachi, Pakistan (PMD / ECMWF / GFS)

Records:
- issue_time (UTC timestamp when forecast was emitted)
- valid_time (UTC timestamp when forecast applies)
- lead_h (hours between issue and valid time, enforcing lead_h >= 6)
- city, latitude, longitude
- source (model/provider)
- forecast_rain_mm, rain_probability_pct, temperature_c
- observed_rain_mm (when ground truth / station data becomes available)
"""

import os
import json
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional
import requests

from weather_service import CITY_COORDINATES, get_city_coordinates

LOG_STORAGE_PATH = os.path.join("data", "forecast_logs.json")


def generate_forecast_log_entry(
    city: str,
    source: str,
    issue_time: datetime,
    valid_time: datetime,
    forecast_rain_mm: float,
    rain_probability_pct: int,
    observed_rain_mm: Optional[float] = None,
    is_simulated: bool = False
) -> Dict[str, Any]:
    """Structure a normalized forecast record compliant with the verification pipeline."""
    lead_hours = int(round((valid_time - issue_time).total_seconds() / 3600.0))
    city_info = get_city_coordinates(city)

    return {
        "city": city_info["name"],
        "source": source,
        "issue_time": issue_time.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "valid_time": valid_time.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "lead_h": lead_hours,
        "forecast_mm": round(forecast_rain_mm, 2),
        "rain_probability_pct": rain_probability_pct,
        "observed_mm": round(observed_rain_mm, 2) if observed_rain_mm is not None else None,
        "is_simulated": is_simulated
    }


def fetch_and_log_live_forecast(city_name: str, source: str = "ECMWF IFS (Open-Meteo)") -> List[Dict[str, Any]]:
    """
    Fetch multi-hourly forecasts from Open-Meteo API (national ECMWF IFS & GFS global models)
    and format them into lead-time paired log entries.
    """
    city_info = get_city_coordinates(city_name)
    lat, lon = city_info["lat"], city_info["lon"]

    url = (
        "https://api.open-meteo.com/v1/forecast"
        f"?latitude={lat}&longitude={lon}"
        "&hourly=precipitation,precipitation_probability,temperature_2m"
        "&timezone=UTC&forecast_days=3"
    )

    now = datetime.utcnow().replace(minute=0, second=0, microsecond=0)
    entries: List[Dict[str, Any]] = []

    try:
        resp = requests.get(url, timeout=5)
        if resp.status_code == 200:
            data = resp.json()
            hourly = data.get("hourly", {})
            times = hourly.get("time", [])
            precips = hourly.get("precipitation", [])
            probs = hourly.get("precipitation_probability", [])

            for t_str, prec, prob in zip(times, precips, probs):
                try:
                    v_time = datetime.strptime(t_str, "%Y-%m-%dT%H:%M")
                    lead_h = int((v_time - now).total_seconds() / 3600.0)
                    if lead_h >= 6:  # Minimum 6 hours lead time requirement
                        entry = generate_forecast_log_entry(
                            city=city_name,
                            source=source,
                            issue_time=now,
                            valid_time=v_time,
                            forecast_rain_mm=float(prec or 0.0),
                            rain_probability_pct=int(prob or 0),
                            observed_rain_mm=None,
                            is_simulated=False
                        )
                        entries.append(entry)
                except ValueError:
                    continue
    except Exception as exc:
        print(f"Warning: Live forecast logging failed for {city_name}: {exc}. Using documented fallback.")

    return entries


def load_forecast_logs(filepath: str = LOG_STORAGE_PATH) -> List[Dict[str, Any]]:
    """Load logged forecast records from storage."""
    if not os.path.exists(filepath):
        return []
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data if isinstance(data, list) else []
    except Exception:
        return []


def save_forecast_logs(records: List[Dict[str, Any]], filepath: str = LOG_STORAGE_PATH) -> bool:
    """Save or append forecast records to archival storage."""
    try:
        existing = load_forecast_logs(filepath)
        # Avoid duplicate (city, source, issue_time, valid_time)
        existing_keys = {
            (r.get("city"), r.get("source"), r.get("issue_time"), r.get("valid_time"))
            for r in existing
        }
        for rec in records:
            key = (rec.get("city"), rec.get("source"), rec.get("issue_time"), rec.get("valid_time"))
            if key not in existing_keys:
                existing.append(rec)
                existing_keys.add(key)

        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(existing, f, indent=2, ensure_ascii=False)
        return True
    except Exception as exc:
        print(f"Failed to save forecast logs: {exc}")
        return False
