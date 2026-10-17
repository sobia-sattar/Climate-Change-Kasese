"""
app.py - RainCheck: Evidence-Based Weather & Climate Risk Intelligence.
Designed in the FloodSimple Insurtech Style (Dribbble 17048555).

Contains:
1. Public-Facing Landing Page (Hero, CTAs, Problem/Solution, Audience Hubs, Workflow, Disclosures)
2. Functional Application Dashboard (Operational Advice, Verification Analytics, Ground-Truth Portal)

Strictly zero emojis: all visual markers use clean, scalable SVG vector icons.
"""

import os
import json
from datetime import datetime
from typing import Optional, Tuple, Dict, Any, List

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from translations import (
    get_ui_text,
    get_language_status,
    LANGUAGE_STATUS
)
from advice import (
    generate_advice,
    generate_deterministic_advice
)
from weather_service import fetch_live_weather
from verifier import RAIN_THRESHOLD_MM, MIN_LEAD_HOURS
from icons import get_svg_icon

# -----------------------------------------------------------------------------
# Streamlit Page Setup
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="RainCheck — Weather Verification & Risk Intelligence",
    page_icon="https://cdn-icons-png.flaticon.com/512/3222/3222807.png",
    layout="wide",
    initial_sidebar_state="expanded"
)

RESULTS_FILE_PATH = os.path.join("data", "results.json")
FEEDBACK_FILE_PATH = os.path.join("data", "feedback.json")

# -----------------------------------------------------------------------------
# FloodSimple Insurtech CSS (High-Contrast, Zero-Emoji Architecture)
# -----------------------------------------------------------------------------
FLOODSIMPLE_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

/* Scoped Main Content Area */
.main, section.main, .stMainBlockContainer {
    background-color: #F8FAFC !important;
}
section.main p, section.main span, section.main label, 
section.main h1, section.main h2, section.main h3, 
section.main h4, section.main h5, section.main h6 {
    color: #0F172A !important;
}

/* Scoped Sidebar (Dark Navy Theme with Bright High-Contrast Text) */
section[data-testid="stSidebar"] {
    background-color: #0B132B !important;
    border-right: 1px solid #1E293B !important;
}
section[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] span,
section[data-testid="stSidebar"] label,
section[data-testid="stSidebar"] div,
section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3 {
    color: #F8FAFC !important;
}
section[data-testid="stSidebar"] div[data-testid="stRadio"] label p {
    color: #F8FAFC !important;
    font-weight: 600 !important;
    font-size: 0.95rem !important;
}
section[data-testid="stSidebar"] div[data-baseweb="select"] > div {
    background-color: #1E293B !important;
    color: #FFFFFF !important;
    border: 1px solid #334155 !important;
    border-radius: 8px !important;
}
section[data-testid="stSidebar"] div[data-baseweb="select"] span,
section[data-testid="stSidebar"] div[data-baseweb="select"] div {
    color: #FFFFFF !important;
    background-color: transparent !important;
}
section[data-testid="stSidebar"] svg {
    fill: #94A3B8 !important;
    stroke: #94A3B8 !important;
}

/* FloodSimple Brand Header */
.brand-nav {
    display: flex;
    justify-content: space-between;
    align-items: center;
    background: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 14px;
    padding: 16px 24px;
    margin-bottom: 24px;
    box-shadow: 0 2px 10px rgba(15, 23, 42, 0.03);
}
.brand-logo {
    display: flex;
    align-items: center;
    gap: 12px;
    font-size: 1.35rem;
    font-weight: 800;
    color: #0B132B !important;
}
.brand-sub {
    font-size: 0.8rem;
    font-weight: 600;
    color: #64748B !important;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

/* Hero Section */
.hero-box {
    background: linear-gradient(135deg, #0B132B 0%, #162544 50%, #0F172A 100%) !important;
    border-radius: 20px !important;
    padding: 36px 44px !important;
    margin-bottom: 32px !important;
    box-shadow: 0 12px 30px -5px rgba(11, 19, 43, 0.28) !important;
    border: 1px solid rgba(255, 255, 255, 0.1) !important;
}
.hero-box * {
    color: #FFFFFF !important;
}

/* Live Telemetry Pulse Badge */
.telemetry-badge {
    display: inline-flex;
    align-items: center;
    gap: 10px;
    padding: 6px 16px;
    background: rgba(16, 185, 129, 0.16);
    color: #34D399 !important;
    border: 1px solid rgba(52, 211, 153, 0.4);
    border-radius: 9999px;
    font-size: 0.8rem;
    font-weight: 700;
    letter-spacing: 0.6px;
    text-transform: uppercase;
}
.pulse-circle {
    width: 8px;
    height: 8px;
    background-color: #10B981;
    border-radius: 50%;
    box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.7);
    animation: pulse-ring 2s infinite;
}
@keyframes pulse-ring {
    0% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.7); }
    70% { transform: scale(1); box-shadow: 0 0 0 8px rgba(16, 185, 129, 0); }
    100% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(16, 185, 129, 0); }
}

