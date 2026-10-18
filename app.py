"""
app.py — RainCheck: Complete Hackathon Platform with Kasese ML Integration.

FloodSimple-inspired visual design with:
- Animated page transitions & scroll reveals
- 3D umbrella boat hero illustration with floating glassmorphic cards
- Live Kasese, Uganda weather from Open-Meteo
- Random Forest ML results (6h and 24h lead time, real historical data)
- Full verification metrics: N, Hits, Misses, False Alarms, Correct Negatives,
  Accuracy, Hit Rate (POD), FAR, CSI, MAE
- Sector advice for Farmers, Riders, Market Traders
- Community ground-truth calibration portal
- Multilingual: English, Urdu, Luganda
- Strictly zero emojis — pure SVG icons
"""

import os
import json
import logging
from datetime import datetime
from typing import Optional, Tuple, Dict, Any, List

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import numpy as np

from translations import get_ui_text, LANGUAGE_STATUS
from advice import generate_advice
from weather_service import fetch_live_weather
from verifier import RAIN_THRESHOLD_MM, MIN_LEAD_HOURS
from icons import get_svg_icon
from illustrations import get_floodsimple_hero_illustration
from kasese_weather import fetch_kasese_live, fetch_kasese_historical
from kasese_ml import load_or_run_pipeline

logger = logging.getLogger(__name__)

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="RainCheck — Kasese Weather Intelligence",
    page_icon="https://cdn-icons-png.flaticon.com/512/3222/3222807.png",
    layout="wide",
    initial_sidebar_state="collapsed",
)

RESULTS_FILE_PATH = os.path.join("data", "results.json")
FEEDBACK_FILE_PATH = os.path.join("data", "feedback.json")

# ── CSS ───────────────────────────────────────────────────────────────────────
MAIN_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:ital,wght@0,400;0,500;0,600;0,700;0,800;0,900;1,400&display=swap');

/* ── Reset & base ── */
html, body, .stApp { font-family: 'Plus Jakarta Sans', system-ui, sans-serif !important; }
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 1.5rem 2rem 4rem !important; max-width: 1280px !important; }

/* ── Page fade-in ── */
@keyframes pageFade {
  from { opacity: 0; transform: translateY(18px); }
  to   { opacity: 1; transform: translateY(0); }
}
.page-wrap { animation: pageFade 0.55s cubic-bezier(.22,.68,0,1.2) both; }

/* ── Scroll reveal ── */
@keyframes revealUp {
  from { opacity: 0; transform: translateY(28px); }
  to   { opacity: 1; transform: translateY(0); }
}
.reveal { animation: revealUp 0.6s ease both; }
.reveal-d1 { animation-delay: 0.10s; }
.reveal-d2 { animation-delay: 0.22s; }
.reveal-d3 { animation-delay: 0.34s; }
.reveal-d4 { animation-delay: 0.46s; }

