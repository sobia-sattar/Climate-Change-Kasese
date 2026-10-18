"""
app.py — RainCheck: Evidence-Grounded Weather Advice Platform for Kasese, Uganda.
FloodSimple Insurtech Style (Dribbble 17048555) — Humanized, Animated, Zero-Bleed Architecture.

Key Highlights:
1. Interactive Role Switching: Farmer, Rider, Trader each have dedicated 3D animated illustrations
   and calibrated operational action protocols.
2. Real-time Open-Meteo API integration for Kasese, Uganda (lat 0.1833, lon 30.0833).
3. Trained Random Forest ML pipeline on 2,160 actual historical hours with chronological split.
4. Complete forecast verification metrics: N, Hits, Misses, False Alarms, Correct Negatives,
   Accuracy, Hit Rate (POD), FAR, CSI, MAE.
5. Strict Numeric Anti-Hallucination Safety Guard.
6. Multilingual support: English, Urdu, Luganda.
7. Zero markdown indentation issues, zero raw HTML bleeding, strictly zero emojis.
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

from translations import (
    get_ui_text,
    get_language_status,
    LANGUAGE_STATUS,
    get_role_display_name,
    get_role_question_text,
)
from advice import generate_advice
from weather_service import fetch_live_weather
from verifier import RAIN_THRESHOLD_MM, MIN_LEAD_HOURS
from icons import get_svg_icon
from illustrations import (
    get_floodsimple_hero_illustration,
    get_farmer_illustration,
    get_rider_illustration,
    get_trader_illustration,
    get_role_illustration,
    get_3d_product_cards_html,
)
from kasese_weather import fetch_kasese_live, fetch_kasese_historical
from kasese_ml import load_or_run_pipeline

logger = logging.getLogger(__name__)

# ── Streamlit Page Configuration ─────────────────────────────────────────────
st.set_page_config(
    page_title="RainCheck — Kasese Weather Intelligence",
    page_icon="https://cdn-icons-png.flaticon.com/512/3222/3222807.png",
    layout="wide",
    initial_sidebar_state="collapsed",
)

RESULTS_FILE_PATH = os.path.join("data", "results.json")
FEEDBACK_FILE_PATH = os.path.join("data", "feedback.json")


def html_block(html_str: str) -> str:
    """Strip all leading whitespace from each line so Streamlit CommonMark never parses it as code."""
    return "\n".join(line.strip() for line in html_str.strip().splitlines() if line.strip())


# ── Clean FloodSimple 3D CSS ──────────────────────────────────────────────────
MAIN_CSS = html_block("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800;900&display=swap');

html, body, .stApp {
font-family: 'Plus Jakarta Sans', system-ui, sans-serif !important;
background-color: #F8FAFC !important;
color: #0F172A !important;
}

#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 1.2rem 2rem 4rem !important; max-width: 1260px !important; }

/* Page fade-in */
@keyframes pageFade {
from { opacity: 0; transform: translateY(12px); }
to   { opacity: 1; transform: translateY(0); }
}
.page-wrap { animation: pageFade 0.4s ease both; }

/* Top Navigation */
.fs-top-nav {
display: flex; justify-content: space-between; align-items: center;
background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 20px;
padding: 14px 28px; margin-bottom: 20px;
box-shadow: 0 4px 20px -2px rgba(15,23,42,.04);
}
.fs-brand {
display: flex; align-items: center; gap: 12px;
font-size: 1.45rem; font-weight: 900; color: #0B132B !important; letter-spacing: -0.5px;
}
.fs-brand .hl { color: #0284C7; }

/* Tab styling */
div[data-baseweb="tab-list"] {
background: #F1F5F9 !important; padding: 6px !important;
border-radius: 16px !important; gap: 6px !important; margin-bottom: 24px !important;
}
button[data-baseweb="tab"] {
background: transparent !important; border: none !important;
border-radius: 12px !important; padding: 10px 22px !important;
font-weight: 700 !important; font-size: 0.92rem !important;
color: #64748B !important; transition: all .2s ease !important;
}
button[data-baseweb="tab"][aria-selected="true"] {
background: #FFFFFF !important; color: #0B132B !important;
box-shadow: 0 4px 14px rgba(15,23,42,.08) !important;
}

/* 3D Elevated Cards */
.fs-card {
background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 24px;
padding: 32px 36px; margin-bottom: 24px; position: relative; overflow: hidden;
box-shadow: 0 16px 36px -12px rgba(15,23,42,.06), 0 0 1px 1px rgba(226,232,240,.8);
transition: transform .25s ease, box-shadow .25s ease;
}
.fs-card:hover {
box-shadow: 0 20px 45px -12px rgba(2,132,199,.12), 0 0 1px 1px rgba(226,232,240,.8);
}
.fs-card::before {
content: ""; position: absolute; top: 0; left: 0; right: 0; height: 5px;
background: linear-gradient(90deg, #0284C7, #38BDF8, #10B981);
}

.card-section-label {
font-size: 0.8rem; font-weight: 800; color: #0284C7 !important;
text-transform: uppercase; letter-spacing: 0.7px; margin-bottom: 4px;
}
.card-title {
font-size: 1.45rem; font-weight: 800; color: #0B132B !important;
margin: 0 0 16px 0; letter-spacing: -0.3px;
}

/* Hero Section */
.hero-amber-tag {
display: inline-flex; align-items: center; gap: 7px;
padding: 6px 14px; background: #FEF3C7; color: #D97706 !important;
border-radius: 9999px; font-size: 0.78rem; font-weight: 800;
letter-spacing: 0.8px; text-transform: uppercase; margin-bottom: 16px;
}
.hero-headline {
font-size: 3.1rem; font-weight: 900; color: #0B132B !important;
line-height: 1.15; letter-spacing: -1.2px; margin: 0 0 16px 0;
}
.loop-wrap { position: relative; display: inline-block; }
.loop-wrap span { position: relative; z-index: 2; color: #0284C7 !important; }
.loop-svg {
position: absolute; top: -14%; left: -8%; width: 116%; height: 128%;
z-index: 1; pointer-events: none; overflow: visible;
}
.hero-sub {
font-size: 1.12rem; color: #475569 !important; font-weight: 500;
line-height: 1.65; margin: 0 0 24px 0;
}

/* Metric pills */
.metric-pill {
display: inline-flex; align-items: center; gap: 7px;
background: #F1F5F9; border: 1px solid #CBD5E1; border-radius: 9999px;
padding: 5px 14px; font-size: 0.84rem; font-weight: 700; color: #334155 !important;
}

/* Human Action Box */
.action-box {
background: #F0FDF4; border-left: 5px solid #10B981;
border-radius: 16px; padding: 22px 26px; margin: 18px 0;
}
.action-box.warn { background: #FFFBEB; border-color: #F59E0B; }
.action-box p { font-size: 1.18rem; font-weight: 700; color: #0F172A !important; line-height: 1.6; margin: 0; }

/* 4x2 Metric Grid */
.metric-grid {
display: grid; grid-template-columns: repeat(4, 1fr); gap: 12px; margin: 16px 0;
}
.metric-cell {
background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 14px;
padding: 14px 16px; text-align: center;
}
.metric-cell .val { font-size: 1.7rem; font-weight: 900; color: #0B132B !important; line-height: 1.1; }
.metric-cell .lbl {
font-size: 0.72rem; font-weight: 700; color: #64748B !important;
text-transform: uppercase; letter-spacing: 0.5px; margin-top: 4px;
}

/* 2x2 Contingency Grid */
.contingency-grid {
display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin: 14px 0;
}
.cont-cell { border-radius: 14px; padding: 16px; text-align: center; }
.cont-cell .cv { font-size: 1.6rem; font-weight: 900; }
.cont-cell .cl { font-size: 0.75rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.4px; }
.cont-cell.hits { background: #DCFCE7; }
.cont-cell.hits .cv { color: #16A34A !important; }
.cont-cell.misses { background: #FEE2E2; }
.cont-cell.misses .cv { color: #DC2626 !important; }
.cont-cell.fa { background: #FEF3C7; }
.cont-cell.fa .cv { color: #D97706 !important; }
.cont-cell.cn { background: #E0F2FE; }
.cont-cell.cn .cv { color: #0284C7 !important; }

/* Live Telemetry Hero */
.weather-hero {
background: linear-gradient(135deg, #0B132B 0%, #163356 55%, #0F172A 100%);
border-radius: 24px; padding: 30px 36px; color: #FFFFFF; margin-bottom: 24px;
box-shadow: 0 16px 40px -10px rgba(11,19,43,.35);
}
.pulse-badge {
display: inline-flex; align-items: center; gap: 8px;
padding: 5px 14px; background: rgba(16,185,129,.18);
border: 1px solid rgba(52,211,153,.4); border-radius: 9999px;
font-size: 0.78rem; font-weight: 800; color: #34D399 !important;
text-transform: uppercase; letter-spacing: 0.6px; margin-bottom: 12px;
}
.pulse-dot {
width: 7px; height: 7px; background: #10B981; border-radius: 50%;
box-shadow: 0 0 0 0 rgba(16,185,129,.7);
animation: dotPulse 2s infinite;
}
@keyframes dotPulse {
0%   { box-shadow: 0 0 0 0 rgba(16,185,129,.7); }
70%  { box-shadow: 0 0 0 7px rgba(16,185,129,0); }
100% { box-shadow: 0 0 0 0 rgba(16,185,129,0); }
}

/* Feature importance bar */
.fi-bar-bg { background: #F1F5F9; border-radius: 9999px; height: 8px; flex: 1; }
.fi-bar-fill { height: 8px; border-radius: 9999px; background: linear-gradient(90deg, #0284C7, #38BDF8); }

/* Buttons */
div.stButton > button {
background: linear-gradient(135deg, #0284C7, #0369A1) !important;
color: #FFFFFF !important; border: none !important; border-radius: 9999px !important;
padding: 10px 26px !important; font-weight: 800 !important; font-size: 0.95rem !important;
box-shadow: 0 10px 24px -6px rgba(2,132,199,.4) !important;
}

/* ── Mobile & Tablet Responsiveness ────────────────────────────── */
@media (max-width: 768px) {
.block-container {
padding: 0.6rem 0.8rem 3rem !important;
}
.fs-top-nav {
padding: 10px 14px !important;
flex-direction: column !important;
align-items: flex-start !important;
gap: 8px !important;
border-radius: 16px !important;
}
.fs-brand {
font-size: 1.25rem !important;
}
.pulse-badge {
font-size: 0.72rem !important;
padding: 4px 10px !important;
margin: 0 !important;
}
.hero-headline {
font-size: 1.95rem !important;
line-height: 1.22 !important;
letter-spacing: -0.6px !important;
margin-bottom: 12px !important;
}
.hero-sub {
font-size: 0.94rem !important;
line-height: 1.55 !important;
margin-bottom: 16px !important;
}
div[data-baseweb="tab-list"] {
padding: 4px !important;
gap: 4px !important;
overflow-x: auto !important;
flex-wrap: nowrap !important;
-webkit-overflow-scrolling: touch !important;
}
button[data-baseweb="tab"] {
padding: 8px 12px !important;
font-size: 0.78rem !important;
white-space: nowrap !important;
}
.fs-card {
padding: 20px 16px !important;
border-radius: 18px !important;
margin-bottom: 16px !important;
}
.card-title {
font-size: 1.18rem !important;
margin-bottom: 12px !important;
}
.action-box {
padding: 14px 16px !important;
border-radius: 14px !important;
margin: 14px 0 !important;
}
.action-box p {
font-size: 0.96rem !important;
line-height: 1.55 !important;
}
.metric-pill {
padding: 4px 10px !important;
font-size: 0.76rem !important;
gap: 5px !important;
}
.metric-grid {
grid-template-columns: repeat(2, 1fr) !important;
gap: 8px !important;
}
.metric-cell {
padding: 10px 8px !important;
}
.metric-cell .val {
font-size: 1.35rem !important;
}
.weather-hero {
padding: 20px 16px !important;
border-radius: 18px !important;
}
.weather-hero > div:nth-child(2) {
gap: 12px !important;
}
.gl-badge {
padding: 6px 10px !important;
font-size: 0.72rem !important;
border-radius: 12px !important;
}
.gl-badge.b1 {
top: 6px !important;
left: -4px !important;
}
.gl-badge.b2 {
top: 24px !important;
right: -4px !important;
}
.gl-badge.b3 {
bottom: 10px !important;
right: 4px !important;
}
div[data-testid="stRadio"] > div {
flex-wrap: wrap !important;
gap: 6px !important;
}
div[data-testid="stRadio"] label {
font-size: 0.82rem !important;
padding: 2px 6px !important;
}
}

@media (max-width: 480px) {
.hero-headline {
font-size: 1.68rem !important;
}
.metric-grid {
grid-template-columns: 1fr 1fr !important;
}
.contingency-grid {
grid-template-columns: 1fr 1fr !important;
gap: 6px !important;
}
.cont-cell {
padding: 10px 6px !important;
}
.cont-cell .cv {
font-size: 1.22rem !important;
}
}
</style>
""")
st.markdown(MAIN_CSS, unsafe_allow_html=True)


