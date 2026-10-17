"""
app.py - RainCheck: Evidence-Based Weather & Climate Risk Intelligence.
Inspired by FloodSimple Modern Insurtech & Weather Risk Architecture.

Pilots: Kampala (Uganda 🇺🇬) and Pakistani Cities (Lahore, Karachi, Islamabad 🇵🇰).
Features:
- FloodSimple-styled clean UI: Deep slate & electric azure accents, soft drop shadows, clean cards
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
# -----------------------------------------------------------------------------
FLOODSIMPLE_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
    color: #0f172a;
}

/* Background canvas */
.stApp {
    background-color: #f8fafc;
}

/* FloodSimple Top Brand Bar */
.brand-header {
    background: #0b132b;
    border-radius: 16px;
    padding: 24px 32px;
    color: white;
    margin-bottom: 24px;
    box-shadow: 0 10px 25px -5px rgba(11, 19, 43, 0.25);
    border: 1px solid #1e293b;
}

/* Live Pulse Radar Badge */
.pulse-badge {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    padding: 6px 14px;
    background: rgba(16, 185, 129, 0.15);
    color: #34d399;
    border: 1px solid rgba(52, 211, 153, 0.4);
    border-radius: 9999px;
    font-size: 0.8rem;
    font-weight: 700;
    letter-spacing: 0.5px;
    text-transform: uppercase;
}
.pulse-dot {
    width: 8px;
    height: 8px;
    background-color: #10b981;
    border-radius: 50%;
    box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.7);
    animation: pulse-ring 2s infinite;
}
@keyframes pulse-ring {
    0% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.7); }
    70% { transform: scale(1); box-shadow: 0 0 0 8px rgba(16, 185, 129, 0); }
    100% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(16, 185, 129, 0); }
}

/* FloodSimple Clean Cards */
.fs-card {
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 16px;
    padding: 24px;
    margin-bottom: 20px;
    box-shadow: 0 4px 20px -2px rgba(15, 23, 42, 0.05);
    transition: all 0.25s ease-in-out;
}
.fs-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 12px 24px -4px rgba(15, 23, 42, 0.08);
    border-color: #cbd5e1;
}

/* FloodSimple KPI Metric Boxes */
.kpi-container {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 16px;
    margin-bottom: 24px;
}
.kpi-box {
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 14px;
    padding: 18px 20px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.03);
}
.kpi-value {
    font-size: 2rem;
    font-weight: 800;
    color: #0b132b;
    margin: 4px 0;
}
.kpi-label {
    font-size: 0.82rem;
    font-weight: 600;
    color: #64748b;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}
.kpi-sub {
    font-size: 0.8rem;
    color: #0284c7;
    font-weight: 500;
}

/* Status Badges */
.badge-simulated {
    background: #fffbeb;
    color: #b45309;
    border: 1px solid #fde68a;
    padding: 4px 10px;
    border-radius: 8px;
    font-size: 0.75rem;
    font-weight: 700;
    display: inline-block;
}
.badge-verified {
    background: #ecfdf5;
    color: #047857;
    border: 1px solid #a7f3d0;
    padding: 4px 10px;
    border-radius: 8px;
    font-size: 0.75rem;
    font-weight: 700;
    display: inline-block;
}

/* Persona Action Box */
.action-box {
    background: #f0fdf4;
    border: 1px solid #bbf7d0;
    border-left: 6px solid #16a34a;
    border-radius: 12px;
    padding: 18px 22px;
    margin-top: 14px;
}
.action-box-warning {
    background: #fffbeb;
    border: 1px solid #fef3c7;
    border-left: 6px solid #f59e0b;
    border-radius: 12px;
    padding: 18px 22px;
    margin-top: 14px;
}

/* Clean Form inputs */
div[data-testid="stForm"] {
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 16px;
    padding: 24px;
    box-shadow: 0 4px 16px rgba(0,0,0,0.04);
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
    """
    Load verification metrics from JSON.
    Handles missing files, simulated data tags, and schema validation.
    """
    if not os.path.exists(filepath):
        return None, False, f"Verification file '{filepath}' not found. Please run the verification pipeline."

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

        # Standardize expected columns
        expected_cols = [
            "city", "source", "lead_h", "n", "hits", "misses",
            "false_alarms", "correct_negatives", "hit_rate",
            "false_alarm_ratio", "mae_mm"
        ]
        for col in expected_cols:
            if col not in df.columns:
                df[col] = None

        return df, is_simulated, None

    except json.JSONDecodeError as err:
        return None, False, f"Invalid JSON format in results file: {err}"
    except Exception as err:
        return None, False, f"Unexpected error reading results file: {err}"


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
    """
    Append user observation to feedback storage.
    CRITICAL: Writes strictly to feedback.json. Never alters forecast verification metrics.
    """
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
# Main Application Layout
# -----------------------------------------------------------------------------
def main():
    # --- Sidebar Controls ---
    with st.sidebar:
        st.markdown("### 🛡️ **RainCheck**")
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
        st.caption(f"**Agreed Standard**: Rain Event $\\ge {RAIN_THRESHOLD_MM}\\text{{ mm}}$ | Minimum Lead $\\ge {MIN_LEAD_HOURS}\\text{{h}}$")

    # Fetch live country weather API
    live_weather = get_cached_live_weather(selected_city)

    # --- FloodSimple Brand Header & Live Telemetry ---
    st.markdown(
        f"""
        <div class="brand-header">
            <div style="display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap; gap: 16px;">
                <div>
                    <div class="pulse-badge">
                        <span class="pulse-dot"></span> LIVE TELEMETRY STREAM &bull; {live_weather['flag']} {live_weather['city']}
                    </div>
                    <h1 style="color: white; font-size: 2.2rem; font-weight: 800; margin: 12px 0 6px 0; letter-spacing: -0.5px;">
                        {live_weather['icon']} {live_weather['condition']} &bull; {live_weather['temperature_c']}°C
                    </h1>
                    <p style="color: #94a3b8; font-size: 1rem; margin: 0;">
                        Apparent: {live_weather['feels_like_c']}°C &bull; Humidity: {live_weather['humidity_pct']}% &bull; Wind: {live_weather['wind_speed_kmh']} km/h &bull; Lead Time Horizon: $\\ge {MIN_LEAD_HOURS}$h
                    </p>
                </div>
                <div style="text-align: right; background: rgba(255,255,255,0.06); padding: 12px 20px; border-radius: 12px; border: 1px solid rgba(255,255,255,0.1);">
                    <div style="font-size: 0.78rem; font-weight: 700; color: #38bdf8; text-transform: uppercase; letter-spacing: 0.5px;">
                        24-Hour Precipitation Chance
                    </div>
                    <div style="font-size: 2rem; font-weight: 800; color: #ffffff;">
                        {live_weather['rain_prob_24h']}%
                    </div>
                    <div style="font-size: 0.75rem; color: #94a3b8;">
                        Model: {live_weather['api_source']}
                    </div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Load verification results
    df_results, is_simulated, load_error = load_verification_results()

    # --- FloodSimple Navigation Tabs ---
    tab_advice, tab_evidence, tab_feedback = st.tabs([
        "🛡️ Operational Advice",
        "📊 Forecast Verification Evidence",
        "📝 Ground-Truth Calibration"
    ])

    # =========================================================================
    # TAB 1: OPERATIONAL ADVICE (FloodSimple Card Hub)
    # =========================================================================
    with tab_advice:
        st.markdown("### Actionable Guidance Grounded in Evidence")
        st.write("Decisions calibrated to verified forecast reliability rather than generic probabilities.")

        # 1. Persona Selector
        role_cols = st.columns(3)
        roles = [
            ("Farmer", "🌾", "Agricultural Operations", "Soil moisture, spraying schedules & harvest drying protection."),
            ("Rider", "🛵", "Urban Transit & Couriers", "Braking distance, flood-prone routes & road surface safety."),
            ("Trader", "🏪", "Market Commerce & Vendors", "Stall protection, inventory elevation & perishable preservation.")
        ]

        # Use radio for accessible clean selection
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
            sel_idx = st.selectbox("Ground Advice in Verification Model:", range(len(options_str)), format_func=lambda i: options_str[i])
            selected_record = matched_records[sel_idx]
        else:
            st.warning(get_ui_text("no_evidence_available", selected_lang))

        # 3. FloodSimple Live Risk & Reliability Display
        if selected_record:
            hit_rate_pct = int((selected_record.get("hit_rate") or 0.0) * 100)
            far_pct = int((selected_record.get("false_alarm_ratio") or 0.0) * 100)
            mae_val = selected_record.get("mae_mm", 0.0)

            # 4 KPI Stat Widgets (FloodSimple style)
            st.markdown(
                f"""
                <div class="kpi-container">
                    <div class="kpi-box">
                        <div class="kpi-label">Forecast Hit Rate (POD)</div>
                        <div class="kpi-value" style="color: #10b981;">{hit_rate_pct}%</div>
                        <div class="kpi-sub">Verified rain events captured</div>
                    </div>
                    <div class="kpi-box">
                        <div class="kpi-label">False Alarm Ratio (FAR)</div>
                        <div class="kpi-value" style="color: {'#ef4444' if far_pct >= 40 else '#3b82f6'};">{far_pct}%</div>
                        <div class="kpi-sub">Warnings without rainfall</div>
                    </div>
                    <div class="kpi-box">
                        <div class="kpi-label">Mean Absolute Error</div>
                        <div class="kpi-value" style="color: #6366f1;">{mae_val} mm</div>
                        <div class="kpi-sub">Average quantitative divergence</div>
                    </div>
                    <div class="kpi-box">
                        <div class="kpi-label">Sample Evidence Size</div>
                        <div class="kpi-value" style="color: #0b132b;">{selected_record['n']}</div>
                        <div class="kpi-sub">{'⚠️ Low Confidence (N<30)' if selected_record['n'] < 30 else '✅ Statistically Sound'}</div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

        # 4. AI Guardrail Controls
        with st.expander("⚙️ Optional AI Assistant & Guardrail Verification Engine", expanded=False):
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

        # Guard Status Banner
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
        badge_html = '<span class="badge-simulated">⚠️ SIMULATED EVIDENCE</span>' if is_simulated else '<span class="badge-verified">VERIFIED GROUND TRUTH</span>'
        box_class = "action-box-warning" if advice_payload.get("condition") == "high_false_alarms" else "action-box"

        st.markdown(
            f"""
            <div class="fs-card">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div style="font-size: 1.3rem; font-weight: 700; color: #0b132b;">
                        {get_ui_text('role_' + selected_role.lower(), selected_lang)} Operational Advisory
                    </div>
                    {badge_html}
                </div>
                <div class="{box_class}">
                    <div style="font-size: 0.85rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.5px; color: #0f172a; margin-bottom: 6px;">
                        Recommended Protocol
                    </div>
                    <div style="font-size: 1.15rem; line-height: 1.6; font-weight: 600; color: #0f172a;">
                        {advice_payload['advice']}
                    </div>
                </div>
                <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 16px; font-size: 0.85rem; color: #64748b;">
                    <div><b>Operational Threshold:</b> Event $\\ge {RAIN_THRESHOLD_MM}$ mm | Lead $\\ge {MIN_LEAD_HOURS}$h</div>
                    <div><b>Calibrated for:</b> {live_weather['city']}</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        if advice_payload.get("is_small_sample"):
            st.warning(f"⚠️ {advice_payload['uncertainty_note']}")

    # =========================================================================
    # TAB 2: FORECAST VERIFICATION EVIDENCE (FloodSimple Analytics)
    # =========================================================================
    with tab_evidence:
        st.markdown("### Meteorological Model Verification Dashboard")
        st.write("Rigorous 2x2 contingency evaluation across pilot observation stations.")

        if is_simulated:
            st.markdown(
                f"""
                <div style="background-color: #fffbeb; border: 1px solid #fde68a; border-left: 5px solid #f59e0b; padding: 14px 18px; border-radius: 10px; margin-bottom: 20px;">
                    <b style="color: #b45309;">⚠️ SIMULATED BENCHMARK DATASET:</b>
                    <span style="color: #92400e;"> {get_ui_text('simulated_warning', selected_lang)}</span>
                </div>
                """,
                unsafe_allow_html=True
            )

        if load_error or df_results is None:
            st.error(f"❌ {get_ui_text('no_results_file', selected_lang)}")
        else:
            # City filter
            all_cities = ["All Pilot Cities"] + sorted(df_results["city"].dropna().unique().tolist())
            city_filter = st.selectbox("Filter Verification Cohort:", all_cities)
            fdf = df_results if city_filter == "All Pilot Cities" else df_results[df_results["city"] == city_filter]

            # Visualizations (FloodSimple Style)
            col_chart1, col_chart2 = st.columns([1, 2])
            with col_chart1:
                # Semicircular Reliability Dial
                avg_hit = float(fdf["hit_rate"].mean() if not fdf.empty else 0.0)
                fig_dial = go.Figure(go.Indicator(
                    mode="gauge+number",
                    value=avg_hit * 100,
                    number={"suffix": "%", "font": {"size": 36, "color": "#0b132b", "family": "Plus Jakarta Sans"}},
                    title={"text": "Average Forecast Hit Rate", "font": {"size": 14, "color": "#64748b"}},
                    gauge={
                        "axis": {"range": [0, 100], "tickwidth": 1, "tickcolor": "#cbd5e1"},
                        "bar": {"color": "#0284c7"},
                        "bgcolor": "#f8fafc",
                        "steps": [
                            {"range": [0, 50], "color": "#fee2e2"},
                            {"range": [50, 75], "color": "#fef3c7"},
                            {"range": [75, 100], "color": "#dcfce7"}
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
                    color_discrete_map={"hit_rate": "#10b981", "false_alarm_ratio": "#ef4444"},
                    title="Model Reliability Comparison: Hit Rate vs False Alarm Ratio",
                    labels={"value": "Ratio (0.0 to 1.0)", "source": "Weather Forecast Model", "variable": "Metric"}
                )
                fig_compare.update_layout(height=280, margin=dict(l=20, r=20, t=40, b=20), yaxis=dict(range=[0, 1.05]))
                st.plotly_chart(fig_compare, use_container_width=True)

            # Clean Contingency Table (2x2 Matrix)
            st.markdown("#### Complete Verification Results & 2x2 Contingency Matrix")
            st.caption(f"Evaluated against rain threshold $\\ge {RAIN_THRESHOLD_MM}\\text{{ mm}}$ and lead time $\\ge {MIN_LEAD_HOURS}\\text{{h}}$.")

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
    # TAB 3: GROUND-TRUTH CALIBRATION (FloodSimple Claim / Feedback Portal)
    # =========================================================================
    with tab_feedback:
        st.markdown("### Community Ground-Truth Observation Portal")
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
