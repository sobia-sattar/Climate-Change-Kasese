"""
advice.py - Evidence-Grounded Advice Generator and Safety Guard.

Core Principles:
1. Grounded strictly in verification evidence (results.json).
2. Never invents rainfall amounts, probabilities, or metrics.
3. Strict Numeric Safety Guard: Any LLM-generated number not matching
   supplied evidence triggers an immediate reject and safe fallback.
4. Deterministic fallback works 100% offline without API keys or payments.
5. Communicates uncertainty (e.g., sample size N < 30).
6. Disclaims official warning status.
"""

import re
import json
import logging
from typing import Dict, Any, Optional, Tuple, List, Set
from translations import get_ui_text, get_fallback_advice

logger = logging.getLogger(__name__)

# Disallowed claims that violate RainCheck safety guidelines
DISALLOWED_PHRASES = [
    "official warning",
    "official weather warning",
    "guaranteed forecast",
    "100% accurate",
    "100% certain",
    "national meteorological authority warning",
    "emergency evacuation",
]


def extract_numbers_from_text(text: str) -> List[float]:
    """
    Extract all integer and floating point numbers from a text string.
    Handles attached units (e.g. 25.6°C, 25.6C, 1.4mm, 6h, 88%) without improper splitting.
    """
    pattern = r"(?<![\w.])(\d+(?:\.\d+)?)(%|°C|C|mm|km/h|h)?(?![\w.])"
    matches = re.findall(pattern, text, re.IGNORECASE)
    numbers: List[float] = []

    for num_str, unit in matches:
        try:
            val = float(num_str)
            numbers.append(round(val, 3))
            if unit == "%":
                # Add decimal equivalent for percentages (e.g., 88% -> 0.88)
                numbers.append(round(val / 100.0, 3))
        except ValueError:
            continue

    return numbers


def extract_evidence_numeric_whitelist(
    evidence: Optional[Dict[str, Any]],
    live_weather: Optional[Dict[str, Any]] = None
) -> Set[float]:
    """
    Build a set of allowed numbers directly derived from the verification evidence and live weather API.
    Includes exact metrics, integer counts, lead times, and percentage representations.
    """
    whitelist: Set[float] = set()

    if evidence and isinstance(evidence, dict):
        # Numerical fields present in results.json schema
        numeric_keys = [
            "lead_h",
            "n",
            "hits",
            "misses",
            "false_alarms",
            "correct_negatives",
            "hit_rate",
            "false_alarm_ratio",
            "mae_mm"
        ]

        for key in numeric_keys:
            if key in evidence and evidence[key] is not None:
                try:
                    val = float(evidence[key])
                    whitelist.add(round(val, 3))
                    # If metric is a ratio (0.0 to 1.0), also allow its percentage equivalent
                    if 0.0 <= val <= 1.0:
                        whitelist.add(round(val * 100.0, 1))
                        whitelist.add(round(val * 100.0, 0))
                except (ValueError, TypeError):
                    pass

    if live_weather and isinstance(live_weather, dict):
        # Add accurate figures from country live weather API
        live_keys = [
            "temperature_c", "feels_like_c", "precipitation_mm",
            "rain_prob_24h", "wind_speed_kmh", "humidity_pct"
        ]
        for key in live_keys:
            if key in live_weather and live_weather[key] is not None:
                try:
                    val = float(live_weather[key])
                    whitelist.add(round(val, 3))
                    if 0.0 <= val <= 1.0:
                        whitelist.add(round(val * 100.0, 1))
                        whitelist.add(round(val * 100.0, 0))
                    elif 1.0 < val <= 100.0 and key in ("rain_prob_24h", "humidity_pct"):
                        whitelist.add(round(val / 100.0, 3))
                except (ValueError, TypeError):
                    pass

    return whitelist