# ── Data Loaders with Caching ────────────────────────────────────────────────
@st.cache_data(ttl=300)
def get_kasese_live() -> Dict[str, Any]:
    data = fetch_kasese_live()
    defaults = {
        "city": "Kasese, Uganda", "country": "Uganda", "iso": "UG",
        "temperature_c": 28.5, "feels_like_c": 32.0, "humidity_pct": 52,
        "precipitation_mm": 0.0, "wind_speed_kmh": 5.1, "rain_prob_24h": 34,
        "condition": "Overcast", "icon": "cloud",
        "api_source": "Open-Meteo (Kasese, Uganda - Live)",
    }
    result = {**defaults}
    if isinstance(data, dict):
        result.update(data)
    return result


@st.cache_data(ttl=43200)
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


ROLE_ICONS = {"Overview": "umbrella", "Farmer": "sprout", "Rider": "navigation", "Trader": "store"}
ROLE_QUESTIONS = {
    "Overview": "What does today's weather mean across all outdoor sectors in Kasese?",
    "Farmer": "Should I plant, spray agrochemicals, or dry crops today?",
    "Rider": "Are the roads safe for delivery trips today?",
    "Trader": "Should I open outdoor market stalls today?",
}


def render_weather_hero(live: Dict) -> str:
    icon_svg = get_svg_icon(live.get("icon", "sun"), size=44, color="#FFFFFF")
    html = f"""
<div class="weather-hero">
<div class="pulse-badge">
<span class="pulse-dot"></span> Live Telemetry &bull; {live.get('city','Kasese, Uganda')} ({live.get('iso','UG')})
</div>
<div style="display: flex; align-items: center; gap: 20px; flex-wrap: wrap;">
<div style="font-size: 4rem; line-height: 1;">{icon_svg}</div>
<div>
<div style="font-size: 2.6rem; font-weight: 900; line-height: 1.1; letter-spacing: -0.5px;">
{live.get('condition','Overcast')} &bull; {live.get('temperature_c',28.5)}°C
</div>
<div style="font-size: 0.95rem; color: #94A3B8; margin-top: 6px; font-weight: 600;">
Feels {live.get('feels_like_c',32.0)}°C &bull; Humidity {live.get('humidity_pct',52)}% &bull; Wind {live.get('wind_speed_kmh',5.1)} km/h
</div>
</div>
<div style="margin-left: auto; text-align: center; background: rgba(255,255,255,.1);
border: 1px solid rgba(255,255,255,.15); border-radius: 16px; padding: 14px 24px;">
<div style="font-size: 0.72rem; font-weight: 800; color: #38BDF8; text-transform: uppercase; letter-spacing: 0.6px;">
24-Hour Rain Chance
</div>
<div style="font-size: 2.6rem; font-weight: 900; color: #FFFFFF; line-height: 1.1;">
{live.get('rain_prob_24h',34)}%
</div>
<div style="font-size: 0.72rem; color: #94A3B8; margin-top: 4px;">
{live.get('api_source','Open-Meteo')}
</div>
</div>
</div>
</div>
"""
    return html_block(html)


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
    return html_block(f'<div class="metric-grid">{cells}</div>')


