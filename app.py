"""
app.py - RainCheck Web Application
Evidence-Based Weather Verification & Actionable Advice.

Pilots: Kampala (Uganda 🇺🇬) & Pakistani Cities (Lahore, Karachi, Islamabad 🇵🇰).
Features:
- Live Country Weather API (Open-Meteo WMO / National Models - Free, high-accuracy)
- Animated, clean, responsive UI with smooth transitions and status pulses
- Crisp, non-overwhelming persona advice (Farmer, Rider, Trader)
- Regex-based Numeric Safety Guard preventing hallucinations
- Multi-page navigation: Evidence, Advice, Community Feedback
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

# -----------------------------------------------------------------------------
# Configuration & Theme
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="RainCheck — Weather Verification & Advice",
    page_icon="🌦️",
    layout="wide",
    initial_sidebar_state="expanded"
)

RESULTS_FILE_PATH = os.path.join("data", "results.json")
FEEDBACK_FILE_PATH = os.path.join("data", "feedback.json")


# -----------------------------------------------------------------------------
# CSS Styling & Animations
# -----------------------------------------------------------------------------
CUSTOM_CSS = """
<style>
/* Modern fonts and sleek layout */
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Plus Jakarta Sans', sans-serif;
}

/* Subtle card styling with hover lift animation */
.animated-card {
    background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
    border: 1px solid #e2e8f0;
    border-radius: 14px;
    padding: 20px 24px;
    margin-bottom: 16px;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
    transition: transform 0.25s ease, box-shadow 0.25s ease;
}
.animated-card:hover {
    transform: translateY(-3px);
    box-shadow: 0 12px 20px -3px rgba(0, 0, 0, 0.08);
}

/* Live pulsating indicator badge */
.pulse-badge {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    padding: 4px 12px;
    background-color: #ecfdf5;
    color: #065f46;
    border: 1px solid #a7f3d0;
    border-radius: 9999px;
    font-size: 0.82rem;
    font-weight: 600;
}
.pulse-dot {
    width: 8px;
    height: 8px;
    background-color: #10b981;
    border-radius: 50%;
    box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.7);
    animation: pulse 1.8s infinite;
}
@keyframes pulse {
    0% {
        transform: scale(0.95);
        box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.7);
    }
    70% {
        transform: scale(1);
        box-shadow: 0 0 0 8px rgba(16, 185, 129, 0);
    }
    100% {
        transform: scale(0.95);
        box-shadow: 0 0 0 0 rgba(16, 185, 129, 0);
    }
}

/* Weather Hero Header Card */
.weather-hero {
    background: linear-gradient(135deg, #0ea5e9 0%, #2563eb 100%);
    color: white;
    padding: 22px 28px;
    border-radius: 16px;
    margin-bottom: 24px;
    box-shadow: 0 10px 25px -5px rgba(37, 99, 235, 0.3);
}

/* Advice Highlight Cards */
.advice-box {
    background: #ffffff;
    border-left: 5px solid #2563eb;
    border-radius: 10px;
    padding: 18px 22px;
    margin-top: 10px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.04);
}