def validate_text_against_evidence(
    text: str,
    evidence: Optional[Dict[str, Any]],
    live_weather: Optional[Dict[str, Any]] = None
) -> Tuple[bool, List[str]]:
    """
    Safety Guard: Validates that:
    1. No prohibited official warning claims are made.
    2. Any numeric claim in the text matches the supplied evidence whitelist.
    """
    reasons: List[str] = []
    text_lower = text.lower()

    # Check for disallowed official authority phrases
    for phrase in DISALLOWED_PHRASES:
        if phrase in text_lower:
            reasons.append(f"Contains prohibited authoritative phrase: '{phrase}'.")

    # If no evidence was provided, text MUST NOT contain any specific weather numbers
    numbers_in_text = extract_numbers_from_text(text)
    whitelist = extract_evidence_numeric_whitelist(evidence, live_weather=live_weather)

    for num in numbers_in_text:
        # Check if number matches any whitelist item within a small floating tolerance
        matched = any(abs(num - w) < 0.01 for w in whitelist)
        if not matched:
            reasons.append(
                f"Unsupported number '{num}' found in output. It does not exist in the verification evidence or live weather API."
            )

    is_valid = len(reasons) == 0
    return is_valid, reasons


def determine_evidence_condition(evidence: Optional[Dict[str, Any]]) -> str:
    """
    Classify evidence into a discrete operational condition for deterministic fallbacks:
    - 'no_evidence': Missing data or invalid record
    - 'high_false_alarms': False alarm ratio >= 0.40
    - 'high_rain': Hit rate >= 0.70 with reasonable false alarm ratio
    - 'moderate_or_dry': Default stable or dry conditions
    """
    if not evidence or not isinstance(evidence, dict):
        return "no_evidence"

    far = evidence.get("false_alarm_ratio")
    hit_rate = evidence.get("hit_rate")

    if far is None or hit_rate is None:
        return "no_evidence"

    try:
        far_f = float(far)
        hit_f = float(hit_rate)
    except (ValueError, TypeError):
        return "no_evidence"

    if far_f >= 0.40:
        return "high_false_alarms"
    elif hit_f >= 0.70:
        return "high_rain"
    else:
        return "moderate_or_dry"


def generate_deterministic_advice(
    role: str,
    evidence: Optional[Dict[str, Any]],
    lang: str = "en"
) -> Dict[str, Any]:
    """
    Produce guaranteed evidence-grounded advice using deterministic templates.
    Never fails, works offline, and requires no external API.
    """
    condition = determine_evidence_condition(evidence)
    advice_body = get_fallback_advice(role, condition, lang=lang)

    uncertainty_note = ""
    is_small_sample = False

    if evidence and isinstance(evidence, dict):
        n_count = evidence.get("n", 0)
        try:
            if int(n_count) < 30:
                is_small_sample = True
                uncertainty_note = get_ui_text("small_sample_warning", lang=lang)
        except (ValueError, TypeError):
            pass

    return {
        "advice": advice_body,
        "is_fallback": True,
        "mode": "deterministic_template",
        "condition": condition,
        "guard_passed": True,
        "guard_notes": ["Generated via deterministic template."],
        "is_small_sample": is_small_sample,
        "uncertainty_note": uncertainty_note,
        "disclaimer": get_ui_text("disclaimer_official", lang=lang)
    }


def call_optional_llm_api(
    prompt: str,
    api_key: Optional[str] = None,
    api_endpoint: Optional[str] = None,
    mock_response: Optional[str] = None
) -> str:
    """
    Optional LLM caller.
    If mock_response is provided (used in unit tests), it returns it immediately.
    If no API key is provided or request fails, raises RuntimeError to trigger fallback.
    """
    if mock_response is not None:
        return mock_response

    if not api_key:
        raise ValueError("No LLM API key configured.")

    # Generic HTTP call to allow flexible LLM providers without heavy SDK dependencies
    import requests
    endpoint = api_endpoint or "https://api.openai.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "gpt-4o-mini",
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are a weather verification assistant. Give 2 short sentences of advice. "
                    "You must ONLY mention exact numbers that appear in the prompt. "
                    "Never invent rainfall amounts, probabilities, or metrics. "
                    "Never claim to be an official warning service."
                )
            },
            {"role": "prompt", "content": prompt}
        ],
        "temperature": 0.2,
        "max_tokens": 150
    }

    response = requests.post(endpoint, headers=headers, json=payload, timeout=8)
    if response.status_code == 200:
        data = response.json()
        return data["choices"][0]["message"]["content"].strip()
    else:
        raise RuntimeError(f"LLM API returned status {response.status_code}: {response.text}")


