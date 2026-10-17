"""
app.py - RainCheck: Evidence-Based Weather & Climate Risk Intelligence.
Engineered with FloodSimple Insurtech Design System.

Features:
- Premium light insurtech aesthetic: High-contrast typography, electric cyan & navy accents
- Live Country Weather Telemetry (Open-Meteo National / WMO Models)
- Forecast Verification Engine integration (2x2 contingency matrix, 1.0mm threshold, lead_h >= 6)
- Persona Action Hubs: Farmer 🌾, Rider 🛵, Trader 🏪
- Strict Numeric Safety Guard (rejects hallucinations, 100% offline fallback)
- Community Ground-Truth Observation Portal (isolated data storage)
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

# -----------------------------------------------------------------------------
# Page Configuration
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="RainCheck — Weather Verification & Risk Intelligence",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

RESULTS_FILE_PATH = os.path.join("data", "results.json")
FEEDBACK_FILE_PATH = os.path.join("data", "feedback.json")

# -----------------------------------------------------------------------------
# FloodSimple Insurtech Design System (CSS)
# Fully enforces high-contrast, beautiful cards across dark & light browser modes
# -----------------------------------------------------------------------------
FLOODSIMPLE_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

/* Global Reset & Typography */
html, body, [class*="css"], .stApp {
    font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif !important;
    background-color: #F8FAFC !important;
    color: #0F172A !important;
}

/* Ensure all labels, texts, and markdown are high-contrast and readable */
p, span, label, h1, h2, h3, h4, h5, h6 {
    color: #0F172A !important;
}

/* Sidebar styling */
section[data-testid="stSidebar"] {
    background-color: #0B132B !important;
    border-right: 1px solid #1E293B !important;
}
section[data-testid="stSidebar"] * {
    color: #F8FAFC !important;
}
section[data-testid="stSidebar"] .stSelectbox label, 
section[data-testid="stSidebar"] .stRadio label {
    color: #E2E8F0 !important;
    font-weight: 600 !important;
}
section[data-testid="stSidebar"] .stSelectbox div[data-baseweb="select"] {
    background-color: #1E293B !important;
    border: 1px solid #334155 !important;
    border-radius: 10px !important;
    color: #FFFFFF !important;
}
section[data-testid="stSidebar"] .stSelectbox div[data-baseweb="select"] * {
    color: #FFFFFF !important;
}

/* FloodSimple Top Brand Header */
.brand-hero {
    background: linear-gradient(135deg, #0B132B 0%, #162544 50%, #0F172A 100%) !important;
    border-radius: 20px !important;
    padding: 28px 36px !important;
    margin-bottom: 24px !important;
    box-shadow: 0 10px 30px -5px rgba(11, 19, 43, 0.25) !important;
    border: 1px solid rgba(255, 255, 255, 0.1) !important;
}
.brand-hero * {
    color: #FFFFFF !important;
}

/* Live Pulse Radar Badge */
.pulse-badge {
    display: inline-flex !important;
    align-items: center !important;
    gap: 10px !important;
    padding: 6px 16px !important;
    background: rgba(16, 185, 129, 0.15) !important;
    color: #34D399 !important;
    border: 1px solid rgba(52, 211, 153, 0.35) !important;
    border-radius: 9999px !important;
    font-size: 0.8rem !important;
    font-weight: 700 !important;
    letter-spacing: 0.6px !important;
    text-transform: uppercase !important;
}
.pulse-dot {
    width: 9px !important;
    height: 9px !important;
    background-color: #10B981 !important;
    border-radius: 50% !important;
    box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.7) !important;
    animation: pulse-ring 2s infinite !important;
}
@keyframes pulse-ring {
    0% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.7); }
    70% { transform: scale(1); box-shadow: 0 0 0 8px rgba(16, 185, 129, 0); }
    100% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(16, 185, 129, 0); }
}

/* FloodSimple Navigation Tabs (Modern Segmented Pills) */
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
    padding: 10px 22px !important;
    font-size: 0.95rem !important;
    font-weight: 700 !important;
    color: #475569 !important;
    transition: all 0.2s ease !important;
}
button[data-baseweb="tab"]:hover {
    color: #0F172A !important;
    background: rgba(255, 255, 255, 0.5) !important;
}
button[data-baseweb="tab"][aria-selected="true"] {
    background: #FFFFFF !important;
    color: #0284C7 !important;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08) !important;
}
div[data-baseweb="tab-highlight"] {
    display: none !important;
}

/* FloodSimple Clean Cards */
.fs-card {
    background: #FFFFFF !important;
    border: 1px solid #E2E8F0 !important;
    border-radius: 16px !important;
    padding: 24px !important;
    margin-bottom: 20px !important;
    box-shadow: 0 4px 16px rgba(15, 23, 42, 0.04) !important;
}

/* KPI Metric Boxes */
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
    border-top: 4px solid #0284C7 !important;
}
.kpi-box-green { border-top-color: #10B981 !important; }
.kpi-box-blue { border-top-color: #0284C7 !important; }
.kpi-box-purple { border-top-color: #6366F1 !important; }
.kpi-box-amber { border-top-color: #F59E0B !important; }

.kpi-title {
    font-size: 0.78rem !important;
    font-weight: 700 !important;
    color: #64748B !important;
    text-transform: uppercase !important;
    letter-spacing: 0.5px !important;
}
.kpi-num {
    font-size: 2.1rem !important;
    font-weight: 800 !important;
    color: #0F172A !important;
    margin: 4px 0 !important;
}
.kpi-desc {
    font-size: 0.8rem !important;
    color: #0284C7 !important;
    font-weight: 600 !important;
}

/* Persona Styled Radio Selector */
div[data-testid="stRadio"] > div[role="radiogroup"] {
    display: flex !important;
    gap: 12px !important;
    margin-bottom: 12px !important;
}
div[data-testid="stRadio"] > div[role="radiogroup"] > label {
    background: #FFFFFF !important;
    border: 2px solid #E2E8F0 !important;
    border-radius: 14px !important;
    padding: 14px 22px !important;
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

/* Action Advisory Box */
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

/* Tag Badges */
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

/* Forms & Inputs */
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
    """Fetch live weather from Open-Meteo API with 5-minute caching."""
    return fetch_live_weather(city)


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
# Main Application
# -----------------------------------------------------------------------------
def main():
    # --- Sidebar Controls ---
    with st.sidebar:
        st.markdown("## 🛡️ **RainCheck**")
        st.caption("Weather Verification & Risk Intelligence")

        # 1. Pilot City Selection
        pilot_cities = [
            "Kampala, Uganda",
            "Lahore, Pakistan",
            "Karachi, Pakistan",
            "Islamabad, Pakistan"
        ]
        selected_city = st.selectbox(
            "📍 " + get_ui_text("select_city", "en"),
            options=pilot_cities,
            index=0
        )

        # 2. Language Selection
        lang_keys = list(LANGUAGE_STATUS.keys())
        lang_labels = [f"{LANGUAGE_STATUS[k]['native']} ({LANGUAGE_STATUS[k]['name']})" for k in lang_keys]
        selected_lang_label = st.selectbox(
            "🌐 " + get_ui_text("select_language", "en"),
            options=lang_labels,
            index=0
        )
        selected_lang = lang_keys[lang_labels.index(selected_lang_label)]
        lang_meta = get_language_status(selected_lang)

        if not lang_meta["is_reviewed"]:
            st.warning(f"⚠️ **Note**: {lang_meta['note']}")

        st.markdown("---")
        # Institutional Disclaimer
        st.info(get_ui_text("disclaimer_official", selected_lang))

        st.markdown("---")
        st.caption(f"**Verification Criteria**: Rain Event $\\ge {RAIN_THRESHOLD_MM}\\text{{ mm}}$ | Lead Horizon $\\ge {MIN_LEAD_HOURS}\\text{{h}}$")

    # Fetch live country weather API
    live_weather = get_cached_live_weather(selected_city)

    # --- FloodSimple Brand Header & Live Telemetry ---
    st.markdown(
        f"""
        <div class="brand-hero">
            <div style="display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap; gap: 20px;">
                <div>
                    <div class="pulse-badge">
                        <span class="pulse-dot"></span> LIVE TELEMETRY &bull; {live_weather['flag']} {live_weather['city']}
                    </div>
                    <div style="color: #FFFFFF; font-size: 2.3rem; font-weight: 800; margin: 12px 0 6px 0; letter-spacing: -0.5px;">
                        {live_weather['icon']} {live_weather['condition']} &bull; {live_weather['temperature_c']}°C
                    </div>
                    <div style="color: #94A3B8; font-size: 1rem; margin: 0; font-weight: 500;">
                        Apparent: {live_weather['feels_like_c']}°C &bull; Humidity: {live_weather['humidity_pct']}% &bull; Wind: {live_weather['wind_speed_kmh']} km/h &bull; Verified Lead Horizon: $\\ge {MIN_LEAD_HOURS}$h
                    </div>
                </div>
                <div style="text-align: right; background: rgba(255,255,255,0.08); padding: 16px 24px; border-radius: 14px; border: 1px solid rgba(255,255,255,0.12);">
                    <div style="font-size: 0.78rem; font-weight: 700; color: #38BDF8; text-transform: uppercase; letter-spacing: 0.5px;">
                        24-Hour Precipitation Chance
                    </div>
                    <div style="font-size: 2.2rem; font-weight: 800; color: #FFFFFF;">
                        {live_weather['rain_prob_24h']}%
                    </div>
                    <div style="font-size: 0.75rem; color: #94A3B8; margin-top: 4px;">
                        Source: {live_weather['api_source']}
                    </div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Load verification results
    df_results, is_simulated, load_error = load_verification_results()

    # --- FloodSimple Segmented Navigation Tabs ---
    tab_advice, tab_evidence, tab_feedback = st.tabs([
        "🛡️ Operational Advisory",
        "📊 Forecast Verification Analytics",
        "📝 Ground-Truth Calibration"
    ])

    # =========================================================================
    # TAB 1: OPERATIONAL ADVISORY (FloodSimple Card Hub)
    # =========================================================================
    with tab_advice:
        st.markdown("### 🌾 Sector-Specific Decision Protocol")
        st.write("Actionable guidance calibrated directly to verified meteorological accuracy.")

        # 1. Persona Selector
        roles = [
            ("Farmer", "🌾", "Agricultural Operations"),
            ("Rider", "🛵", "Urban Transit & Couriers"),
            ("Trader", "🏪", "Market Commerce & Vendors")
        ]
        role_names = [r[0] for r in roles]

        selected_role = st.radio(
            "Select Your Sector:",
            options=role_names,
            format_func=lambda x: f"{next(r[1] for r in roles if r[0] == x)} {get_ui_text('role_' + x.lower(), selected_lang)}",
            horizontal=True
        )

        st.markdown("---")

        # 2. Select Evidence Pairing
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
            sel_idx = st.selectbox("Calibrate against Verification Model:", range(len(options_str)), format_func=lambda i: options_str[i])
            selected_record = matched_records[sel_idx]
        else:
            st.warning(get_ui_text("no_evidence_available", selected_lang))

        # 3. FloodSimple 4 KPI Stat Boxes
        if selected_record:
            hit_rate_pct = int((selected_record.get("hit_rate") or 0.0) * 100)
            far_pct = int((selected_record.get("false_alarm_ratio") or 0.0) * 100)
            mae_val = selected_record.get("mae_mm", 0.0)
            n_val = selected_record.get("n", 0)

            st.markdown(
                f"""
                <div class="kpi-grid">
                    <div class="kpi-box kpi-box-green">
                        <div class="kpi-title">Forecast Hit Rate (POD)</div>
                        <div class="kpi-num" style="color: #10B981;">{hit_rate_pct}%</div>
                        <div class="kpi-desc">Verified rain events captured</div>
                    </div>
                    <div class="kpi-box {'kpi-box-amber' if far_pct >= 40 else 'kpi-box-blue'}">
                        <div class="kpi-title">False Alarm Ratio (FAR)</div>
                        <div class="kpi-num" style="color: {'#EF4444' if far_pct >= 40 else '#0284C7'};">{far_pct}%</div>
                        <div class="kpi-desc">Rain alerts with zero rain</div>
                    </div>
                    <div class="kpi-box kpi-box-purple">
                        <div class="kpi-title">Mean Absolute Error</div>
                        <div class="kpi-num" style="color: #6366F1;">{mae_val} mm</div>
                        <div class="kpi-desc">Average rainfall divergence</div>
                    </div>
                    <div class="kpi-box kpi-box-blue">
                        <div class="kpi-title">Sample Evidence Size</div>
                        <div class="kpi-num" style="color: #0F172A;">{n_val}</div>
                        <div class="kpi-desc">{'⚠️ Low (N<30)' if n_val < 30 else '✅ Statistically Sound'}</div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

        # 4. Optional AI Assistant with Guardrail Inspection
        with st.expander("⚙️ Optional AI Assistant & Safety Guardrail Settings", expanded=False):
            enable_llm = st.toggle(
                get_ui_text("llm_toggle_label", selected_lang),
                value=False,
                help="Generates advice strictly bounded by verification numbers."
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
                            f"Current temp is {live_weather['temperature_c']}C. Plan outdoor work accordingly."
                        )
                    elif "Hallucination Test" in test_scenario:
                        mock_llm_mode = "Expect 85.5mm torrential flood rainfall with 99% probability. Stop all work."
                    else:
                        mock_llm_mode = "This is an official government weather warning. Immediate evacuation mandatory."
                else:
                    llm_api_key = st.text_input("Enter OpenAI API Key (safe fallback if empty):", type="password")

        # 5. Generate Safe Evidence Advice
        advice_payload = generate_advice(
            role=selected_role,
            evidence=selected_record,
            lang=selected_lang,
            enable_llm=enable_llm if 'enable_llm' in locals() else False,
            llm_api_key=llm_api_key if 'llm_api_key' in locals() else None,
            mock_llm_response=mock_llm_mode if 'mock_llm_mode' in locals() else None,
            live_weather=live_weather
        )

        # Guard Status Indicator
        if advice_payload.get("is_fallback"):
            if not advice_payload.get("guard_passed", True):
                st.error("🛡️ **" + get_ui_text("llm_guard_failed", selected_lang) + "**")
                with st.expander("Inspect Hallucination Blocked by Safety Guard"):
                    st.code(advice_payload.get("rejected_llm_output", ""))
                    for note in advice_payload.get("guard_notes", []):
                        st.write(f"- ⚠️ {note}")
            else:
                st.caption("ℹ️ " + get_ui_text("llm_disabled_notice", selected_lang))
        else:
            st.success("✅ **" + get_ui_text("llm_guard_passed", selected_lang) + "**")

        # 6. FloodSimple Action Plan Card
        badge_html = '<span class="badge-sim">⚠️ SIMULATED EVIDENCE</span>' if is_simulated else '<span class="badge-ver">VERIFIED GROUND TRUTH</span>'
        box_class = "action-box-warning" if advice_payload.get("condition") == "high_false_alarms" else "action-box"

        st.markdown(
            f"""
            <div class="fs-card">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div style="font-size: 1.3rem; font-weight: 800; color: #0B132B;">
                        {get_ui_text('role_' + selected_role.lower(), selected_lang)} Operational Advisory
                    </div>
                    {badge_html}
                </div>
                <div class="{box_class}">
                    <div style="font-size: 0.8rem; font-weight: 800; text-transform: uppercase; letter-spacing: 0.6px; margin-bottom: 6px;">
                        Recommended Action Plan
                    </div>
                    <div style="font-size: 1.18rem; line-height: 1.6; font-weight: 600;">
                        {advice_payload['advice']}
                    </div>
                </div>
                <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 16px; font-size: 0.85rem; color: #64748B;">
                    <div><b>Operational Threshold:</b> Event $\\ge {RAIN_THRESHOLD_MM}$ mm | Lead Horizon $\\ge {MIN_LEAD_HOURS}$h</div>
                    <div><b>Station Location:</b> {live_weather['city']}</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        if advice_payload.get("is_small_sample"):
            st.warning(f"⚠️ {advice_payload['uncertainty_note']}")

    # =========================================================================
    # TAB 2: FORECAST VERIFICATION ANALYTICS (FloodSimple Evidence)
    # =========================================================================
    with tab_evidence:
        st.markdown("### 📊 Meteorological Verification Analytics")
        st.write("Rigorous 2x2 contingency matrix evaluation across weather stations.")

        if is_simulated:
            st.markdown(
                f"""
                <div style="background-color: #FFFBEB; border: 1px solid #FDE68A; border-left: 5px solid #F59E0B; padding: 14px 20px; border-radius: 12px; margin-bottom: 20px;">
                    <b style="color: #B45309;">⚠️ SIMULATED BENCHMARK DATASET:</b>
                    <span style="color: #92400E;"> {get_ui_text('simulated_warning', selected_lang)}</span>
                </div>
                """,
                unsafe_allow_html=True
            )

        if load_error or df_results is None:
            st.error(f"❌ {get_ui_text('no_results_file', selected_lang)}")
        else:
            all_cities = ["All Pilot Cities"] + sorted(df_results["city"].dropna().unique().tolist())
            city_filter = st.selectbox("Filter Verification Dataset:", all_cities)
            fdf = df_results if city_filter == "All Pilot Cities" else df_results[df_results["city"] == city_filter]

            # Visualizations
            col_chart1, col_chart2 = st.columns([1, 2])
            with col_chart1:
                # Semicircular Reliability Dial
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
                # Model Comparison Bar Chart
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
            st.caption(f"Evaluated against rain event threshold $\\ge {RAIN_THRESHOLD_MM}\\text{{ mm}}$ and lead time horizon $\\ge {MIN_LEAD_HOURS}\\text{{h}}$.")

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

    # =========================================================================
    # TAB 3: GROUND-TRUTH CALIBRATION (FloodSimple Feedback Portal)
    # =========================================================================
    with tab_feedback:
        st.markdown("### 📝 Community Ground-Truth Calibration Portal")
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

            submit_btn = st.form_submit_button("📤 Submit Ground-Truth Report", use_container_width=True)

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
                        st.success("✅ " + get_ui_text("feedback_success", selected_lang))

        # Recent Verified Feedbacks
        with st.expander("Recent Community Ground-Truth Feed (Read-Only)"):
            all_feedbacks = load_feedback_records()
            if all_feedbacks:
                st.dataframe(pd.DataFrame(all_feedbacks).tail(8), use_container_width=True)
            else:
                st.info("No community observations recorded yet.")


if __name__ == "__main__":
    main()