/* Badge tags */
.sim-badge {
    background-color: #fffbeb;
    color: #b45309;
    border: 1px solid #fde68a;
    padding: 3px 10px;
    border-radius: 6px;
    font-size: 0.8rem;
    font-weight: 600;
}
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


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
        return None, False, f"File not found: '{filepath}'. Please place results.json in the data/ directory."

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
            return None, is_simulated, "The results.json file contains no metric records."

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
# Main Application
# -----------------------------------------------------------------------------
def main():
    # --- Sidebar Controls ---
    with st.sidebar:
        st.markdown("## 🌦️ **RainCheck**")
        st.caption("Evidence-Based Weather Verification")

        # 1. Language Selection
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

        # 2. Pilot City Selector
        pilot_cities = [
            "Kampala, Uganda",
            "Lahore, Pakistan",
            "Karachi, Pakistan",
            "Islamabad, Pakistan"
        ]
        selected_city = st.selectbox(
            "📍 " + get_ui_text("select_city", selected_lang),
            options=pilot_cities,
            index=0
        )

        st.markdown("---")
        # Official Meteorological Disclaimer
        st.info(get_ui_text("disclaimer_official", selected_lang))

    # --- Live Weather API Fetch ---
    live_weather = get_cached_live_weather(selected_city)

    # --- Animated Weather Hero Banner ---
    st.markdown(
        f"""
        <div class="weather-hero">
            <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap;">
                <div>
                    <span class="pulse-badge">
                        <span class="pulse-dot"></span> LIVE COUNTRY API: {live_weather['flag']} {live_weather['city']}
                    </span>
                    <h2 style="color: white; margin: 10px 0 4px 0; font-size: 2rem;">
                        {live_weather['icon']} {live_weather['condition']} &bull; {live_weather['temperature_c']}°C
                    </h2>
                    <p style="color: #e0f2fe; margin: 0; font-size: 0.95rem;">
                        Feels like {live_weather['feels_like_c']}°C &bull; Humidity: {live_weather['humidity_pct']}% &bull; Wind: {live_weather['wind_speed_kmh']} km/h
                    </p>
                </div>
                <div style="text-align: right; margin-top: 8px;">
                    <span style="background: rgba(255,255,255,0.2); padding: 6px 14px; border-radius: 20px; font-weight: 600; font-size: 0.9rem;">
                        🌧️ 24h Rain Chance: {live_weather['rain_prob_24h']}%
                    </span>
                    <div style="font-size: 0.75rem; color: #bae6fd; margin-top: 6px;">
                        Source: {live_weather['api_source']}
                    </div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Load verification results from results.json
    df_results, is_simulated, load_error = load_verification_results()

    # --- Multi-Page Navigation Tabs ---
    tab_advice, tab_evidence, tab_feedback = st.tabs([
        "💡 " + get_ui_text("nav_advice", selected_lang),
        "📊 " + get_ui_text("nav_evidence", selected_lang),
        "📝 " + get_ui_text("nav_feedback", selected_lang)
    ])

    # =========================================================================
    # PAGE: ADVICE (Simple, Crisp, Animated)
    # =========================================================================
    with tab_advice:
        st.subheader("Actionable Guidance Grounded in Evidence")

        # 1. Role Selection
        role_options = ["Farmer", "Rider", "Trader"]
        role_emojis = {"Farmer": "🌾", "Rider": "🛵", "Trader": "🏪"}
        role_labels = [f"{role_emojis[r]} {get_ui_text(f'role_{r.lower()}', selected_lang)}" for r in role_options]

        selected_role_idx = st.radio(
            "Select Persona:",
            options=range(len(role_options)),
            format_func=lambda i: role_labels[i],
            horizontal=True,
            label_visibility="collapsed"
        )
        selected_role = role_options[selected_role_idx]

        # 2. Match verification evidence for selected city
        city_evidence_records = []
        if df_results is not None and not df_results.empty:
            city_prefix = selected_city.split(",")[0].strip()
            city_df = df_results[df_results["city"].str.contains(city_prefix, case=False, na=False)]
            city_evidence_records = city_df.to_dict(orient="records")

        selected_record: Optional[Dict[str, Any]] = None
        if city_evidence_records:
            record_options = [
                f"{r['source']} ({r['lead_h']}h lead) — Hit Rate: {r['hit_rate']:.0%}, False Alarms: {r['false_alarm_ratio']:.0%}"
                for r in city_evidence_records
            ]
            sel_rec_idx = st.selectbox(
                "Forecast Model Verification Evidence:",
                options=range(len(record_options)),
                format_func=lambda idx: record_options[idx]
            )
            selected_record = city_evidence_records[sel_rec_idx]
        else:
            st.warning("⚠️ " + get_ui_text("no_evidence_available", selected_lang))

        # 3. Quick Stats Ribbon (Visual, Simple)
        if selected_record:
            c1, c2, c3, c4 = st.columns(4)
            with c1:
                st.metric("Forecast Lead Time", f"{selected_record['lead_h']} hours")
            with c2:
                st.metric("Model Hit Rate", f"{selected_record['hit_rate']:.0%}")
            with c3:
                st.metric("False Alarm Ratio", f"{selected_record['false_alarm_ratio']:.0%}")
            with c4:
                sample_flag = "⚠️ Low (N<30)" if selected_record['n'] < 30 else "✅ Reliable"
                st.metric("Sample Size (N)", f"{selected_record['n']}", sample_flag)

        # 4. AI Guardrail Toggle (Optional)
        with st.expander("⚙️ Optional AI Assistant & Safety Guard Settings"):
            enable_llm = st.toggle(
                get_ui_text("llm_toggle_label", selected_lang),
                value=False,
                help="Generates advice using LLM with strict numeric guardrails."
            )
            mock_llm_mode = None
            llm_api_key = None

            if enable_llm:
                ai_mode = st.radio(
                    "Execution Mode:",
                    [
                        "Offline Demonstration & Safety Guard Tester (No API Key)",
                        "Live External LLM (Requires OpenAI API Key)"
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
                        mock_llm_mode = (
                            "Expect 75.5mm torrential rain with 98% probability. "
                            "Stop all operations immediately."
                        )
                    else:
                        mock_llm_mode = (
                            "This is an official national weather warning. Immediate shutdown required."
                        )
                else:
                    llm_api_key = st.text_input(
                        "Enter OpenAI API Key (safe fallback if empty):",
                        type="password"
                    )

        # 5. Generate Evidence Advice
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

        # 6. Clean, Non-Overwhelming Advice Cards
        st.markdown(
            f"""
            <div class="animated-card" style="border-left: 6px solid #2563eb;">
                <div style="display: flex; align-items: center; justify-content: space-between;">
                    <h3 style="margin: 0; color: #1e3a8a;">
                        {role_emojis[selected_role]} {get_ui_text('role_' + selected_role.lower(), selected_lang)} Recommendation
                    </h3>
                    <span class="sim-badge">
                        {'⚠️ SIMULATED EVIDENCE' if is_simulated else 'VERIFIED EVIDENCE'}
                    </span>
                </div>
                <hr style="margin: 12px 0; border: none; border-top: 1px solid #e2e8f0;"/>
                <p style="font-size: 1.15rem; line-height: 1.6; color: #1e293b; font-weight: 500; margin: 0;">
                    {advice_payload['advice']}
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

        if advice_payload.get("is_small_sample"):
            st.warning(f"⚠️ {advice_payload['uncertainty_note']}")

    # =========================================================================
    # PAGE: EVIDENCE (Interactive Charts, Visual Metrics)
    # =========================================================================
    with tab_evidence:
        st.subheader("Model Performance & Verification Data")

        if is_simulated:
            st.markdown(
                f"""
                <div style="background-color: #fffbeb; border: 1px solid #fef3c7; border-left: 4px solid #f59e0b; padding: 12px 16px; border-radius: 8px; margin-bottom: 16px;">
                    <span style="font-weight: 700; color: #b45309;">⚠️ SIMULATED DATASET:</span>
                    <span style="color: #92400e;"> {get_ui_text('simulated_warning', selected_lang)}</span>
                </div>
                """,
                unsafe_allow_html=True
            )

        if load_error or df_results is None:
            st.error(f"❌ {get_ui_text('no_results_file', selected_lang)}")
        else:
            # Filter by City
            city_opts = ["All Cities"] + sorted(df_results["city"].dropna().unique().tolist())
            city_filter = st.selectbox("Filter Verification Dataset:", options=city_opts)
            fdf = df_results if city_filter == "All Cities" else df_results[df_results["city"] == city_filter]

            # Visual Gauge & Charts
            g1, g2 = st.columns([1, 2])
            with g1:
                # Semicircular Reliability Gauge
                avg_hit = float(fdf["hit_rate"].mean() if not fdf.empty else 0.0)
                fig_gauge = go.Figure(go.Indicator(
                    mode="gauge+number",
                    value=avg_hit * 100,
                    number={"suffix": "%", "font": {"size": 32, "color": "#1e3a8a"}},
                    title={"text": "Average Hit Rate", "font": {"size": 16, "color": "#475569"}},
                    gauge={
                        "axis": {"range": [0, 100], "tickwidth": 1, "tickcolor": "#cbd5e1"},
                        "bar": {"color": "#2563eb"},
                        "bgcolor": "#f1f5f9",
                        "steps": [
                            {"range": [0, 50], "color": "#fee2e2"},
                            {"range": [50, 75], "color": "#fef3c7"},
                            {"range": [75, 100], "color": "#dcfce7"}
                        ]
                    }
                ))
                fig_gauge.update_layout(height=260, margin=dict(l=20, r=20, t=40, b=20))
                st.plotly_chart(fig_gauge, use_container_width=True)

            with g2:
                fig_bar = px.bar(
                    fdf,
                    x="source",
                    y=["hit_rate", "false_alarm_ratio"],
                    barmode="group",
                    color_discrete_map={"hit_rate": "#10b981", "false_alarm_ratio": "#ef4444"},
                    title="Hit Rate vs False Alarm Ratio by Forecast Source",
                    labels={"value": "Ratio", "source": "Model / Source", "variable": "Metric"}
                )
                fig_bar.update_layout(height=260, margin=dict(l=20, r=20, t=40, b=20), yaxis=dict(range=[0, 1.05]))
                st.plotly_chart(fig_bar, use_container_width=True)

            # Clean Collapsible Raw Data Table
            with st.expander("📋 View Complete Verification Data Table", expanded=True):
                st.dataframe(
                    fdf[[
                        "city", "source", "lead_h", "n", "hits", "misses",
                        "false_alarms", "correct_negatives", "hit_rate",
                        "false_alarm_ratio", "mae_mm"
                    ]].rename(columns={
                        "city": "City",
                        "source": "Source",
                        "lead_h": "Lead (h)",
                        "n": "N",
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
    # PAGE: FEEDBACK (Simple, Isolated Storage)
    # =========================================================================
    with tab_feedback:
        st.subheader("Community Ground-Truth Calibration")
        st.caption("Your reports help verify forecast quality. Observations are stored independently and NEVER contaminate forecast metrics.")

        with st.form("quick_feedback_form", clear_on_submit=True):
            fcol1, fcol2 = st.columns(2)
            with fcol1:
                obs_choices = ["Rain", "No Rain", "Unsure"]
                obs_labels = [get_ui_text(f"feedback_{c.lower().replace(' ', '_')}", selected_lang) for c in obs_choices]
                selected_obs_idx = st.radio(
                    "Observed Weather:",
                    options=range(len(obs_choices)),
                    format_func=lambda idx: obs_labels[idx],
                    horizontal=True
                )
                observed_val = obs_choices[selected_obs_idx]

                area_val = st.text_input(
                    "Approximate Area / Neighborhood:",
                    placeholder="e.g. Nakasero, Kansanga, Gulberg, Model Town"
                )

            with fcol2:
                time_val = st.selectbox(
                    "Observation Time Window:",
                    [
                        "Morning (06:00 - 12:00)",
                        "Afternoon (12:00 - 18:00)",
                        "Evening (18:00 - 24:00)",
                        "Overnight (00:00 - 06:00)"
                    ]
                )
                consent = st.checkbox(
                    "I consent to contributing this observation for community research.",
                    value=False
                )

            submitted = st.form_submit_button("📤 Submit Observation", use_container_width=True)
            if submitted:
                if not consent:
                    st.error("Please confirm consent before submitting.")
                elif not area_val.strip():
                    st.error("Please specify your approximate area or neighborhood.")
                else:
                    new_obs = {
                        "timestamp": datetime.utcnow().isoformat() + "Z",
                        "city": selected_city,
                        "area": area_val.strip(),
                        "observation": observed_val,
                        "time_window": time_val,
                        "consent_granted": True
                    }
                    if save_feedback_record(new_obs):
                        st.success("✅ Observation recorded safely in community storage. Thank you!")

        # Recent Submissions Viewer
        with st.expander("Recent Community Reports"):
            recent_fbs = load_feedback_records()
            if recent_fbs:
                st.dataframe(pd.DataFrame(recent_fbs).tail(5), use_container_width=True)
            else:
                st.info("No community observations recorded yet.")


if __name__ == "__main__":
    main()