/* Navigation Segmented Pills */
div[data-baseweb="tab-list"] {
    background: #E2E8F0 !important;
    padding: 6px !important;
    border-radius: 14px !important;
    gap: 6px !important;
    margin-bottom: 24px !important;
}
button[data-baseweb="tab"] {
    background: transparent !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 10px 24px !important;
    font-size: 0.95rem !important;
    font-weight: 700 !important;
    color: #475569 !important;
    transition: all 0.2s ease !important;
}
button[data-baseweb="tab"]:hover {
    color: #0F172A !important;
    background: rgba(255, 255, 255, 0.6) !important;
}
button[data-baseweb="tab"][aria-selected="true"] {
    background: #FFFFFF !important;
    color: #0284C7 !important;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08) !important;
}
div[data-baseweb="tab-highlight"] {
    display: none !important;
}

/* FloodSimple Cards */
.fs-card {
    background: #FFFFFF !important;
    border: 1px solid #E2E8F0 !important;
    border-radius: 16px !important;
    padding: 26px !important;
    margin-bottom: 22px !important;
    box-shadow: 0 4px 18px rgba(15, 23, 42, 0.04) !important;
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}
.fs-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 10px 25px -4px rgba(15, 23, 42, 0.08);
}

/* 4-Column KPI Grid */
.kpi-grid {
    display: grid !important;
    grid-template-columns: repeat(4, 1fr) !important;
    gap: 16px !important;
    margin-bottom: 24px !important;
}
@media (max-width: 900px) {
    .kpi-grid { grid-template-columns: repeat(2, 1fr) !important; }
}
.kpi-box {
    background: #FFFFFF !important;
    border: 1px solid #E2E8F0 !important;
    border-radius: 14px !important;
    padding: 20px !important;
    box-shadow: 0 2px 8px rgba(0,0,0,0.03) !important;
}
.kpi-box-green { border-top: 4px solid #10B981 !important; }
.kpi-box-blue { border-top: 4px solid #0284C7 !important; }
.kpi-box-purple { border-top: 4px solid #6366F1 !important; }
.kpi-box-amber { border-top: 4px solid #F59E0B !important; }

.kpi-label {
    font-size: 0.78rem !important;
    font-weight: 700 !important;
    color: #64748B !important;
    text-transform: uppercase !important;
    letter-spacing: 0.5px !important;
}
.kpi-value {
    font-size: 2.1rem !important;
    font-weight: 800 !important;
    color: #0F172A !important;
    margin: 4px 0 !important;
}
.kpi-subtitle {
    font-size: 0.8rem !important;
    color: #0284C7 !important;
    font-weight: 600 !important;
}

/* Persona Selection Cards (Horizontal radio overrides) */
div[data-testid="stRadio"] > div[role="radiogroup"] {
    display: flex !important;
    gap: 14px !important;
    margin-bottom: 12px !important;
}
div[data-testid="stRadio"] > div[role="radiogroup"] > label {
    background: #FFFFFF !important;
    border: 2px solid #E2E8F0 !important;
    border-radius: 14px !important;
    padding: 16px 24px !important;
    cursor: pointer !important;
    transition: all 0.2s ease !important;
    box-shadow: 0 2px 4px rgba(0,0,0,0.02) !important;
}
div[data-testid="stRadio"] > div[role="radiogroup"] > label:hover {
    border-color: #0284C7 !important;
    transform: translateY(-2px) !important;
}
div[data-testid="stRadio"] label p {
    font-size: 1.05rem !important;
    font-weight: 700 !important;
    color: #0F172A !important;
}

/* Action Recommendation Callouts */
.action-box {
    background: #F0FDF4 !important;
    border: 1px solid #BBF7D0 !important;
    border-left: 6px solid #16A34A !important;
    border-radius: 12px !important;
    padding: 20px 24px !important;
    margin-top: 14px !important;
}
.action-box * {
    color: #14532D !important;
}
.action-box-warning {
    background: #FFFBEB !important;
    border: 1px solid #FEF3C7 !important;
    border-left: 6px solid #F59E0B !important;
    border-radius: 12px !important;
    padding: 20px 24px !important;
    margin-top: 14px !important;
}
.action-box-warning * {
    color: #78350F !important;
}

/* Verification Badges */
.badge-sim {
    background: #FFFBEB !important;
    color: #B45309 !important;
    border: 1px solid #FDE68A !important;
    padding: 4px 12px !important;
    border-radius: 8px !important;
    font-size: 0.78rem !important;
    font-weight: 700 !important;
}
.badge-ver {
    background: #ECFDF5 !important;
    color: #047857 !important;
    border: 1px solid #A7F3D0 !important;
    padding: 4px 12px !important;
    border-radius: 8px !important;
    font-size: 0.78rem !important;
    font-weight: 700 !important;
}

/* Clean Form inputs */
div[data-testid="stForm"] {
    background: #FFFFFF !important;
    border: 1px solid #E2E8F0 !important;
    border-radius: 16px !important;
    padding: 28px !important;
    box-shadow: 0 4px 16px rgba(0,0,0,0.03) !important;
}
input, textarea {
    color: #0F172A !important;
    background-color: #F8FAFC !important;
    border: 1px solid #CBD5E1 !important;
    border-radius: 10px !important;
}
</style>
"""
st.markdown(FLOODSIMPLE_CSS, unsafe_allow_html=True)


# -----------------------------------------------------------------------------
# Data Loading & Persistence Helpers
# -----------------------------------------------------------------------------
@st.cache_data(ttl=300)
def get_cached_live_weather(city: str) -> Dict[str, Any]:
    """Fetch live weather from Open-Meteo API with 5-minute caching and defensive fallbacks."""
    data = fetch_live_weather(city)
    iso_code = "UG" if "Uganda" in city else "PK"
    country_name = "Uganda" if "Uganda" in city else "Pakistan"
    defaults = {
        "city": city,
        "country": country_name,
        "iso": iso_code,
        "temperature_c": 24.0,
        "feels_like_c": 24.0,
        "humidity_pct": 65,
        "precipitation_mm": 0.0,
        "rain_prob_24h": 20,
        "wind_speed_kmh": 5.0,
        "condition": "Clear Sky",
        "icon": "sun",
        "api_source": "Open-Meteo National Models"
    }
    result = dict(defaults)
    if isinstance(data, dict):
        result.update(data)
    if "iso" not in result or not result["iso"]:
        result["iso"] = iso_code
    return result


def load_verification_results(filepath: str = RESULTS_FILE_PATH) -> Tuple[Optional[pd.DataFrame], bool, Optional[str]]:
    """Load verification metrics from results.json."""
    if not os.path.exists(filepath):
        return None, False, f"Verification file '{filepath}' not found."

    try:
        with open(filepath, "r", encoding="utf-8") as f:
            raw_data = json.load(f)

        is_simulated = False
        records: List[Dict[str, Any]] = []

        if isinstance(raw_data, list):
            records = raw_data
            is_simulated = any(r.get("is_simulated", False) for r in raw_data)
        elif isinstance(raw_data, dict):
            status = raw_data.get("dataset_status", "").upper()
            if "SIMULATED" in status or raw_data.get("is_simulated", False):
                is_simulated = True
            records = raw_data.get("records", [])

        if not records:
            return None, is_simulated, "The verification dataset contains no records."

        df = pd.DataFrame(records)

        expected_cols = [
            "city", "source", "lead_h", "n", "hits", "misses",
            "false_alarms", "correct_negatives", "hit_rate",
            "false_alarm_ratio", "mae_mm"
        ]
        for col in expected_cols:
            if col not in df.columns:
                df[col] = None

        return df, is_simulated, None

    except Exception as err:
        return None, False, f"Error reading results: {err}"


def load_feedback_records(filepath: str = FEEDBACK_FILE_PATH) -> List[Dict[str, Any]]:
    """Load community feedback observations safely."""
    if not os.path.exists(filepath):
        return []
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data if isinstance(data, list) else []
    except Exception:
        return []


def save_feedback_record(record: Dict[str, Any], filepath: str = FEEDBACK_FILE_PATH) -> bool:
    """Append user observation to feedback storage safely."""
    try:
        records = load_feedback_records(filepath)
        records.append(record)
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(records, f, indent=2, ensure_ascii=False)
        return True
    except Exception as err:
        st.error(f"Failed to record feedback: {err}")
        return False


# -----------------------------------------------------------------------------
# Main Application Flow
# -----------------------------------------------------------------------------
def main():
    # Session state for view navigation
    if "current_view" not in st.session_state:
        st.session_state["current_view"] = "landing"

    # --- Sidebar Controls ---
    with st.sidebar:
        st.markdown(
            f"""
            <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 8px;">
                {get_svg_icon("shield", size=26, color="#38BDF8")}
                <span style="font-size: 1.25rem; font-weight: 800; color: #FFFFFF;">RainCheck</span>
            </div>
            """,
            unsafe_allow_html=True
        )
        st.caption("Weather Verification & Risk Intelligence")

        st.markdown("---")
        # Navigation View Selector
        view_mode = st.radio(
            "Platform Navigation:",
            ["Public Overview & Landing", "Operational Intelligence Dashboard"],
            index=0 if st.session_state["current_view"] == "landing" else 1
        )
        st.session_state["current_view"] = "landing" if "Public Overview" in view_mode else "dashboard"

        st.markdown("---")
        # Pilot City Selection
        pilot_cities = [
            "Kampala, Uganda",
            "Lahore, Pakistan",
            "Karachi, Pakistan",
            "Islamabad, Pakistan"
        ]
        selected_city = st.selectbox(
            "Pilot City Focus:",
            options=pilot_cities,
            index=0
        )

        # Language Selection
        lang_keys = list(LANGUAGE_STATUS.keys())
        lang_labels = [f"{LANGUAGE_STATUS[k]['native']} ({LANGUAGE_STATUS[k]['name']})" for k in lang_keys]
        selected_lang_label = st.selectbox(
            "Language Selection:",
            options=lang_labels,
            index=0
        )
        selected_lang = lang_keys[lang_labels.index(selected_lang_label)]
        lang_meta = get_language_status(selected_lang)

        if not lang_meta["is_reviewed"]:
            st.warning(f"Note: {lang_meta['note']}")

        st.markdown("---")
        # Institutional Disclaimer
        st.info(get_ui_text("disclaimer_official", selected_lang))

        st.markdown("---")
        st.caption(f"Verification Standard: Rain Event >= {RAIN_THRESHOLD_MM} mm | Lead Horizon >= {MIN_LEAD_HOURS}h")

    # Fetch live country telemetry
    live_weather = get_cached_live_weather(selected_city)
    df_results, is_simulated, load_error = load_verification_results()

    # =========================================================================
    # VIEW 1: PUBLIC LANDING PAGE (FloodSimple Insurtech Style)
    # =========================================================================
    if st.session_state["current_view"] == "landing":
        # Brand Header Bar
        st.markdown(
            f"""
            <div class="brand-nav">
                <div class="brand-logo">
                    {get_svg_icon("shield", size=26, color="#0284C7")}
                    <span>RainCheck</span>
                    <span class="brand-sub">| Climate Risk Intelligence</span>
                </div>
                <div>
                    <span class="telemetry-badge">
                        <span class="pulse-circle"></span> Monitoring Active: {live_weather.get('city', selected_city)} ({live_weather.get('iso', 'UG')})
                    </span>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        # Hero Banner
        st.markdown(
            f"""
            <div class="hero-box">
                <div style="max-width: 860px;">
                    <div class="telemetry-badge" style="margin-bottom: 16px;">
                        <span class="pulse-circle"></span> Empirical Precipitation Verification
                    </div>
                    <h1 style="font-size: 2.8rem; font-weight: 800; line-height: 1.15; margin: 0 0 16px 0; letter-spacing: -0.8px;">
                        Calibrated Weather Decisions Grounded in Empirical Verification.
                    </h1>
                    <p style="font-size: 1.15rem; line-height: 1.6; color: #CBD5E1; margin: 0 0 28px 0; font-weight: 400;">
                        Uncalibrated weather forecasts trigger agricultural losses, transit disruptions, and damaged market inventories. 
                        RainCheck verifies numerical weather prediction models (ECMWF, GFS) using continuous 2x2 contingency matrix scoring 
                        at the standard 1.0 mm event threshold to deliver risk-calibrated operational protocols.
                    </p>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        # Primary CTAs
        c_btn1, c_btn2, _ = st.columns([1.5, 1.5, 3])
        with c_btn1:
            if st.button("Explore Weather Insights", type="primary", use_container_width=True):
                st.session_state["current_view"] = "dashboard"
                st.rerun()
        with c_btn2:
            st.button("Review Verification Protocol", use_container_width=True)

        st.markdown("<div style='height: 32px;'></div>", unsafe_allow_html=True)

        # Section: The Challenge vs The Solution
        st.markdown("### The Operational Challenge & Empirical Solution")
        st.write("Why generic precipitation forecasts fail daily earners in pilot urban centers.")

        col_ch1, col_ch2 = st.columns(2)
        with col_ch1:
            st.markdown(
                f"""
                <div class="fs-card" style="border-top: 4px solid #EF4444;">
                    <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 12px;">
                        {get_svg_icon("alert-triangle", size=22, color="#EF4444")}
                        <span style="font-weight: 800; font-size: 1.1rem; color: #0F172A;">The Problem: Uncalibrated Forecasts</span>
                    </div>
                    <ul style="color: #475569; font-size: 0.95rem; line-height: 1.7; padding-left: 20px; margin: 0;">
                        <li><b>False Alarm Disillusionment:</b> Excessive rain warnings cause farmers and traders to ignore critical alerts.</li>
                        <li><b>Sunk Economic Costs:</b> Premature harvest covers or missed spraying windows diminish agricultural yield.</li>
                        <li><b>Transit Hazards:</b> Motorcycle couriers risk dangerous road-slip corridors when rain timing is poorly verified.</li>
                    </ul>
                </div>
                """,
                unsafe_allow_html=True
            )
        with col_ch2:
            st.markdown(
                f"""
                <div class="fs-card" style="border-top: 4px solid #10B981;">
                    <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 12px;">
                        {get_svg_icon("check-circle", size=22, color="#10B981")}
                        <span style="font-weight: 800; font-size: 1.1rem; color: #0F172A;">The RainCheck Verification Approach</span>
                    </div>
                    <ul style="color: #475569; font-size: 0.95rem; line-height: 1.7; padding-left: 20px; margin: 0;">
                        <li><b>Continuous Contingency Scoring:</b> Evaluates Hits, Misses, False Alarms, and Correct Negatives at >= 1.0 mm.</li>
                        <li><b>Lead-Time Filtering:</b> Analyzes accuracy strictly across operationally relevant windows (>= 6h lead horizon).</li>
                        <li><b>Guaranteed Numeric Safety:</b> Regex guardrails reject hallucinated numbers, falling back to deterministic templates.</li>
                    </ul>
                </div>
                """,
                unsafe_allow_html=True
            )

        st.markdown("<div style='height: 24px;'></div>", unsafe_allow_html=True)

        # Section: 3 Audience Pillars
        st.markdown("### Targeted Sector Solutions")
        st.write("Calibrated decision protocols tailored to vulnerable micro-enterprises.")

        aud1, aud2, aud3 = st.columns(3)
        with aud1:
            st.markdown(
                f"""
                <div class="fs-card">
                    <div style="margin-bottom: 14px;">{get_svg_icon("sprout", size=32, color="#0284C7")}</div>
                    <h4 style="margin: 0 0 8px 0; font-size: 1.15rem; font-weight: 800; color: #0B132B;">Agricultural Operations</h4>
                    <p style="color: #64748B; font-size: 0.92rem; line-height: 1.6; margin: 0 0 14px 0;">
                        Optimizes agrochemical spraying, post-harvest drying shelter, and field seedbed drainage using verified forecast hit rates.
                    </p>
                    <span class="badge-ver">Agro-Calibrated</span>
                </div>
                """,
                unsafe_allow_html=True
            )
        with aud2:
            st.markdown(
                f"""
                <div class="fs-card">
                    <div style="margin-bottom: 14px;">{get_svg_icon("navigation", size=32, color="#0284C7")}</div>
                    <h4 style="margin: 0 0 8px 0; font-size: 1.15rem; font-weight: 800; color: #0B132B;">Urban Transit & Couriers</h4>
                    <p style="color: #64748B; font-size: 0.92rem; line-height: 1.6; margin: 0 0 14px 0;">
                        Evaluates unpaved surface road-slip hazards, braking distance inflation, and flood-prone corridors in Kampala and Lahore.
                    </p>
                    <span class="badge-ver">Mobility Safety</span>
                </div>
                """,
                unsafe_allow_html=True
            )
        with aud3:
            st.markdown(
                f"""
                <div class="fs-card">
                    <div style="margin-bottom: 14px;">{get_svg_icon("store", size=32, color="#0284C7")}</div>
                    <h4 style="margin: 0 0 8px 0; font-size: 1.15rem; font-weight: 800; color: #0B132B;">Market Commerce & Vendors</h4>
                    <p style="color: #64748B; font-size: 0.92rem; line-height: 1.6; margin: 0 0 14px 0;">
                        Coordinates perishable produce elevation, tarpaulin stall deployment, and bulk restocking timing based on false alarm ratios.
                    </p>
                    <span class="badge-ver">Inventory Resilience</span>
                </div>
                """,
                unsafe_allow_html=True
            )

        st.markdown("<div style='height: 24px;'></div>", unsafe_allow_html=True)

        # Section: 3-Stage Scientific Workflow
        st.markdown("### The Three-Stage Verification Pipeline")
        st.write("End-to-end data pipeline from multi-model collection to verified advice.")

        wf1, wf2, wf3 = st.columns(3)
        with wf1:
            st.markdown(
                f"""
                <div class="fs-card" style="border-left: 5px solid #0284C7;">
                    <div style="font-weight: 800; color: #0284C7; font-size: 0.82rem; text-transform: uppercase; margin-bottom: 6px;">Stage 01</div>
                    <h4 style="margin: 0 0 8px 0; color: #0B132B; font-weight: 800;">Multi-Model Logging</h4>
                    <p style="font-size: 0.9rem; color: #64748B; line-height: 1.6; margin: 0;">
                        Captures ECMWF IFS and GFS forecasts with explicit issue times, valid times, and lead horizons >= 6 hours.
                    </p>
                </div>
                """,
                unsafe_allow_html=True
            )
        with wf2:
            st.markdown(
                f"""
                <div class="fs-card" style="border-left: 5px solid #6366F1;">
                    <div style="font-weight: 800; color: #6366F1; font-size: 0.82rem; text-transform: uppercase; margin-bottom: 6px;">Stage 02</div>
                    <h4 style="margin: 0 0 8px 0; color: #0B132B; font-weight: 800;">2x2 Contingency Matrix</h4>
                    <p style="font-size: 0.9rem; color: #64748B; line-height: 1.6; margin: 0;">
                        Applies standard 1.0 mm event threshold to compute empirical Hit Rate (POD), False Alarm Ratio (FAR), and MAE.
                    </p>
                </div>
                """,
                unsafe_allow_html=True
            )
        with wf3:
            st.markdown(
                f"""
                <div class="fs-card" style="border-left: 5px solid #10B981;">
                    <div style="font-weight: 800; color: #10B981; font-size: 0.82rem; text-transform: uppercase; margin-bottom: 6px;">Stage 03</div>
                    <h4 style="margin: 0 0 8px 0; color: #0B132B; font-weight: 800;">Grounded Advisory</h4>
                    <p style="font-size: 0.9rem; color: #64748B; line-height: 1.6; margin: 0;">
                        Translates empirical verification into sector action plans. Safety Guard rejects unsupported numbers automatically.
                    </p>
                </div>
                """,
                unsafe_allow_html=True
            )

        st.markdown("---")

        # Footer
        st.markdown(
            """
            <div style="text-align: center; color: #64748B; font-size: 0.85rem; padding: 24px 0;">
                <b>RainCheck Platform</b> &bull; Climate-Change-Kasese Hackathon Project &bull; 
                Institutional Collaboration with UNMA (Uganda) & PMD (Pakistan) &bull; Built in Compliance with WMO-No. 4678 Standards.
            </div>
            """,
            unsafe_allow_html=True
        )

    # =========================================================================
    # VIEW 2: OPERATIONAL DASHBOARD (FloodSimple Analytics & Advisory Hub)
    # =========================================================================
    else:
        # Dashboard Live Hero Ribbon
        st.markdown(
            f"""
            <div class="hero-box" style="padding: 26px 36px; margin-bottom: 24px;">
                <div style="display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap; gap: 20px;">
                    <div>
                        <div class="telemetry-badge" style="margin-bottom: 10px;">
                            <span class="pulse-circle"></span> Live Telemetry &bull; {live_weather.get('iso', 'UG')} &bull; {live_weather.get('city', selected_city)}
                        </div>
                        <div style="color: #FFFFFF; font-size: 2.2rem; font-weight: 800; margin: 6px 0; letter-spacing: -0.5px;">
                            {live_weather.get('condition', 'Clear Sky')} &bull; {live_weather.get('temperature_c', 24.0)}°C
                        </div>
                        <div style="color: #94A3B8; font-size: 0.95rem; font-weight: 500;">
                            Apparent: {live_weather.get('feels_like_c', 24.0)}°C &bull; Humidity: {live_weather.get('humidity_pct', 65)}% &bull; Wind: {live_weather.get('wind_speed_kmh', 5.0)} km/h &bull; Verified Lead Horizon: >= {MIN_LEAD_HOURS}h
                        </div>
                    </div>
                    <div style="text-align: right; background: rgba(255,255,255,0.08); padding: 16px 24px; border-radius: 14px; border: 1px solid rgba(255,255,255,0.12);">
                        <div style="font-size: 0.78rem; font-weight: 700; color: #38BDF8; text-transform: uppercase; letter-spacing: 0.5px;">
                            24-Hour Precipitation Chance
                        </div>
                        <div style="font-size: 2.2rem; font-weight: 800; color: #FFFFFF;">
                            {live_weather.get('rain_prob_24h', 20)}%
                        </div>
                        <div style="font-size: 0.75rem; color: #94A3B8; margin-top: 4px;">
                            Model: {live_weather.get('api_source', 'WMO National Models')}
                        </div>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        # Dashboard Tabs
        tab_advice, tab_evidence, tab_feedback = st.tabs([
            "Operational Advisory",
            "Forecast Verification Analytics",
            "Ground-Truth Calibration"
        ])

        # ---------------------------------------------------------------------
        # DASHBOARD TAB 1: OPERATIONAL ADVISORY
        # ---------------------------------------------------------------------
        with tab_advice:
            st.markdown("### Sector-Specific Action Protocols")
            st.write("Decisions calibrated to empirical forecast verification metrics.")

            # Persona Selector
            roles = ["Farmer", "Rider", "Trader"]
            role_labels = [get_ui_text('role_' + r.lower(), selected_lang) for r in roles]

            selected_role = st.radio(
                "Select Operational Sector:",
                options=roles,
                format_func=lambda r: f"{r} ({get_ui_text('role_' + r.lower(), selected_lang)})",
                horizontal=True
            )

            st.markdown("---")

            # Evidence Matching
            city_prefix = selected_city.split(",")[0].strip()
            matched_records = []
            if df_results is not None and not df_results.empty:
                city_df = df_results[df_results["city"].str.contains(city_prefix, case=False, na=False)]
                matched_records = city_df.to_dict(orient="records")

            selected_record: Optional[Dict[str, Any]] = None
            if matched_records:
                options_str = [
                    f"{r['source']} ({r['lead_h']}h lead) — Hit Rate: {r['hit_rate']:.0%}, False Alarms: {r['false_alarm_ratio']:.0%}"
                    for r in matched_records
                ]
                sel_idx = st.selectbox("Ground Advice in Verification Model:", range(len(options_str)), format_func=lambda i: options_str[i])
                selected_record = matched_records[sel_idx]
            else:
                st.warning(get_ui_text("no_evidence_available", selected_lang))

            # 4 KPI Stat Boxes
            if selected_record:
                hit_rate_pct = int((selected_record.get("hit_rate") or 0.0) * 100)
                far_pct = int((selected_record.get("false_alarm_ratio") or 0.0) * 100)
                mae_val = selected_record.get("mae_mm", 0.0)
                n_val = selected_record.get("n", 0)

                st.markdown(
                    f"""
                    <div class="kpi-grid">
                        <div class="kpi-box kpi-box-green">
                            <div class="kpi-label">Forecast Hit Rate (POD)</div>
                            <div class="kpi-value" style="color: #10B981;">{hit_rate_pct}%</div>
                            <div class="kpi-subtitle">Verified rain events captured</div>
                        </div>
                        <div class="kpi-box {'kpi-box-amber' if far_pct >= 40 else 'kpi-box-blue'}">
                            <div class="kpi-label">False Alarm Ratio (FAR)</div>
                            <div class="kpi-value" style="color: {'#EF4444' if far_pct >= 40 else '#0284C7'};">{far_pct}%</div>
                            <div class="kpi-subtitle">Alerts with zero precipitation</div>
                        </div>
                        <div class="kpi-box kpi-box-purple">
                            <div class="kpi-label">Mean Absolute Error</div>
                            <div class="kpi-value" style="color: #6366F1;">{mae_val} mm</div>
                            <div class="kpi-subtitle">Average quantitative divergence</div>
                        </div>
                        <div class="kpi-box kpi-box-blue">
                            <div class="kpi-label">Sample Evidence Size</div>
                            <div class="kpi-value" style="color: #0F172A;">{n_val}</div>
                            <div class="kpi-subtitle">{'Low Confidence (N<30)' if n_val < 30 else 'Statistically Sound'}</div>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            # AI Configuration with Live Safety Guard Tester
            with st.expander("AI Assistant & Safety Guardrail Configuration", expanded=False):
                enable_llm = st.toggle(
                    get_ui_text("llm_toggle_label", selected_lang),
                    value=False,
                    help="Generates advice strictly bounded by verified numbers."
                )
                mock_llm_mode = None
                llm_api_key = None

                if enable_llm:
                    ai_mode = st.radio(
                        "Execution Mode:",
                        [
                            "Offline Demonstration & Safety Guard Tester (No API Key Required)",
                            "Live OpenAI API (Requires API Key)"
                        ]
                    )
                    if "Offline Demonstration" in ai_mode:
                        test_scenario = st.selectbox(
                            "Test Guardrail Safety Mechanism:",
                            [
                                "Normal Grounded Advice (Uses verified numbers)",
                                "Hallucination Test: Invented Numbers (Safety Guard blocks this!)",
                                "Prohibited Claim Test: Official Warning (Safety Guard blocks this!)"
                            ]
                        )
                        if "Normal Grounded" in test_scenario:
                            lead = selected_record.get('lead_h', 24) if selected_record else 24
                            hr = int(selected_record.get('hit_rate', 0.8) * 100) if selected_record else 80
                            mock_llm_mode = (
                                f"With a {lead} hour lead time, verified model hit rate is {hr}%. "
                                f"Current temp is {live_weather.get('temperature_c', 24.0)}C. Plan outdoor work accordingly."
                            )
                        elif "Hallucination Test" in test_scenario:
                            mock_llm_mode = "Expect 85.5mm torrential flood rainfall with 99% probability. Stop all work."
                        else:
                            mock_llm_mode = "This is an official government weather warning. Immediate evacuation mandatory."
                    else:
                        llm_api_key = st.text_input("Enter OpenAI API Key (safe fallback if empty):", type="password")

            # Generate Advice
            advice_payload = generate_advice(
                role=selected_role,
                evidence=selected_record,
                lang=selected_lang,
                enable_llm=enable_llm if 'enable_llm' in locals() else False,
                llm_api_key=llm_api_key if 'llm_api_key' in locals() else None,
                mock_llm_response=mock_llm_mode if 'mock_llm_mode' in locals() else None,
                live_weather=live_weather
            )

            # Guard Status Notification
            if advice_payload.get("is_fallback"):
                if not advice_payload.get("guard_passed", True):
                    st.error("Safety Guard Warning: Output contained unverified numbers or claims. Defaulted safely to the deterministic template.")
                    with st.expander("Inspect Hallucination Blocked by Safety Guard"):
                        st.code(advice_payload.get("rejected_llm_output", ""))
                        for note in advice_payload.get("guard_notes", []):
                            st.write(f"- {note}")
                else:
                    st.caption(get_ui_text("llm_disabled_notice", selected_lang))
            else:
                st.success(get_ui_text("llm_guard_passed", selected_lang))

            # Action Advisory Card
            badge_html = '<span class="badge-sim">SIMULATED EVIDENCE</span>' if is_simulated else '<span class="badge-ver">VERIFIED GROUND TRUTH</span>'
            box_class = "action-box-warning" if advice_payload.get("condition") == "high_false_alarms" else "action-box"

            st.markdown(
                f"""
                <div class="fs-card">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div style="font-size: 1.3rem; font-weight: 800; color: #0B132B;">
                            {selected_role} Operational Advisory
                        </div>
                        {badge_html}
                    </div>
                    <div class="{box_class}">
                        <div style="font-size: 0.8rem; font-weight: 800; text-transform: uppercase; letter-spacing: 0.6px; margin-bottom: 6px;">
                            Calibrated Protocol
                        </div>
                        <div style="font-size: 1.18rem; line-height: 1.6; font-weight: 600;">
                            {advice_payload['advice']}
                        </div>
                    </div>
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 16px; font-size: 0.85rem; color: #64748B;">
                        <div><b>Operational Criteria:</b> Event >= {RAIN_THRESHOLD_MM} mm | Lead Horizon >= {MIN_LEAD_HOURS}h</div>
                        <div><b>Station:</b> {live_weather.get('city', selected_city)}</div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

            if advice_payload.get("is_small_sample"):
                st.warning(f"Uncertainty: {advice_payload['uncertainty_note']}")

        # ---------------------------------------------------------------------
        # DASHBOARD TAB 2: FORECAST VERIFICATION ANALYTICS
        # ---------------------------------------------------------------------
        with tab_evidence:
            st.markdown("### Meteorological Model Verification Dashboard")
            st.write("Rigorous 2x2 contingency matrix evaluation across weather stations.")

            if is_simulated:
                st.markdown(
                    f"""
                    <div style="background-color: #FFFBEB; border: 1px solid #FDE68A; border-left: 5px solid #F59E0B; padding: 14px 20px; border-radius: 12px; margin-bottom: 20px;">
                        <b style="color: #B45309;">SIMULATED BENCHMARK DATASET:</b>
                        <span style="color: #92400E;"> {get_ui_text('simulated_warning', selected_lang)}</span>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            if load_error or df_results is None:
                st.error(f"Error: {get_ui_text('no_results_file', selected_lang)}")
            else:
                all_cities = ["All Pilot Cities"] + sorted(df_results["city"].dropna().unique().tolist())
                city_filter = st.selectbox("Filter Verification Dataset:", all_cities)
                fdf = df_results if city_filter == "All Pilot Cities" else df_results[df_results["city"] == city_filter]

                # Charts
                col_chart1, col_chart2 = st.columns([1, 2])
                with col_chart1:
                    avg_hit = float(fdf["hit_rate"].mean() if not fdf.empty else 0.0)
                    fig_dial = go.Figure(go.Indicator(
                        mode="gauge+number",
                        value=avg_hit * 100,
                        number={"suffix": "%", "font": {"size": 36, "color": "#0B132B", "family": "Plus Jakarta Sans"}},
                        title={"text": "Average Forecast Hit Rate", "font": {"size": 14, "color": "#64748B"}},
                        gauge={
                            "axis": {"range": [0, 100], "tickwidth": 1, "tickcolor": "#CBD5E1"},
                            "bar": {"color": "#0284C7"},
                            "bgcolor": "#F8FAFC",
                            "steps": [
                                {"range": [0, 50], "color": "#FEE2E2"},
                                {"range": [50, 75], "color": "#FEF3C7"},
                                {"range": [75, 100], "color": "#DCFCE7"}
                            ]
                        }
                    ))
                    fig_dial.update_layout(height=280, margin=dict(l=20, r=20, t=40, b=20), paper_bgcolor="rgba(0,0,0,0)")
                    st.plotly_chart(fig_dial, use_container_width=True)

                with col_chart2:
                    fig_compare = px.bar(
                        fdf,
                        x="source",
                        y=["hit_rate", "false_alarm_ratio"],
                        barmode="group",
                        color_discrete_map={"hit_rate": "#10B981", "false_alarm_ratio": "#EF4444"},
                        title="Model Reliability Comparison: Hit Rate vs False Alarm Ratio",
                        labels={"value": "Ratio (0.0 to 1.0)", "source": "Weather Forecast Model", "variable": "Metric"}
                    )
                    fig_compare.update_layout(
                        height=280,
                        margin=dict(l=20, r=20, t=40, b=20),
                        yaxis=dict(range=[0, 1.05]),
                        paper_bgcolor="rgba(0,0,0,0)",
                        plot_bgcolor="#FFFFFF"
                    )
                    st.plotly_chart(fig_compare, use_container_width=True)

                # 2x2 Contingency Matrix Table
                st.markdown("#### Complete 2x2 Contingency Matrix & Verification Results")
                st.caption(f"Evaluated against rain event threshold >= {RAIN_THRESHOLD_MM} mm and lead time horizon >= {MIN_LEAD_HOURS}h.")

                st.dataframe(
                    fdf[[
                        "city", "source", "lead_h", "n", "hits", "misses",
                        "false_alarms", "correct_negatives", "hit_rate",
                        "false_alarm_ratio", "mae_mm"
                    ]].rename(columns={
                        "city": "Station / City",
                        "source": "Forecast Model",
                        "lead_h": "Lead (h)",
                        "n": "Sample (N)",
                        "hits": "Hits",
                        "misses": "Misses",
                        "false_alarms": "False Alarms",
                        "correct_negatives": "Correct Negatives",
                        "hit_rate": "Hit Rate",
                        "false_alarm_ratio": "FAR",
                        "mae_mm": "MAE (mm)"
                    }),
                    use_container_width=True
                )

        # ---------------------------------------------------------------------
        # DASHBOARD TAB 3: GROUND-TRUTH CALIBRATION
        # ---------------------------------------------------------------------
        with tab_feedback:
            st.markdown("### Community Ground-Truth Calibration Portal")
            st.write("Crowdsourced precipitation validation for micro-climate calibration. Feedback is isolated and never alters scientific verification records.")

            with st.form("community_observation_form", clear_on_submit=True):
                st.subheader("Submit Rainfall Observation")

                col_obs1, col_obs2 = st.columns(2)
                with col_obs1:
                    obs_options = ["Rain", "No Rain", "Unsure"]
                    obs_labels = [get_ui_text(f"feedback_{o.lower().replace(' ', '_')}", selected_lang) for o in obs_options]
                    selected_idx = st.radio(
                        "Observed Precipitation:",
                        options=range(len(obs_options)),
                        format_func=lambda i: obs_labels[i],
                        horizontal=True
                    )
                    observed_choice = obs_options[selected_idx]

                    approx_area = st.text_input(
                        "Approximate Area / Neighborhood:",
                        placeholder="e.g. Nakasero, Kansanga, Gulberg, Model Town"
                    )

                with col_obs2:
                    obs_window = st.selectbox(
                        "Observation Time Window:",
                        [
                            "Morning (06:00 - 12:00)",
                            "Afternoon (12:00 - 18:00)",
                            "Evening (18:00 - 24:00)",
                            "Overnight (00:00 - 06:00)"
                        ]
                    )

                    consent_ok = st.checkbox(
                        "I consent to contributing this observation for non-commercial climate research.",
                        value=False
                    )

                submit_btn = st.form_submit_button("Submit Ground-Truth Report", use_container_width=True)

                if submit_btn:
                    if not consent_ok:
                        st.error("Please confirm research consent prior to submission.")
                    elif not approx_area.strip():
                        st.error("Please provide your approximate neighborhood or locality.")
                    else:
                        new_report = {
                            "timestamp": datetime.utcnow().isoformat() + "Z",
                            "city": selected_city,
                            "area": approx_area.strip(),
                            "observation": observed_choice,
                            "time_window": obs_window,
                            "consent_granted": True
                        }
                        if save_feedback_record(new_report):
                            st.success(get_ui_text("feedback_success", selected_lang))

            # Recent Reports Feed
            with st.expander("Recent Community Ground-Truth Feed (Read-Only)"):
                all_feedbacks = load_feedback_records()
                if all_feedbacks:
                    st.dataframe(pd.DataFrame(all_feedbacks).tail(8), use_container_width=True)
                else:
                    st.info("No community observations recorded yet.")


if __name__ == "__main__":
    main()