def render_contingency(r: Dict) -> str:
    html = f"""
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
    return html_block(html)


# ── Main Application ─────────────────────────────────────────────────────────
def main():
    if "role" not in st.session_state or st.session_state["role"] not in ["Overview", "Farmer", "Rider", "Trader"]:
        st.session_state["role"] = "Overview"
    if "city" not in st.session_state:
        st.session_state["city"] = "Kasese, Uganda"
    if "lang" not in st.session_state:
        st.session_state["lang"] = "en"

    # 1. Top Navbar
    st.markdown(
        html_block(f"""
<div class="fs-top-nav">
<div class="fs-brand">
{get_svg_icon("umbrella", size=28, color="#0284C7")}
<span>Rain<span class="hl">Check</span></span>
</div>
<div style="display: flex; align-items: center; gap: 16px;">
<div class="pulse-badge" style="margin: 0;">
<span class="pulse-dot"></span> Kasese, Uganda &bull; Active Telemetry
</div>
</div>
</div>
"""),
        unsafe_allow_html=True
    )

    # 2. Controls Row
    qc1, qc2 = st.columns([1.2, 0.8])
    with qc1:
        city_sel = st.radio(
            "Pilot City:",
            ["Kasese, Uganda", "Kampala, Uganda", "Lahore, Pakistan"],
            horizontal=True,
            index=["Kasese, Uganda", "Kampala, Uganda", "Lahore, Pakistan"].index(st.session_state["city"]),
            label_visibility="collapsed"
        )
        st.session_state["city"] = city_sel

    with qc2:
        lang_map = [("en", "English"), ("ur", "اردو"), ("lg", "Luganda")]
        lang_sel = st.radio(
            "Language:",
            lang_map,
            format_func=lambda x: x[1],
            horizontal=True,
            index=next(i for i, (k, _) in enumerate(lang_map) if k == st.session_state["lang"]),
            label_visibility="collapsed"
        )
        st.session_state["lang"] = lang_sel[0]

    selected_city: str = st.session_state["city"]
    selected_lang: str = st.session_state["lang"]

    # 3. Data Retrieval
    if "Kasese" in selected_city:
        live = get_kasese_live()
    else:
        live = get_other_city_weather(selected_city)

    kasese_live = get_kasese_live()
    ml_results, ml_status = get_kasese_ml_results()

    # Hit rate for illustration display
    hit_rate_display = 71
    if ml_results:
        r6 = next((r for r in ml_results if r.get("lead_h") == 6), None)
        if r6:
            hit_rate_display = int(r6.get("hit_rate", 0.71) * 100)

    # 4. Main Navigation Tabs
    tab_home, tab_kasese, tab_advice, tab_feedback = st.tabs([
        get_ui_text("tab_advisor", selected_lang),
        get_ui_text("tab_kasese", selected_lang),
        get_ui_text("tab_safety", selected_lang),
        get_ui_text("tab_feedback", selected_lang),
    ])

    # ═════════════════════════════════════════════════════════════════════════
    # TAB 1: OPERATIONAL ADVISOR (Dynamic Role Switching with 3D Illustrations)
    # ═════════════════════════════════════════════════════════════════════════
    with tab_home:
        st.markdown('<div class="page-wrap">', unsafe_allow_html=True)

        lang_meta = get_language_status(selected_lang)
        if not lang_meta.get("is_reviewed", True):
            st.markdown(
                html_block(f"""
