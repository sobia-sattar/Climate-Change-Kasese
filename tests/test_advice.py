"""
test_advice.py - Test suite for RainCheck Advice Engine, Safety Guard, and Fallbacks.

Verifies:
1. Safe execution without LLM or API keys.
2. Handling of missing evidence.
3. Strict rejection of unsupported numeric claims (hallucination guard).
4. Detection and rejection of prohibited authoritative phrasing.
5. Communication of small sample uncertainty (N < 30).
6. Resilient fallback during LLM network/API exceptions.
"""

import pytest
from advice import (
    generate_advice,
    generate_deterministic_advice,
    validate_text_against_evidence,
    extract_numbers_from_text,
    extract_evidence_numeric_whitelist,
    determine_evidence_condition
)

# Standard mock evidence record based on teammate's schema
SAMPLE_EVIDENCE = {
    "city": "Kampala, Uganda",
    "source": "Open-Meteo (ECMWF IFS)",
    "lead_h": 6,
    "n": 60,
    "hits": 22,
    "misses": 3,
    "false_alarms": 4,
    "correct_negatives": 31,
    "hit_rate": 0.88,
    "false_alarm_ratio": 0.15,
    "mae_mm": 1.4,
    "is_simulated": True
}

# Small sample evidence (N < 30)
SMALL_SAMPLE_EVIDENCE = {
    "city": "Lahore, Pakistan",
    "source": "Icon Global",
    "lead_h": 48,
    "n": 18,
    "hits": 3,
    "misses": 3,
    "false_alarms": 4,
    "correct_negatives": 8,
    "hit_rate": 0.50,
    "false_alarm_ratio": 0.57,
    "mae_mm": 4.5,
    "is_simulated": True
}


def test_deterministic_fallback_no_api_key():
    """App must generate safe, grounded advice without any API key or payment."""
    result = generate_advice(
        role="Farmer",
        evidence=SAMPLE_EVIDENCE,
        lang="en",
        enable_llm=False,
        llm_api_key=None
    )
    assert result["is_fallback"] is True
    assert result["mode"] == "deterministic_template"
    assert "Protect harvested grain" in result["advice"]
    assert "RainCheck is NOT an official" in result["disclaimer"]


def test_missing_evidence_safe_handling():
    """If evidence is missing (None or empty), provide safe disclaimer advising official sources."""
    result = generate_advice(
        role="Rider",
        evidence=None,
        lang="en",
        enable_llm=False
    )
    assert result["is_fallback"] is True
    assert result["condition"] == "no_evidence"
    assert "missing" in result["advice"].lower() or "not available" in result["advice"].lower()


def test_numeric_guard_rejects_hallucinated_numbers():
    """
    CRITICAL SAFETY REQUIREMENT:
    If LLM invents an unverified rainfall amount (e.g. 50mm) or ungrounded probability (e.g. 95%),
    the safety guard must reject the text and switch to the deterministic template.
    """
    hallucinated_llm_text = (
        "There is a 95% chance of heavy rain with 50mm expected. "
        "Take immediate shelter."
    )

    result = generate_advice(
        role="Farmer",
        evidence=SAMPLE_EVIDENCE,  # Whitelist has hit_rate=0.88, mae=1.4, lead=6, etc. Neither 95 nor 50 exist!
        lang="en",
        enable_llm=True,
        mock_llm_response=hallucinated_llm_text
    )

    # Must be rejected by safety guard
    assert result["guard_passed"] is False
    assert result["is_fallback"] is True
    assert any("Unsupported number" in note for note in result["guard_notes"])
    # Resulting advice must be safe template, not hallucinated text
    assert result["advice"] != hallucinated_llm_text
    assert "Protect harvested grain" in result["advice"]


def test_numeric_guard_accepts_verified_numbers():
    """
    If LLM output cites exact numbers from the evidence (e.g., hit rate 88% or 6h lead),
    it is safely validated and returned.
    """
    grounded_llm_text = (
        "Based on verified 6 hour lead forecasts, the hit rate is 88%. "
        "Carry waterproof covers for outdoor produce."
    )

    result = generate_advice(
        role="Trader",
        evidence=SAMPLE_EVIDENCE,
        lang="en",
        enable_llm=True,
        mock_llm_response=grounded_llm_text
    )

    assert result["guard_passed"] is True
    assert result["is_fallback"] is False
    assert result["advice"] == grounded_llm_text


def test_prohibited_authoritative_claims_rejected():
    """App must never claim to be an official warning service."""
    authoritative_llm_text = "This is an official warning of imminent storm flash flooding."

    result = generate_advice(
        role="Rider",
        evidence=SAMPLE_EVIDENCE,
        lang="en",
        enable_llm=True,
        mock_llm_response=authoritative_llm_text
    )

    assert result["guard_passed"] is False
    assert result["is_fallback"] is True
    assert any("prohibited authoritative phrase" in note for note in result["guard_notes"])


def test_small_sample_size_warning():
    """Small sample size (N < 30) must be flagged with a caution note."""
    result = generate_advice(
        role="Farmer",
        evidence=SMALL_SAMPLE_EVIDENCE,  # n = 18
        lang="en",
        enable_llm=False
    )
    assert result["is_small_sample"] is True
    assert "N < 30" in result["uncertainty_note"]


def test_llm_network_failure_triggers_fallback():
    """If LLM API throws an unexpected network error, app recovers gracefully without crashing."""
    # When api_key is None and enable_llm is True (without mock), call_optional_llm_api raises ValueError
    result = generate_advice(
        role="Rider",
        evidence=SAMPLE_EVIDENCE,
        lang="en",
        enable_llm=True,
        llm_api_key=None,
        mock_llm_response=None
    )
    assert result["is_fallback"] is True
    assert result["guard_passed"] is True  # fallback is safe
    assert "waterproof gear" in result["advice"].lower()


def test_multilingual_fallbacks():
    """Deterministic fallbacks must be populated across English, Urdu, and Luganda."""
    for lang in ["en", "ur", "lg"]:
        for role in ["Farmer", "Rider", "Trader"]:
            result = generate_deterministic_advice(role, SAMPLE_EVIDENCE, lang=lang)
            assert len(result["advice"]) > 10
            assert result["disclaimer"] != ""


def test_numeric_guard_accepts_live_weather_numbers():
    """Live weather API numbers (e.g. current temp 25.6C, rain prob 35%) are recognized and verified."""
    live_weather = {
        "temperature_c": 25.6,
        "precipitation_mm": 0.5,
        "rain_prob_24h": 35,
        "humidity_pct": 72
    }
    grounded_text = (
        "Live temp is 25.6C with 35% chance of precipitation. "
        "Verified forecast hit rate remains 88%."
    )
    result = generate_advice(
        role="Farmer",
        evidence=SAMPLE_EVIDENCE,
        lang="en",
        enable_llm=True,
        mock_llm_response=grounded_text,
        live_weather=live_weather
    )
    assert result["guard_passed"] is True
    assert result["is_fallback"] is False
    assert result["advice"] == grounded_text