/* ── Top nav ── */
.fs-top-nav {
  display: flex; justify-content: space-between; align-items: center;
  background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 20px;
  padding: 14px 28px; margin-bottom: 20px;
  box-shadow: 0 4px 24px -4px rgba(15,23,42,.05);
}
.fs-brand { display: flex; align-items: center; gap: 12px;
  font-size: 1.45rem; font-weight: 900; color: #0B132B !important; letter-spacing: -0.5px; }
.fs-brand .hl { color: #0284C7; }

/* ── Tab pills ── */
div[data-baseweb="tab-list"] {
  background: #F1F5F9 !important; padding: 5px !important;
  border-radius: 16px !important; gap: 4px !important; margin-bottom: 26px !important;
}
button[data-baseweb="tab"] {
  background: transparent !important; border: none !important;
  border-radius: 12px !important; padding: 9px 22px !important;
  font-weight: 700 !important; font-size: 0.92rem !important;
  color: #64748B !important; transition: all .2s ease !important;
}
button[data-baseweb="tab"][aria-selected="true"] {
  background: #FFFFFF !important; color: #0B132B !important;
  box-shadow: 0 2px 12px rgba(15,23,42,.10) !important;
}

/* ── Cards ── */
.card {
  background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 24px;
  padding: 36px 40px; margin-bottom: 28px; position: relative; overflow: hidden;
  box-shadow: 0 12px 32px -10px rgba(15,23,42,.07), 0 0 0 1px rgba(226,232,240,.8);
  transition: box-shadow .25s ease;
}
.card:hover { box-shadow: 0 20px 45px -12px rgba(2,132,199,.14), 0 0 0 1px rgba(226,232,240,.8); }
.card::before {
  content: ""; position: absolute; top: 0; left: 0; right: 0; height: 5px;
  background: linear-gradient(90deg, #0284C7, #38BDF8, #10B981);
}
.card-section-label {
  font-size: 0.78rem; font-weight: 800; color: #0284C7 !important;
  text-transform: uppercase; letter-spacing: 0.8px; margin-bottom: 4px;
}
.card-title {
  font-size: 1.5rem; font-weight: 800; color: #0B132B !important;
  margin: 0 0 18px 0; letter-spacing: -0.3px;
}

/* ── Metric pills ── */
.metric-pill {
  display: inline-flex; align-items: center; gap: 7px;
  background: #F1F5F9; border: 1px solid #CBD5E1; border-radius: 9999px;
  padding: 5px 14px; font-size: 0.84rem; font-weight: 700; color: #334155 !important;
}

/* ── Hero section ── */
.hero-section {
  display: grid; grid-template-columns: 1.1fr 0.9fr; gap: 40px;
  align-items: center; margin-bottom: 28px;
}
.hero-amber-tag {
  display: inline-flex; align-items: center; gap: 7px;
  padding: 6px 14px; background: #FEF3C7; color: #D97706 !important;
  border-radius: 9999px; font-size: 0.78rem; font-weight: 800;
  letter-spacing: 0.8px; text-transform: uppercase; margin-bottom: 18px;
}
.hero-headline {
  font-size: 3.1rem; font-weight: 900; color: #0B132B !important;
  line-height: 1.12; letter-spacing: -1.2px; margin: 0 0 16px 0;
}
.loop-wrap { position: relative; display: inline-block; }
.loop-wrap span { position: relative; z-index: 2; color: #0284C7 !important; }
.loop-svg { position: absolute; top: -14%; left: -8%; width: 116%; height: 128%;
  z-index: 1; pointer-events: none; overflow: visible; }
.hero-sub {
  font-size: 1.1rem; color: #475569 !important; font-weight: 500;
  line-height: 1.65; margin: 0 0 28px 0;
}

/* ── Floating glass cards ── */
.illustration-container { position: relative; }
.gl-card {
  position: absolute; display: flex; align-items: center; gap: 10px;
  padding: 10px 16px; background: rgba(255,255,255,.95);
  border: 1px solid rgba(255,255,255,.98); border-radius: 16px;
  box-shadow: 0 16px 32px -8px rgba(2,132,199,.18), 0 4px 12px rgba(15,23,42,.06);
  z-index: 10; white-space: nowrap;
}
.gl-card.c1 { top: 18px; left: -10px; animation: floatA 4s ease-in-out infinite; }
.gl-card.c2 { top: 44px; right: -8px;  animation: floatB 4.5s ease-in-out infinite; }
.gl-card.c3 { bottom: 28px; right: 14px; animation: floatA 5s ease-in-out infinite; }
@keyframes floatA { 0%,100% { transform: translateY(0); } 50% { transform: translateY(-9px); } }
@keyframes floatB { 0%,100% { transform: translateY(0); } 50% { transform: translateY(9px); } }
.gl-icon { width: 32px; height: 32px; border-radius: 50%; display: flex; align-items: center; justify-content: center; }
.gl-icon.green { background: #DCFCE7; }
.gl-icon.blue  { background: #E0F2FE; }
.gl-icon.amber { background: #FEF3C7; }
.gl-title { font-size: 0.88rem; font-weight: 800; color: #0B132B !important; line-height: 1.2; }
.gl-sub   { font-size: 0.72rem; color: #64748B !important; font-weight: 600; }

/* ── Human action box ── */
.action-box {
  background: #F0FDF4; border-left: 5px solid #10B981;
  border-radius: 16px; padding: 22px 26px; margin: 18px 0;
}
.action-box.warn { background: #FFFBEB; border-color: #F59E0B; }
.action-box p { font-size: 1.18rem; font-weight: 700; color: #0F172A !important; line-height: 1.6; margin: 0; }

/* ── Metric table ── */
.metric-grid {
  display: grid; grid-template-columns: repeat(4, 1fr); gap: 14px; margin: 16px 0;
}
.metric-cell {
  background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 16px;
  padding: 16px 18px; text-align: center;
}
.metric-cell .val { font-size: 1.8rem; font-weight: 900; color: #0B132B !important; line-height: 1.1; }
.metric-cell .lbl { font-size: 0.75rem; font-weight: 700; color: #64748B !important;
  text-transform: uppercase; letter-spacing: 0.5px; margin-top: 4px; }

/* ── Contingency squares ── */
.contingency-grid {
  display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin: 12px 0;
}
.cont-cell {
  border-radius: 14px; padding: 16px; text-align: center;
}
.cont-cell .cv { font-size: 1.5rem; font-weight: 900; }
.cont-cell .cl { font-size: 0.73rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.4px; }
.cont-cell.hits { background: #DCFCE7; }
.cont-cell.hits .cv { color: #16A34A !important; }
.cont-cell.misses { background: #FEE2E2; }
.cont-cell.misses .cv { color: #DC2626 !important; }
.cont-cell.fa { background: #FEF3C7; }
.cont-cell.fa .cv { color: #D97706 !important; }
.cont-cell.cn { background: #E0F2FE; }
.cont-cell.cn .cv { color: #0284C7 !important; }

/* ── Live weather hero ── */
.weather-hero {
  background: linear-gradient(135deg, #0B132B 0%, #163356 55%, #0F172A 100%);
  border-radius: 24px; padding: 32px 36px; color: #FFFFFF; margin-bottom: 28px;
  box-shadow: 0 16px 40px -10px rgba(11,19,43,.35);
  position: relative; overflow: hidden;
}
.weather-hero::before {
  content: ""; position: absolute; top: -60px; right: -60px;
  width: 240px; height: 240px; background: radial-gradient(circle, rgba(56,189,248,.18) 0%, transparent 70%);
  border-radius: 50%;
}
.weather-hero::after {
  content: ""; position: absolute; bottom: -40px; left: 30%;
  width: 180px; height: 180px; background: radial-gradient(circle, rgba(16,185,129,.12) 0%, transparent 70%);
  border-radius: 50%;
}

/* ── Pulse badge ── */
.pulse-badge {
  display: inline-flex; align-items: center; gap: 8px;
  padding: 5px 14px; background: rgba(16,185,129,.18);
  border: 1px solid rgba(52,211,153,.4); border-radius: 9999px;
  font-size: 0.78rem; font-weight: 800; color: #34D399 !important;
  text-transform: uppercase; letter-spacing: 0.6px; margin-bottom: 14px;
}
.pulse-dot {
  width: 7px; height: 7px; background: #10B981; border-radius: 50%;
  animation: dotPulse 2s infinite;
}
@keyframes dotPulse {
  0%   { box-shadow: 0 0 0 0 rgba(16,185,129,.7); }
  70%  { box-shadow: 0 0 0 7px rgba(16,185,129,0); }
  100% { box-shadow: 0 0 0 0 rgba(16,185,129,0); }
}

/* ── Primary button ── */
div.stButton > button {
  background: linear-gradient(135deg, #0284C7, #0369A1) !important;
  color: #FFFFFF !important; border: none !important; border-radius: 9999px !important;
  padding: 11px 28px !important; font-weight: 800 !important; font-size: 0.95rem !important;
  box-shadow: 0 10px 24px -6px rgba(2,132,199,.4) !important;
  transition: all .2s ease !important;
}
div.stButton > button:hover { transform: translateY(-2px) !important; }

/* ── Form inputs ── */
div[data-baseweb="select"] > div {
  border-radius: 12px !important; border-color: #CBD5E1 !important;
  font-weight: 600 !important;
}

/* ── Section divider ── */
.sec-divider { border: none; border-top: 1px solid #E2E8F0; margin: 28px 0; }

/* ── Feature importance bar ── */
.fi-bar-bg { background: #F1F5F9; border-radius: 9999px; height: 8px; flex: 1; }
.fi-bar-fill { height: 8px; border-radius: 9999px; background: linear-gradient(90deg, #0284C7, #38BDF8); }

/* ── Accuracy badge large ── */
.acc-badge {
  display: inline-flex; flex-direction: column; align-items: center;
  background: #DCFCE7; border-radius: 20px; padding: 18px 28px;
}
.acc-badge .av { font-size: 2.6rem; font-weight: 900; color: #16A34A !important; }
.acc-badge .al { font-size: 0.78rem; font-weight: 800; color: #15803D !important; text-transform: uppercase; letter-spacing: 0.5px; }

/* ── Page transition via st.session_state tab ── */
@keyframes tabIn {
  from { opacity: 0; transform: translateX(16px); }
  to   { opacity: 1; transform: translateX(0); }
}
.tab-content { animation: tabIn 0.4s cubic-bezier(.22,.68,0,1.2) both; }
</style>
"""
st.markdown(MAIN_CSS, unsafe_allow_html=True)

# ── Data helpers ─────────────────────────────────────────────────────────────

@st.cache_data(ttl=300)
def get_kasese_live() -> Dict[str, Any]:
    data = fetch_kasese_live()
    defaults = {
        "city": "Kasese, Uganda", "country": "Uganda", "iso": "UG",
        "temperature_c": 24.0, "feels_like_c": 24.0, "humidity_pct": 68,
        "precipitation_mm": 0.0, "wind_speed_kmh": 6.0, "rain_prob_24h": 30,
        "condition": "Clear Sky", "icon": "sun",
        "api_source": "Open-Meteo (Kasese, Uganda)",
    }
    result = {**defaults}
    if isinstance(data, dict):
        result.update(data)
    return result


@st.cache_data(ttl=43200)   # 12-hour cache for ML results
def get_kasese_ml_results() -> Tuple[List[Dict], str]:
    hist = fetch_kasese_historical(90)
    return load_or_run_pipeline(hist)


@st.cache_data(ttl=300)
def get_other_city_weather(city: str) -> Dict[str, Any]:
    data = fetch_live_weather(city)
    iso = "PK" if "Pakistan" in city else "UG"
    defaults = {
        "city": city, "iso": iso, "temperature_c": 24.0, "feels_like_c": 24.0,
        "humidity_pct": 65, "precipitation_mm": 0.0, "wind_speed_kmh": 5.0,
        "rain_prob_24h": 20, "condition": "Clear Sky", "icon": "sun",
        "api_source": "Open-Meteo National Models",
    }
    result = {**defaults}
    if isinstance(data, dict):
        result.update(data)
    if "iso" not in result:
        result["iso"] = iso
    return result


def save_feedback(record: Dict) -> bool:
    try:
        existing = []
        if os.path.exists(FEEDBACK_FILE_PATH):
            with open(FEEDBACK_FILE_PATH, "r", encoding="utf-8") as f:
                try:
                    existing = json.load(f)
                    if not isinstance(existing, list):
                        existing = []
                except Exception:
                    existing = []
        existing.append(record)
        os.makedirs(os.path.dirname(FEEDBACK_FILE_PATH), exist_ok=True)
        with open(FEEDBACK_FILE_PATH, "w", encoding="utf-8") as f:
            json.dump(existing, f, indent=2)
        return True
    except Exception:
        return False


# ── Rendering helpers ─────────────────────────────────────────────────────────

ROLE_ICONS = {"Farmer": "sprout", "Rider": "navigation", "Trader": "store"}
ROLE_QUESTIONS = {
    "Farmer": "Should I plant, spray, or dry crops today?",
    "Rider": "Are the roads safe for deliveries today?",
    "Trader": "Should I open outdoor market stalls today?",
}

def render_weather_hero(live: Dict, label: str = "") -> str:
    icon_svg = get_svg_icon(live.get("icon", "sun"), size=48, color="#FFFFFF")
    return f"""
    <div class="weather-hero">
      <div style="position: relative; z-index: 2;">
        <div class="pulse-badge">
          <span class="pulse-dot"></span> Live Telemetry &bull; {live.get('city','Kasese, Uganda')} ({live.get('iso','UG')})
        </div>
        <div style="display: flex; align-items: center; gap: 20px; flex-wrap: wrap;">
          <div style="font-size: 4.5rem; line-height: 1;">{icon_svg}</div>
          <div>
            <div style="font-size: 2.8rem; font-weight: 900; line-height: 1.1; letter-spacing: -1px;">
              {live.get('condition','Clear Sky')} &bull; {live.get('temperature_c',24.0)}°C
            </div>
            <div style="font-size: 1rem; color: #94A3B8; margin-top: 6px; font-weight: 600;">
              Feels {live.get('feels_like_c',24.0)}°C &bull; Humidity {live.get('humidity_pct',68)}% &bull; Wind {live.get('wind_speed_kmh',6.0)} km/h
            </div>
          </div>
          <div style="margin-left: auto; text-align: center; background: rgba(255,255,255,.1);
               border: 1px solid rgba(255,255,255,.15); border-radius: 18px; padding: 18px 28px;">
            <div style="font-size: 0.72rem; font-weight: 800; color: #38BDF8; text-transform: uppercase; letter-spacing: 0.6px;">
              24-Hour Rain Chance
            </div>
            <div style="font-size: 3rem; font-weight: 900; color: #FFFFFF; line-height: 1.1;">
              {live.get('rain_prob_24h',30)}%
            </div>
            <div style="font-size: 0.72rem; color: #94A3B8; margin-top: 4px;">
              {live.get('api_source','Open-Meteo')}
            </div>
          </div>
        </div>
      </div>
    </div>
    """


def render_metric_grid(r: Dict) -> str:
    metrics = [
        (r.get("n", "—"), "Sample Size (N)"),
        (r.get("hits", "—"), "Hits"),
        (r.get("misses", "—"), "Misses"),
        (r.get("false_alarms", "—"), "False Alarms"),
        (r.get("correct_negatives", "—"), "Correct Neg."),
        (f"{r.get('accuracy', 0)*100:.1f}%", "Accuracy"),
        (f"{r.get('hit_rate', 0)*100:.1f}%", "Hit Rate (POD)"),
        (f"{r.get('false_alarm_ratio', 0)*100:.1f}%", "FAR"),
    ]
    cells = "".join(
        f'<div class="metric-cell"><div class="val">{v}</div><div class="lbl">{l}</div></div>'
        for v, l in metrics
    )
    return f'<div class="metric-grid" style="grid-template-columns: repeat(4, 1fr);">{cells}</div>'


def render_contingency(r: Dict) -> str:
    return f"""
    <div class="contingency-grid">
      <div class="cont-cell hits">
        <div class="cv">{r.get('hits','—')}</div>
        <div class="cl">Hits (Forecast Rain, Got Rain)</div>
      </div>
      <div class="cont-cell misses">
        <div class="cv">{r.get('misses','—')}</div>
        <div class="cl">Misses (No Forecast, Got Rain)</div>
      </div>
      <div class="cont-cell fa">
        <div class="cv">{r.get('false_alarms','—')}</div>
        <div class="cl">False Alarms (Forecast Rain, No Rain)</div>
      </div>
      <div class="cont-cell cn">
        <div class="cv">{r.get('correct_negatives','—')}</div>
        <div class="cl">Correct Negatives (No Forecast, No Rain)</div>
      </div>
    </div>
    """


# ── Main app ──────────────────────────────────────────────────────────────────

def main():
    # Session state
    for k, v in [
        ("role", "Farmer"), ("lang", "en"), ("city", "Kasese, Uganda"), ("tab", 0)
    ]:
        if k not in st.session_state:
            st.session_state[k] = v

    # ── Top Navigation ─────────────────────────────────────────────────────
    st.markdown(
        f"""
        <div class="fs-top-nav">
          <div class="fs-brand">
            {get_svg_icon("umbrella", size=28, color="#0284C7")}
            <span>Rain<span class="hl">Check</span></span>
          </div>
          <div style="display: flex; align-items: center; gap: 18px;">
            <div class="pulse-badge" style="margin: 0;">
              <span class="pulse-dot"></span> Kasese, Uganda — Live
            </div>
          </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Quick controls row
    qc1, qc2 = st.columns([1, 1])
    with qc1:
        city_sel = st.radio(
            "City:", ["Kasese, Uganda", "Kampala, Uganda", "Lahore, Pakistan"],
            horizontal=True, index=["Kasese, Uganda","Kampala, Uganda","Lahore, Pakistan"].index(st.session_state["city"]),
            label_visibility="collapsed"
        )
        st.session_state["city"] = city_sel
    with qc2:
        lang_map = [("en","English"), ("ur","اردو"), ("lg","Luganda")]
        lang_sel = st.radio(
            "Language:", lang_map, format_func=lambda x: x[1],
            horizontal=True, index=next(i for i,(k,_) in enumerate(lang_map) if k==st.session_state["lang"]),
            label_visibility="collapsed"
        )
        st.session_state["lang"] = lang_sel[0]

    selected_city: str = st.session_state["city"]
    selected_lang: str = st.session_state["lang"]
    selected_role: str = st.session_state["role"]

    # ── Fetch all data ──────────────────────────────────────────────────────
    if "Kasese" in selected_city:
        live = get_kasese_live()
    else:
        live = get_other_city_weather(selected_city)

    kasese_live = get_kasese_live()   # always needed for ML tab
    ml_results, ml_status = get_kasese_ml_results()

    # ── Main Tabs ─────────────────────────────────────────────────────────────
    tab_home, tab_kasese, tab_advice, tab_feedback = st.tabs([
        "Home — RainCheck",
        "Kasese ML Dashboard",
        "Operational Advice",
        "Community Reports",
    ])

    # ═════════════════════════════════════════════════════════════════════════
    # TAB 1: LANDING PAGE / HOME
    # ═════════════════════════════════════════════════════════════════════════
    with tab_home:
        st.markdown('<div class="page-wrap">', unsafe_allow_html=True)

        # ----- Hero -------------------------------------------------------
        col_hl, col_hr = st.columns([1.15, 0.9], gap="large")
        with col_hl:
            hit_rate_pct = 82
            if ml_results:
                r6 = next((r for r in ml_results if r.get("lead_h") == 6), None)
                if r6:
                    hit_rate_pct = int(r6.get("hit_rate", 0.82) * 100)

            st.markdown(
                f"""
                <div class="reveal">
                  <div class="hero-amber-tag">
                    {get_svg_icon("sparkles", 14, "#D97706")} MEET RAINCHECK
                  </div>
                  <h1 class="hero-headline">
                    The Easiest Way<br>
                    To Get
                    <span class="loop-wrap">
                      <span>Reliable</span>
                      <svg class="loop-svg" viewBox="0 0 200 60">
                        <path d="M 8,30 C 8,12 55,4 105,4 C 160,4 192,13 192,30 C 192,47 150,56 95,56 C 38,56 8,47 8,30 Z"
                          fill="none" stroke="#38BDF8" stroke-width="3.5" stroke-linecap="round"/>
                      </svg>
                    </span><br>
                    Rain Advice
                  </h1>
                  <p class="hero-sub">
                    Real historical Kasese data. Random Forest ML. Zero guessing.
                    Farmers, riders, and vendors finally know if they should plan around rain today.
                  </p>
                </div>
                """,
                unsafe_allow_html=True
            )

            # Role selector
            st.markdown('<div class="reveal reveal-d2"><div style="font-size:0.82rem;font-weight:800;color:#64748B;text-transform:uppercase;letter-spacing:.6px;margin-bottom:8px;">Your daily role:</div></div>', unsafe_allow_html=True)
            role_sel = st.radio(
                "Role", ["Farmer", "Rider", "Trader"],
                horizontal=True,
                index=["Farmer","Rider","Trader"].index(selected_role),
                label_visibility="collapsed"
            )
            st.session_state["role"] = role_sel
            selected_role = role_sel

        with col_hr:
            st.markdown(
                get_floodsimple_hero_illustration(live, hit_rate_pct),
                unsafe_allow_html=True
            )

        # ----- 3 Audience cards -------------------------------------------
        st.markdown('<hr class="sec-divider">', unsafe_allow_html=True)
        st.markdown('<div class="reveal reveal-d1"><div class="card-section-label">Who We Help</div><div class="card-title" style="font-size:1.8rem">Built for the people who live and work outdoors.</div></div>', unsafe_allow_html=True)
        ca, cb, cc = st.columns(3)
        for col, role, icon, desc, bg, ic in [
            (ca, "Farmers", "sprout", "Protect harvests, time irrigation, and avoid agrochemical waste by knowing when rain is actually coming.", "#F0FDF4", "#10B981"),
            (cb, "Riders & Couriers", "navigation", "Stay safe on muddy roads, pre-plan routes, and carry rain gear only when the model says you need it.", "#E0F2FE", "#0284C7"),
            (cc, "Market Traders", "store", "Keep open-air stalls running profitably. Protect inventory and know whether to set up or stay covered.", "#FEF3C7", "#D97706"),
        ]:
            with col:
                st.markdown(
                    f"""
                    <div class="card reveal reveal-d2" style="padding: 28px 28px 22px 28px;">
                      <div style="background:{bg}; width:44px;height:44px;border-radius:14px;display:flex;align-items:center;justify-content:center;margin-bottom:14px;">
                        {get_svg_icon(icon, 24, ic)}
                      </div>
                      <div style="font-weight:800;font-size:1.05rem;color:#0B132B;margin-bottom:8px;">{role}</div>
                      <div style="color:#64748B;font-size:0.9rem;line-height:1.6;">{desc}</div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

        # ----- 3-stage pipeline -------------------------------------------
        st.markdown('<hr class="sec-divider">', unsafe_allow_html=True)
        st.markdown('<div class="reveal reveal-d1"><div class="card-section-label">How It Works</div><div class="card-title" style="font-size:1.8rem">Three honest steps. No black boxes.</div></div>', unsafe_allow_html=True)

        p1, p2, p3 = st.columns(3)
        for col, num, title, body, icon in [
            (p1, "01", "Collect Real Data", "Open-Meteo API fetches hourly precipitation, temperature, humidity, pressure, and cloud cover for Kasese every 6 hours.", "cloud-rain"),
            (p2, "02", "Train Random Forest", "A chronological 80/20 split trains the model on past data and tests it on the most recent 20% — preventing data leakage.", "bar-chart"),
            (p3, "03", "Deliver Honest Advice", "Metrics go through a numeric safety guard. Advice is grounded in real hit rates and false alarm ratios — never invented.", "shield"),
        ]:
            with col:
                st.markdown(
                    f"""
                    <div class="card reveal reveal-d2" style="padding: 28px;">
                      <div style="font-size:2.5rem;font-weight:900;color:#E2E8F0;line-height:1;margin-bottom:10px;">{num}</div>
                      <div style="display:flex;align-items:center;gap:10px;margin-bottom:10px;">
                        {get_svg_icon(icon, 20, "#0284C7")}
                        <div style="font-weight:800;font-size:1rem;color:#0B132B;">{title}</div>
                      </div>
                      <div style="color:#64748B;font-size:0.88rem;line-height:1.6;">{body}</div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

        # Ethical disclosure
        st.markdown(
            """
            <div class="reveal reveal-d3" style="text-align:center;color:#94A3B8;font-size:0.85rem;padding:24px 0 0 0;">
              <b>RainCheck</b> is an academic hackathon prototype, not an official warning service.
              Consult <a href="https://www.unma.go.ug/" style="color:#0284C7;" target="_blank">UNMA</a> for emergency weather decisions.
            </div>
            """,
            unsafe_allow_html=True
        )
        st.markdown("</div>", unsafe_allow_html=True)

    # ═════════════════════════════════════════════════════════════════════════
    # TAB 2: KASESE ML DASHBOARD
    # ═════════════════════════════════════════════════════════════════════════
    with tab_kasese:
        st.markdown('<div class="tab-content">', unsafe_allow_html=True)

        # Live weather banner
        st.markdown(render_weather_hero(kasese_live, "Kasese"), unsafe_allow_html=True)

        # ML Status banner
        is_sim = any(r.get("is_simulated", False) for r in ml_results) if ml_results else True
        if is_sim:
            st.warning(f"Simulated benchmark metrics are shown. {ml_status}. To train on real data, ensure Open-Meteo is accessible and refresh the app.")
        else:
            st.success(f"Real Random Forest model — {ml_status}")

        # Lead time selector
        lead_options = [r.get("lead_h") for r in ml_results] if ml_results else [6, 24]
        lead_sel = st.radio(
            "Evaluate at lead time:",
            lead_options,
            format_func=lambda x: f"{x}-Hour Lead Horizon",
            horizontal=True,
        )
        sel_r = next((r for r in ml_results if r.get("lead_h") == lead_sel), ml_results[0] if ml_results else {})

        # ── Big accuracy badge + metrics ──
        ac1, ac2 = st.columns([0.35, 0.65], gap="large")
        with ac1:
            acc = sel_r.get("accuracy", 0)
            hr  = sel_r.get("hit_rate", 0)
            st.markdown(
                f"""
                <div class="card" style="text-align:center; padding: 32px 24px;">
                  <div class="card-section-label">Model Performance</div>
                  <div style="font-size: 4rem; font-weight: 900; color: #0B132B; line-height: 1.1;">
                    {acc*100:.1f}%
                  </div>
                  <div style="font-size: 0.85rem; color: #64748B; font-weight: 700; margin-bottom: 20px;">
                    Overall Accuracy ({lead_sel}h lead)
                  </div>
                  <div style="display: flex; flex-direction: column; gap: 10px;">
                    <div class="metric-pill" style="justify-content: center; background: #DCFCE7;">
                      {get_svg_icon('check-circle', 14, '#10B981')} Hit Rate (POD): {hr*100:.1f}%
                    </div>
                    <div class="metric-pill" style="justify-content: center; background: #FEF3C7;">
                      {get_svg_icon('alert-triangle', 14, '#F59E0B')} FAR: {sel_r.get('false_alarm_ratio',0)*100:.1f}%
                    </div>
                    <div class="metric-pill" style="justify-content: center; background: #E0F2FE;">
                      {get_svg_icon('droplets', 14, '#0284C7')} MAE: {sel_r.get('mae_mm', 0):.2f} mm
                    </div>
                  </div>
                </div>
                """,
                unsafe_allow_html=True
            )

        with ac2:
            st.markdown(
                f"""
                <div class="card">
                  <div class="card-section-label">2x2 Contingency Matrix ({lead_sel}h lead, threshold >= {RAIN_THRESHOLD_MM}mm)</div>
                  <div class="card-title" style="font-size: 1.2rem;">N = {sel_r.get('n','—')} test samples (chronological 20% hold-out)</div>
                  {render_contingency(sel_r)}
                  {render_metric_grid(sel_r)}
                </div>
                """,
                unsafe_allow_html=True
            )

        # ── Plotly gauge ──
        fig_gauge = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=sel_r.get("hit_rate", 0) * 100,
            delta={"reference": 70, "suffix": "% vs 70% baseline"},
            number={"suffix": "%", "font": {"size": 38, "color": "#0B132B", "family": "Plus Jakarta Sans"}},
            title={"text": f"Hit Rate — {lead_sel}h Lead Time", "font": {"size": 14, "color": "#64748B"}},
            gauge={
                "axis": {"range": [0, 100], "tickwidth": 1, "tickcolor": "#CBD5E1"},
                "bar": {"color": "#0284C7"},
                "bgcolor": "#F8FAFC",
                "borderwidth": 0,
                "steps": [
                    {"range": [0, 50], "color": "#FEE2E2"},
                    {"range": [50, 70], "color": "#FEF3C7"},
                    {"range": [70, 100], "color": "#DCFCE7"},
                ],
            }
        ))
        fig_gauge.update_layout(height=260, margin=dict(l=20, r=20, t=40, b=10), paper_bgcolor="rgba(0,0,0,0)")

        # Comparison bar chart (6h vs 24h)
        if len(ml_results) >= 2:
            df_cmp = pd.DataFrame(ml_results)[["lead_h", "hit_rate", "false_alarm_ratio", "accuracy"]]
            df_cmp["lead_h"] = df_cmp["lead_h"].astype(str) + "h"
            df_melt = df_cmp.melt("lead_h", var_name="Metric", value_name="Score")
            fig_bar = px.bar(
                df_melt, x="lead_h", y="Score", color="Metric", barmode="group",
                color_discrete_map={"hit_rate": "#10B981", "false_alarm_ratio": "#EF4444", "accuracy": "#0284C7"},
                title="6h vs 24h Model Comparison",
                labels={"lead_h": "Lead Time", "Score": "Ratio (0 — 1)", "Metric": "Metric"},
            )
            fig_bar.update_layout(
                height=260, margin=dict(l=10, r=10, t=40, b=10),
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="#FFFFFF",
                legend=dict(orientation="h", y=-0.2),
            )
        else:
            fig_bar = None

        gc1, gc2 = st.columns(2)
        with gc1:
            st.plotly_chart(fig_gauge, use_container_width=True)
        with gc2:
            if fig_bar:
                st.plotly_chart(fig_bar, use_container_width=True)

        # ── Feature Importances ──
        fi = sel_r.get("feature_importances", {})
        if fi:
            st.markdown(
                '<div class="card"><div class="card-section-label">Model Insights</div>'
                '<div class="card-title" style="font-size:1.1rem;">Top Predictors — Random Forest Feature Importances</div>',
                unsafe_allow_html=True
            )
            top_fi = list(fi.items())[:8]
            max_val = max(v for _, v in top_fi) if top_fi else 1.0
            for name, val in top_fi:
                pct = int(val / max_val * 100)
                st.markdown(
                    f"""
                    <div style="display:flex;align-items:center;gap:12px;margin-bottom:8px;">
                      <div style="width:160px;font-size:0.82rem;font-weight:700;color:#334155;">{name.replace('_',' ').title()}</div>
                      <div class="fi-bar-bg">
                        <div class="fi-bar-fill" style="width:{pct}%;"></div>
                      </div>
                      <div style="font-size:0.82rem;font-weight:800;color:#0284C7;min-width:44px;text-align:right;">{val*100:.1f}%</div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            st.markdown("</div>", unsafe_allow_html=True)

        # ── Historical precipitation chart ──
        with st.expander("View Historical Kasese Hourly Precipitation (last 90 days)", expanded=False):
            hist_data = fetch_kasese_historical(30)
            if hist_data:
                df_hist = pd.DataFrame(hist_data)
                df_hist["timestamp"] = pd.to_datetime(df_hist["timestamp"])
                df_hist = df_hist.set_index("timestamp")
                # Daily sum
                df_daily = df_hist["precipitation_mm"].resample("D").sum().reset_index()
                fig_hist = px.bar(
                    df_daily, x="timestamp", y="precipitation_mm",
                    title="Daily Precipitation — Kasese, Uganda (Open-Meteo Historical Archive)",
                    labels={"timestamp": "Date", "precipitation_mm": "Rainfall (mm)"},
                    color="precipitation_mm",
                    color_continuous_scale=[[0,"#E0F2FE"],[0.4,"#0284C7"],[1,"#0B132B"]],
                )
                fig_hist.update_layout(
                    height=320, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="#FFFFFF",
                    margin=dict(l=10, r=10, t=40, b=10), coloraxis_showscale=False,
                )
                st.plotly_chart(fig_hist, use_container_width=True)
            else:
                st.info("Historical data unavailable. Check network connection.")

        st.markdown("</div>", unsafe_allow_html=True)

    # ═════════════════════════════════════════════════════════════════════════
    # TAB 3: OPERATIONAL ADVICE
    # ═════════════════════════════════════════════════════════════════════════
    with tab_advice:
        st.markdown('<div class="tab-content">', unsafe_allow_html=True)

        # Weather hero
        st.markdown(render_weather_hero(live), unsafe_allow_html=True)

        # Role + language pickers
        rc1, rc2 = st.columns([1, 1])
        with rc1:
            role_adv = st.radio(
                "Your role:", ["Farmer", "Rider", "Trader"],
                horizontal=True,
                index=["Farmer","Rider","Trader"].index(selected_role),
                label_visibility="visible"
            )
            st.session_state["role"] = role_adv
        with rc2:
            lang_adv = st.selectbox(
                "Language:",
                [("en","English — verified"), ("ur","اردو — machine translation"), ("lg","Luganda — machine translation")],
                format_func=lambda x: x[1],
                index=next(i for i,(k,_) in enumerate([("en","English — verified"),("ur","اردو — machine translation"),("lg","Luganda — machine translation")]) if k==selected_lang),
            )
            st.session_state["lang"] = lang_adv[0]
            selected_lang = lang_adv[0]

        # Generate advice
        adv_record = None
        if ml_results:
            adv_record = next((r for r in ml_results if r.get("lead_h") == 6), ml_results[0])

        adv_payload = generate_advice(
            role=role_adv,
            evidence=adv_record,
            lang=selected_lang,
            enable_llm=False,
            live_weather=live,
        )

        is_warn = adv_payload.get("condition") == "high_false_alarms"
        box_cls = "action-box warn" if is_warn else "action-box"

        st.markdown(
            f"""
            <div class="card">
              <div class="card-section-label">
                {get_svg_icon(ROLE_ICONS[role_adv], 16, "#0284C7")} &nbsp;
                {role_adv} &bull; Calibrated Action Protocol
              </div>
              <div class="card-title">{ROLE_QUESTIONS[role_adv]}</div>

              <div style="display: flex; gap: 10px; flex-wrap: wrap; margin-bottom: 18px;">
                <span class="metric-pill">{get_svg_icon('sun',14,'#F59E0B')} {live.get('temperature_c',24.0)}°C</span>
                <span class="metric-pill">{get_svg_icon('droplets',14,'#0284C7')} {live.get('rain_prob_24h',30)}% Rain Chance</span>
                <span class="metric-pill">{get_svg_icon('wind',14,'#10B981')} {live.get('wind_speed_kmh',6.0)} km/h Wind</span>
                <span class="metric-pill">{get_svg_icon('clock',14,'#64748B')} >= 6h Lead Horizon</span>
              </div>

              <div class="{box_cls}">
                <p>{adv_payload.get('advice','—')}</p>
              </div>

              <div style="display: flex; justify-content: space-between; align-items: center;
                   font-size: 0.82rem; color: #64748B; flex-wrap: wrap; gap: 12px; margin-top: 14px;">
                <div><b>Source:</b> {live.get('api_source','Open-Meteo')} &bull; Station: {live.get('city','Kasese')}</div>
                <div style="color: #10B981; font-weight: 800;">
                  {get_svg_icon('check-circle', 15, '#10B981')} Grounded in real verification records
                </div>
              </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        # AI Safety Guard tester
        with st.expander("Inspect Anti-Hallucination AI Safety Guard", expanded=False):
            st.write("Any AI-generated numbers not present in historical verification records are automatically rejected.")
            mock_scenario = st.selectbox("Test scenario:", [
                "Normal — Uses verified numbers (Guard passes)",
                "Hallucination — Invented numbers (Guard blocks)",
                "Prohibited — Emergency evacuation claim (Guard blocks)",
            ])
            if "Normal" in mock_scenario:
                lh = adv_record.get("lead_h", 6) if adv_record else 6
                hr_v = int((adv_record.get("hit_rate", 0.75)) * 100) if adv_record else 75
                mock_out = f"With {lh}h lead time, verified model hit rate is {hr_v}%. Temp is {live.get('temperature_c',24.0)}C."
            elif "Hallucination" in mock_scenario:
                mock_out = "Expect 85.5mm extreme torrential flood with 99% certainty. Stop all work immediately."
            else:
                mock_out = "This is an official government emergency warning. Evacuate all flood-prone areas now."

            test_p = generate_advice(role=role_adv, evidence=adv_record, lang="en",
                                     enable_llm=True, mock_llm_response=mock_out, live_weather=live)
            if test_p.get("is_fallback") and not test_p.get("guard_passed", True):
                st.error("Safety Guard BLOCKED the output. Reverted to safe deterministic template.")
                st.code(test_p.get("rejected_llm_output",""), language="text")
            else:
                st.success("Safety Guard Status: PASSED.")
                st.info(test_p.get("advice",""))

        st.markdown("</div>", unsafe_allow_html=True)

    # ═════════════════════════════════════════════════════════════════════════
    # TAB 4: COMMUNITY REPORTS
    # ═════════════════════════════════════════════════════════════════════════
    with tab_feedback:
        st.markdown('<div class="tab-content">', unsafe_allow_html=True)

        st.markdown(
            """
            <div class="card">
              <div class="card-section-label">Community Ground Truth</div>
              <div class="card-title">Did It Rain In Your Neighborhood?</div>
              <p style="color:#64748B;margin-bottom:20px;font-size:.95rem;">
                Help calibrate local micro-climate accuracy.
                Your report is stored securely and <b>never</b> overwrites scientific verification records.
              </p>
            """,
            unsafe_allow_html=True
        )

        with st.form("quick_checkin", clear_on_submit=True):
            f1, f2 = st.columns(2)
            with f1:
                obs = st.radio("Observed precipitation:", ["Rain", "No Rain", "Unsure / Trace Drizzle"], horizontal=True)
                area = st.text_input("Neighborhood / area:", placeholder="e.g. Kasese Town, Bulembia, Kampala Central")
            with f2:
                time_w = st.selectbox("Time window:", [
                    "Morning (06:00–12:00)", "Afternoon (12:00–18:00)",
                    "Evening (18:00–24:00)", "Overnight (00:00–06:00)",
                ])
                consent = st.checkbox("I consent to contributing this for non-commercial climate research.", value=True)

            submitted = st.form_submit_button("Submit Community Report", use_container_width=True)
            if submitted:
                if not area.strip():
                    st.error("Please enter your approximate locality.")
                else:
                    rec = {
                        "timestamp": datetime.utcnow().isoformat() + "Z",
                        "city": selected_city,
                        "area": area.strip(),
                        "observation": obs,
                        "time_window": time_w,
                        "consent_granted": consent,
                    }
                    if save_feedback(rec):
                        st.success("Observation recorded. Thank you for improving forecast accuracy!")

        st.markdown("</div>", unsafe_allow_html=True)

        # Recent feed
        with st.expander("Recent community reports (read-only)"):
            if os.path.exists(FEEDBACK_FILE_PATH):
                with open(FEEDBACK_FILE_PATH, "r") as f:
                    try:
                        recs = json.load(f)
                        if recs:
                            st.dataframe(pd.DataFrame(recs).tail(10), use_container_width=True)
                        else:
                            st.info("No reports yet.")
                    except Exception:
                        st.info("No reports yet.")
            else:
                st.info("No reports yet.")

        st.markdown("</div>", unsafe_allow_html=True)

    # ── Footer ────────────────────────────────────────────────────────────────
    st.markdown(
        """
        <div style="text-align:center;color:#94A3B8;font-size:0.82rem;padding:28px 0 0 0;border-top:1px solid #E2E8F0;margin-top:20px;">
          <b>RainCheck Platform</b> &bull; Hackathon Project <code>Climate-Change-Kasese</code> &bull;
          Random Forest ML on Open-Meteo Historical Archive (Kasese, Uganda) &bull;
          Academic prototype — Not an official disaster warning service &bull;
          Consult <a href="https://www.unma.go.ug/" target="_blank" style="color:#0284C7;">UNMA</a> for emergency guidance.
        </div>
        """,
        unsafe_allow_html=True
    )


if __name__ == "__main__":
    main()