<div style="background: #FEF3C7; border: 1px solid #FDE68A; border-left: 4px solid #D97706; padding: 10px 16px; border-radius: 12px; margin-bottom: 20px; display: flex; align-items: center; gap: 10px;">
<div style="flex-shrink: 0;">{get_svg_icon('alert-triangle', 16, '#D97706')}</div>
<div style="font-size: 0.86rem; color: #92400E; font-weight: 600;">
<b>{lang_meta.get('name')} ({lang_meta.get('native')}) &bull; {lang_meta.get('status')}:</b> {lang_meta.get('note')}
</div>
</div>
"""),
                unsafe_allow_html=True
            )

        col_hl, col_hr = st.columns([1.1, 0.9], gap="large")

        with col_hl:
            hero_tag = get_ui_text("hero_tag", selected_lang)
            hero_sub = get_ui_text("hero_sub", selected_lang)
            choose_role_txt = get_ui_text("choose_role_label", selected_lang)

            if selected_lang == "ur":
                headline_inner = """
<h1 class="hero-headline" style="font-size: 2.2rem; line-height: 1.35;">
قابلِ اعتماد بارش کے مشورے<br>
<span class="loop-wrap">
<span>سب سے آسان</span>
<svg class="loop-svg" viewBox="0 0 200 60">
<path d="M 8,30 C 8,12 55,4 105,4 C 160,4 192,13 192,30 C 192,47 150,56 95,56 C 38,56 8,47 8,30 Z"
fill="none" stroke="#38BDF8" stroke-width="3.5" stroke-linecap="round"/>
</svg>
</span> طریقے سے
</h1>
"""
            elif selected_lang == "lg":
                headline_inner = """