def generate_advice(
    role: str,
    evidence: Optional[Dict[str, Any]],
    lang: str = "en",
    enable_llm: bool = False,
    llm_api_key: Optional[str] = None,
    mock_llm_response: Optional[str] = None,
    live_weather: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Master advice coordinator:
    1. If evidence is missing, immediately returns safe no-evidence template.
    2. If LLM is disabled, calls deterministic generator.
    3. If LLM is enabled:
       - Calls LLM (or mock for testing).
       - Passes LLM text through Numeric Safety Guard.
       - If guard fails, discards LLM text and falls back to deterministic template.
       - If guard passes, returns LLM advice.
    """
    # 1. Missing evidence handling
    if not evidence:
        result = generate_deterministic_advice(role, None, lang=lang)
        result["guard_notes"] = [get_ui_text("no_evidence_available", lang=lang)]
        return result

    # 2. LLM disabled by user or no API key
    if not enable_llm and mock_llm_response is None:
        return generate_deterministic_advice(role, evidence, lang=lang)

    # 3. LLM enabled: construct strictly-bounded prompt
    live_context = ""
    if live_weather:
        live_context = (
            f"Live Current Temp: {live_weather.get('temperature_c')}C, "
            f"Precipitation: {live_weather.get('precipitation_mm')}mm, "
            f"Rain Prob: {live_weather.get('rain_prob_24h')}%\n"
        )

    prompt = (
        f"Role: {role}\n"
        f"City: {evidence.get('city')}\n"
        f"{live_context}"
        f"Lead time: {evidence.get('lead_h')} hours\n"
        f"Sample size: {evidence.get('n')}\n"
        f"Hit Rate: {evidence.get('hit_rate')}\n"
        f"False Alarm Ratio: {evidence.get('false_alarm_ratio')}\n"
        f"MAE: {evidence.get('mae_mm')} mm\n"
        f"Provide 2 short practical recommendations for this user in {lang}."
    )

    try:
        raw_llm_text = call_optional_llm_api(
            prompt,
            api_key=llm_api_key,
            mock_response=mock_llm_response
        )

        # 4. Numeric Safety Guard check
        guard_passed, guard_reasons = validate_text_against_evidence(
            raw_llm_text, evidence, live_weather=live_weather
        )

        if not guard_passed:
            # REJECT hallucinated or unauthorized output
            logger.warning("LLM output rejected by Safety Guard: %s", guard_reasons)
            fallback_result = generate_deterministic_advice(role, evidence, lang=lang)
            fallback_result["guard_passed"] = False
            fallback_result["guard_notes"] = guard_reasons
            fallback_result["rejected_llm_output"] = raw_llm_text
            return fallback_result

        # Output passed all checks
        is_small_sample = int(evidence.get("n", 0)) < 30
        uncertainty_note = get_ui_text("small_sample_warning", lang=lang) if is_small_sample else ""

        return {
            "advice": raw_llm_text,
            "is_fallback": False,
            "mode": "llm_verified",
            "condition": determine_evidence_condition(evidence),
            "guard_passed": True,
            "guard_notes": [get_ui_text("llm_guard_passed", lang=lang)],
            "is_small_sample": is_small_sample,
            "uncertainty_note": uncertainty_note,
            "disclaimer": get_ui_text("disclaimer_official", lang=lang)
        }

    except Exception as exc:
        # Seamless fallback on any network error, invalid key, or timeout
        logger.info("LLM unavailable or failed (%s). Triggering safe fallback.", exc)
        fallback_result = generate_deterministic_advice(role, evidence, lang=lang)
        fallback_result["guard_notes"] = [f"LLM fallback triggered: {str(exc)}"]
        return fallback_result