<h1 class="hero-headline" style="font-size: 2.2rem; line-height: 1.35;">
Engeri Ennyangu Ey'okufunamu<br>
<span class="loop-wrap">
<span>Amagezi g'Enkuba</span>
<svg class="loop-svg" viewBox="0 0 200 60">
<path d="M 8,30 C 8,12 55,4 105,4 C 160,4 192,13 192,30 C 192,47 150,56 95,56 C 38,56 8,47 8,30 Z"
fill="none" stroke="#38BDF8" stroke-width="3.5" stroke-linecap="round"/>
</svg>
</span> Ag'amazima
</h1>
"""
            else:
                headline_inner = """
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
"""
            st.markdown(
                html_block(f"""
<div>
<div class="hero-amber-tag">
{get_svg_icon("sparkles", 14, "#D97706")}
{hero_tag}
</div>
{headline_inner}
<p class="hero-sub">
{hero_sub}
</p>
</div>
"""),
                unsafe_allow_html=True
            )

            # Role Switcher
            st.markdown(f"<div style='font-size:0.85rem;font-weight:800;color:#64748B;text-transform:uppercase;letter-spacing:.6px;margin-bottom:8px;'>{choose_role_txt}</div>", unsafe_allow_html=True)
            role_options = ["Overview", "Farmer", "Rider", "Trader"]
            current_role = st.session_state.get("role", "Overview")
            if current_role not in role_options:
                current_role = "Overview"
            active_role = st.radio(
                "Select Role:",
                role_options,
                format_func=lambda r: get_role_display_name(r, selected_lang),
                horizontal=True,
                index=role_options.index(current_role),
                label_visibility="collapsed"
            )
            st.session_state["role"] = active_role

        with col_hr:
            if active_role == "Farmer":
                hero_img = get_farmer_illustration(live, hit_rate_display)
            elif active_role == "Rider":
                hero_img = get_rider_illustration(live, hit_rate_display)
            elif active_role == "Trader":
                hero_img = get_trader_illustration(live, hit_rate_display)
            else:
                # "Overview" -> The signature Blue Boat picture!
                hero_img = get_floodsimple_hero_illustration(live, hit_rate_display)
            st.markdown(hero_img, unsafe_allow_html=True)

        # ── Dedicated Role Action Protocol Card ──────────────────────────────
        adv_record = None
        if ml_results:
            adv_record = next((r for r in ml_results if r.get("lead_h") == 6), ml_results[0])

        if active_role == "Overview":
            adv_title = get_ui_text("overview_title", selected_lang)
            adv_question = get_ui_text("overview_question", selected_lang)
            adv_icon = "umbrella"
            adv_text = get_ui_text("overview_advice", selected_lang)
            box_cls = "action-box"
        else:
            role_name_translated = get_role_display_name(active_role, selected_lang)
            proto_suf = get_ui_text("protocol_suffix", selected_lang)
            adv_title = f"{role_name_translated} &bull; {proto_suf}"
            adv_question = get_role_question_text(active_role, selected_lang)
            adv_icon = ROLE_ICONS.get(active_role, "sprout")
            adv_payload = generate_advice(
                role=active_role,
                evidence=adv_record,
                lang=selected_lang,
                enable_llm=False,
                live_weather=live,
            )
            adv_text = adv_payload.get('advice', '—')
            is_warn = adv_payload.get("condition") == "high_false_alarms"
            box_cls = "action-box warn" if is_warn else "action-box"

        grounded_label = get_ui_text("grounded_records", selected_lang)

        st.markdown(
            html_block(f"""
<div class="fs-card" style="margin-top: 24px;">
<div style="display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap; gap: 16px;">
<div>
<div class="card-section-label">
{get_svg_icon(adv_icon, 16, "#0284C7")} &nbsp;
{adv_title}
</div>
<div class="card-title">{adv_question}</div>
</div>
<div style="display: flex; gap: 8px; flex-wrap: wrap;">
<span class="metric-pill">{get_svg_icon('sun', 14, '#F59E0B')} {live.get('temperature_c', 28.5)}°C</span>
<span class="metric-pill">{get_svg_icon('droplets', 14, '#0284C7')} {live.get('rain_prob_24h', 34)}% Rain Chance</span>
<span class="metric-pill">{get_svg_icon('wind', 14, '#10B981')} {live.get('wind_speed_kmh', 5.1)} km/h Wind</span>
<span class="metric-pill">{get_svg_icon('clock', 14, '#64748B')} >= 6h Lead Horizon</span>
</div>
</div>
<div class="{box_cls}">
<p>{adv_text}</p>
</div>
<div style="display: flex; justify-content: space-between; align-items: center; font-size: 0.85rem; color: #64748B; flex-wrap: wrap; gap: 12px; margin-top: 14px;">
<div><b>Calibrated Station:</b> {live.get('city', selected_city)} &bull; <b>Model:</b> Random Forest on Open-Meteo Historical</div>
<div style="color: #10B981; font-weight: 800; display: flex; align-items: center; gap: 6px;">
{get_svg_icon('check-circle', 16, '#10B981')} {grounded_label}
</div>
</div>
</div>
"""),
            unsafe_allow_html=True
        )

        # ── Three Sector Hubs Preview — Animated 3D Product Cards ────────────
        who_title = get_ui_text("who_protect_title", selected_lang)
        who_sub = get_ui_text("who_protect_sub", selected_lang)
        st.markdown(
            f"<div class='card-section-label' style='margin-top: 32px;'>{who_title}</div>"
            f"<div class='card-title' style='font-size:1.8rem'>{who_sub}</div>",
            unsafe_allow_html=True
        )
        st.markdown(
            get_3d_product_cards_html(
                lang=selected_lang,
                active_role=active_role,
                hit_rate_pct=hit_rate_display,
            ),
            unsafe_allow_html=True
        )

        st.markdown('</div>', unsafe_allow_html=True)

    # ═════════════════════════════════════════════════════════════════════════
    # TAB 2: KASESE ML & HISTORICAL VERIFICATION
    # ═════════════════════════════════════════════════════════════════════════
    with tab_kasese:
        st.markdown('<div class="page-wrap">', unsafe_allow_html=True)

        st.markdown(render_weather_hero(kasese_live), unsafe_allow_html=True)

        is_sim = any(r.get("is_simulated", False) for r in ml_results) if ml_results else True
        if is_sim:
            st.warning(f"Simulated benchmark metrics are shown ({ml_status}).")
        else:
            st.success(f"Empirical Random Forest Model — {ml_status}")

        lead_options = [r.get("lead_h") for r in ml_results] if ml_results else [6, 24]
        lead_sel = st.radio(
            "Forecast Lead Horizon:",
            lead_options,
            format_func=lambda x: f"{x}-Hour Lead Time Evaluation",
            horizontal=True,
        )
        sel_r = next((r for r in ml_results if r.get("lead_h") == lead_sel), ml_results[0] if ml_results else {})

        col_m1, col_m2 = st.columns([0.35, 0.65], gap="large")
        with col_m1:
            acc = sel_r.get("accuracy", 0)
            hr = sel_r.get("hit_rate", 0)
            st.markdown(
                html_block(f"""
<div class="fs-card" style="text-align: center; padding: 32px 20px;">
<div class="card-section-label">Model Reliability</div>
<div style="font-size: 4rem; font-weight: 900; color: #0B132B; line-height: 1.1;">
{acc*100:.1f}%
</div>
<div style="font-size: 0.85rem; color: #64748B; font-weight: 700; margin-bottom: 20px;">
Overall Accuracy ({lead_sel}h lead horizon)
</div>
<div style="display: flex; flex-direction: column; gap: 10px;">
<div class="metric-pill" style="justify-content: center; background: #DCFCE7;">
{get_svg_icon('check-circle', 14, '#10B981')} Hit Rate (POD): {hr*100:.1f}%
</div>
<div class="metric-pill" style="justify-content: center; background: #FEF3C7;">
{get_svg_icon('alert-triangle', 14, '#F59E0B')} FAR: {sel_r.get('false_alarm_ratio', 0)*100:.1f}%
</div>
<div class="metric-pill" style="justify-content: center; background: #E0F2FE;">
{get_svg_icon('droplets', 14, '#0284C7')} MAE: {sel_r.get('mae_mm', 0):.2f} mm
</div>
</div>
</div>
"""),
                unsafe_allow_html=True
            )

        with col_m2:
            st.markdown(
                html_block(f"""
<div class="fs-card">
<div class="card-section-label">2x2 Contingency Matrix ({lead_sel}h Lead Time, Event Threshold >= {RAIN_THRESHOLD_MM}mm)</div>
<div class="card-title" style="font-size: 1.18rem;">Evaluation Sample: N = {sel_r.get('n', '—')} chronological hold-out hours</div>
{render_contingency(sel_r)}
{render_metric_grid(sel_r)}
</div>
"""),
                unsafe_allow_html=True
            )

        # Plotly Charts Row
        c_p1, c_p2 = st.columns(2)
        with c_p1:
            fig_gauge = go.Figure(go.Indicator(
                mode="gauge+number",
                value=sel_r.get("hit_rate", 0) * 100,
                number={"suffix": "%", "font": {"size": 40, "color": "#0B132B", "family": "Plus Jakarta Sans"}},
                title={"text": f"Hit Rate (POD) &bull; {lead_sel}h Lead", "font": {"size": 15, "color": "#64748B"}},
                gauge={
                    "axis": {"range": [0, 100], "tickwidth": 1, "tickcolor": "#CBD5E1"},
                    "bar": {"color": "#0284C7"},
                    "bgcolor": "#F8FAFC",
                    "steps": [
                        {"range": [0, 50], "color": "#FEE2E2"},
                        {"range": [50, 70], "color": "#FEF3C7"},
                        {"range": [70, 100], "color": "#DCFCE7"},
                    ],
                }
            ))
            fig_gauge.update_layout(height=260, margin=dict(l=20, r=20, t=40, b=10), paper_bgcolor="rgba(0,0,0,0)")
            st.plotly_chart(fig_gauge, use_container_width=True)

        with c_p2:
            if len(ml_results) >= 2:
                df_cmp = pd.DataFrame(ml_results)[["lead_h", "hit_rate", "false_alarm_ratio", "accuracy"]]
                df_cmp["lead_h"] = df_cmp["lead_h"].astype(str) + "h Lead"
                df_melt = df_cmp.melt("lead_h", var_name="Metric", value_name="Score")
                fig_bar = px.bar(
                    df_melt, x="lead_h", y="Score", color="Metric", barmode="group",
                    color_discrete_map={"hit_rate": "#10B981", "false_alarm_ratio": "#EF4444", "accuracy": "#0284C7"},
                    title="Model Horizon Comparison: 6h vs 24h",
                    labels={"lead_h": "Horizon", "Score": "Metric Value (0 — 1.0)", "Metric": "Evaluation Metric"}
                )
                fig_bar.update_layout(
                    height=260, margin=dict(l=10, r=10, t=40, b=10),
                    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="#FFFFFF"
                )
                st.plotly_chart(fig_bar, use_container_width=True)

        # Feature Importance Insights
        fi = sel_r.get("feature_importances", {})
        if fi:
            st.markdown(
                html_block("""
<div class="fs-card">
<div class="card-section-label">Predictor Analysis</div>
<div class="card-title" style="font-size:1.15rem;">Random Forest Gini Feature Importances (Kasese Station)</div>
"""),
                unsafe_allow_html=True
            )
            top_fi = list(fi.items())[:8]
            max_v = max(v for _, v in top_fi) if top_fi else 1.0
            for fname, fval in top_fi:
                pct = int(fval / max_v * 100)
                st.markdown(
                    html_block(f"""
<div style="display: flex; align-items: center; gap: 12px; margin-bottom: 8px;">
<div style="width: 170px; font-size: 0.82rem; font-weight: 700; color: #334155;">{fname.replace('_', ' ').title()}</div>
<div class="fi-bar-bg">
<div class="fi-bar-fill" style="width: {pct}%;"></div>
</div>
<div style="font-size: 0.82rem; font-weight: 800; color: #0284C7; min-width: 48px; text-align: right;">{fval*100:.1f}%</div>
</div>
"""),
                    unsafe_allow_html=True
                )
            st.markdown("</div>", unsafe_allow_html=True)

        # Historical Precipitation Graph
        with st.expander("Explore Historical Kasese Hourly Precipitation (90 Days)", expanded=False):
            hist_raw = fetch_kasese_historical(30)
            if hist_raw:
                df_h = pd.DataFrame(hist_raw)
                df_h["timestamp"] = pd.to_datetime(df_h["timestamp"])
                df_h = df_h.set_index("timestamp")
                df_d = df_h["precipitation_mm"].resample("D").sum().reset_index()
                fig_h = px.bar(
                    df_d, x="timestamp", y="precipitation_mm",
                    title="Daily Rainfall Volume &bull; Kasese, Uganda (Open-Meteo Archive)",
                    labels={"timestamp": "Date", "precipitation_mm": "Precipitation (mm)"},
                    color="precipitation_mm",
                    color_continuous_scale=[[0, "#E0F2FE"], [0.5, "#0284C7"], [1, "#0B132B"]],
                )
                fig_h.update_layout(height=300, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="#FFFFFF", coloraxis_showscale=False)
                st.plotly_chart(fig_h, use_container_width=True)

        st.markdown('</div>', unsafe_allow_html=True)

    # ═════════════════════════════════════════════════════════════════════════
    # TAB 3: AI SAFETY GUARDRAIL
    # ═════════════════════════════════════════════════════════════════════════
    with tab_advice:
        st.markdown('<div class="page-wrap">', unsafe_allow_html=True)

        st.markdown(
            html_block("""
<div class="fs-card">
<div class="card-section-label">Safe AI Architecture</div>
<div class="card-title">Mathematical Anti-Hallucination Guardrail</div>
<p style="color: #64748B; font-size: 0.95rem; line-height: 1.6;">
Large Language Models frequently hallucinate dangerous numbers (e.g., claiming <i>"99% flood certainty"</i>).
RainCheck deploys a strict regex whitelist filter: if any LLM output introduces unverified statistics,
it is instantly rejected and reverted to the deterministic, human-verified template.
</p>
</div>
"""),
            unsafe_allow_html=True
        )

        test_scenario = st.selectbox(
            "Select Test Scenario to Evaluate Safety Guard:",
            [
                "Scenario 1: Grounded Output (Uses verified numbers — Guard Passes)",
                "Scenario 2: AI Hallucination (Invented 85.5mm flood — Guard Rejects)",
                "Scenario 3: Prohibited Claim (Official evacuation warning — Guard Rejects)"
            ]
        )

        lead_val = adv_record.get("lead_h", 6) if adv_record else 6
        hr_val = int((adv_record.get("hit_rate", 0.71)) * 100) if adv_record else 71

        if "Scenario 1" in test_scenario:
            mock_text = f"With a {lead_val}h lead horizon, model hit rate is {hr_val}%. Current temperature is {live.get('temperature_c', 28.5)}C."
        elif "Scenario 2" in test_scenario:
            mock_text = "Expect 85.5mm extreme flood rainfall with 99% probability. Stop all commercial work immediately."
        else:
            mock_text = "Official National Meteorological Authority warning: Mandatory flood evacuation across Kasese."

        guard_role = st.session_state["role"] if st.session_state.get("role") in ["Farmer", "Rider", "Trader"] else "Farmer"
        test_payload = generate_advice(
            role=guard_role,
            evidence=adv_record,
            lang="en",
            enable_llm=True,
            mock_llm_response=mock_text,
            live_weather=live
        )

        col_g1, col_g2 = st.columns(2)
        with col_g1:
            st.markdown("#### Input Prompt / Mock LLM Response:")
            st.code(mock_text, language="text")

        with col_g2:
            st.markdown("#### Guardrail Inspection Result:")
            if test_payload.get("is_fallback") and not test_payload.get("guard_passed", True):
                st.error("SAFETY GUARD ACTIVATED: Hallucinated output was BLOCKED!")
                st.write("**Grounded Fallback Advice Delivered Instead:**")
                st.info(test_payload.get("advice", ""))
                for note in test_payload.get("guard_notes", []):
                    st.caption(f"- {note}")
            else:
                st.success("SAFETY GUARD PASSED: Output verified against historical records.")
                st.info(test_payload.get("advice", ""))

        st.markdown('</div>', unsafe_allow_html=True)

    # ═════════════════════════════════════════════════════════════════════════
    # TAB 4: COMMUNITY REPORTS
    # ═════════════════════════════════════════════════════════════════════════
    with tab_feedback:
        st.markdown('<div class="page-wrap">', unsafe_allow_html=True)

        fb_title = get_ui_text("feedback_title", selected_lang)
        fb_intro = get_ui_text("feedback_intro", selected_lang)
        fb_obs_label = get_ui_text("feedback_observation", selected_lang)
        fb_rain = get_ui_text("feedback_rain", selected_lang)
        fb_no_rain = get_ui_text("feedback_no_rain", selected_lang)
        fb_unsure = get_ui_text("feedback_unsure", selected_lang)
        fb_area_label = get_ui_text("feedback_area", selected_lang)
        fb_time_label = get_ui_text("feedback_time", selected_lang)
        fb_consent_label = get_ui_text("feedback_consent", selected_lang)
        fb_submit_label = get_ui_text("feedback_submit", selected_lang)
        fb_success_label = get_ui_text("feedback_success", selected_lang)

        st.markdown(
            html_block(f"""
<div class="fs-card">
<div class="card-section-label">Community Ground-Truth Calibration</div>
<div class="card-title">{fb_title}</div>
<p style="color: #64748B; font-size: 0.95rem;">
{fb_intro}
</p>
</div>
"""),
            unsafe_allow_html=True
        )

        with st.form("community_report_form", clear_on_submit=True):
            col_f1, col_f2 = st.columns(2)
            with col_f1:
                obs_choices = [fb_rain, fb_no_rain, fb_unsure]
                obs = st.radio(fb_obs_label, obs_choices, horizontal=True)
                area = st.text_input(fb_area_label, placeholder="e.g. Kasese Town, Bulembia, Nakasero")

            with col_f2:
                time_w = st.selectbox(fb_time_label, [
                    "Morning (06:00 - 12:00)", "Afternoon (12:00 - 18:00)",
                    "Evening (18:00 - 24:00)", "Overnight (00:00 - 06:00)"
                ])
                consent = st.checkbox(fb_consent_label, value=True)

            sub_btn = st.form_submit_button(fb_submit_label, use_container_width=True)
            if sub_btn:
                if not area.strip():
                    st.error("Please specify your local area or neighborhood.")
                else:
                    new_rec = {
                        "timestamp": datetime.utcnow().isoformat() + "Z",
                        "city": selected_city,
                        "area": area.strip(),
                        "observation": obs,
                        "time_window": time_w,
                        "consent_granted": consent
                    }
                    if save_feedback(new_rec):
                        st.success(fb_success_label)

        with st.expander("Recent Community Ground-Truth Feed (Read-Only)"):
            if os.path.exists(FEEDBACK_FILE_PATH):
                try:
                    with open(FEEDBACK_FILE_PATH, "r") as f:
                        records = json.load(f)
                    if records:
                        st.dataframe(pd.DataFrame(records).tail(10), use_container_width=True)
                    else:
                        st.info("No community reports recorded yet.")
                except Exception:
                    st.info("No community reports recorded yet.")

        st.markdown('</div>', unsafe_allow_html=True)

    # ── Universal Footer ──────────────────────────────────────────────────────
    st.markdown(
        html_block("""
<div style="text-align: center; color: #94A3B8; font-size: 0.82rem; padding: 24px 0 0 0; border-top: 1px solid #E2E8F0; margin-top: 24px;">
<b>RainCheck Platform</b> &bull; Hackathon Project <code>Climate-Change-Kasese</code> &bull;
Random Forest ML on Open-Meteo Historical Archive (Kasese, Uganda) &bull;
Academic Decision Support Prototype &bull; Not an official disaster warning agency &bull;
Consult <a href="https://www.unma.go.ug/" target="_blank" style="color: #0284C7; font-weight: 700;">UNMA (Uganda)</a> for emergency alerts.
</div>
"""),
        unsafe_allow_html=True
    )


if __name__ == "__main__":
    main()
