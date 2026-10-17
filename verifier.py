"""
verifier.py - RainCheck Forecast Verification Engine.

Implements scientific meteorological verification standards:
- 2x2 Contingency Matrix (Hits, Misses, False Alarms, Correct Negatives)
- Binary rain occurrence threshold: 1.0 mm (standard meteorological precipitation event)
- Minimum lead time filter: >= 6 hours
- Metrics:
    * Hit Rate (Probability of Detection - POD) = Hits / (Hits + Misses)
    * False Alarm Ratio (FAR) = False Alarms / (Hits + False Alarms)
    * Critical Success Index (Threat Score - CSI) = Hits / (Hits + Misses + False Alarms)
    * Mean Absolute Error (MAE in mm) = Mean(|Forecast_mm - Observed_mm|)
- Safe handling of division-by-zero and small sample uncertainty (N < 30).
"""

import json
import os
from typing import Dict, Any, List, Optional, Tuple


RAIN_THRESHOLD_MM = 1.0  # Agreed event threshold (1.0 mm)
MIN_LEAD_HOURS = 6       # Minimum operational lead time (6h)


def calculate_contingency_counts(
    pairs: List[Dict[str, float]],
    threshold_mm: float = RAIN_THRESHOLD_MM
) -> Dict[str, int]:
    """
    Calculate 2x2 contingency table counts from paired (forecast, observed) precipitation events.
    Each pair dict must have 'forecast_mm' and 'observed_mm'.
    """
    hits = 0
    misses = 0
    false_alarms = 0
    correct_negatives = 0

    for pair in pairs:
        f_rain = pair.get("forecast_mm", 0.0) >= threshold_mm
        o_rain = pair.get("observed_mm", 0.0) >= threshold_mm

        if f_rain and o_rain:
            hits += 1
        elif (not f_rain) and o_rain:
            misses += 1
        elif f_rain and (not o_rain):
            false_alarms += 1
        else:
            correct_negatives += 1

    return {
        "hits": hits,
        "misses": misses,
        "false_alarms": false_alarms,
        "correct_negatives": correct_negatives,
        "n": len(pairs)
    }


def compute_verification_metrics(
    pairs: List[Dict[str, float]],
    threshold_mm: float = RAIN_THRESHOLD_MM
) -> Dict[str, Optional[float]]:
    """
    Compute binary and continuous verification scores from paired forecast/observation data.
    Safely handles edge cases like zero occurrences or zero alarms.
    """
    if not pairs:
        return {
            "n": 0,
            "hits": 0,
            "misses": 0,
            "false_alarms": 0,
            "correct_negatives": 0,
            "hit_rate": None,
            "false_alarm_ratio": None,
            "csi": None,
            "mae_mm": None,
            "is_small_sample": True
        }

    counts = calculate_contingency_counts(pairs, threshold_mm=threshold_mm)
    hits = counts["hits"]
    misses = counts["misses"]
    fa = counts["false_alarms"]
    cn = counts["correct_negatives"]
    n = counts["n"]

    # Hit Rate (POD): Hits / (Hits + Misses)
    rain_observed = hits + misses
    hit_rate = round(hits / rain_observed, 3) if rain_observed > 0 else 0.0

    # False Alarm Ratio (FAR): False Alarms / (Hits + False Alarms)
    rain_forecast = hits + fa
    far = round(fa / rain_forecast, 3) if rain_forecast > 0 else 0.0

    # Critical Success Index (CSI): Hits / (Hits + Misses + False Alarms)
    denom_csi = hits + misses + fa
    csi = round(hits / denom_csi, 3) if denom_csi > 0 else 0.0

    # Continuous metric: Mean Absolute Error (MAE in mm)
    absolute_errors = [
        abs(pair.get("forecast_mm", 0.0) - pair.get("observed_mm", 0.0))
        for pair in pairs
    ]
    mae = round(sum(absolute_errors) / n, 2) if n > 0 else 0.0

    return {
        "n": n,
        "hits": hits,
        "misses": misses,
        "false_alarms": fa,
        "correct_negatives": cn,
        "hit_rate": hit_rate,
        "false_alarm_ratio": far,
        "csi": csi,
        "mae_mm": mae,
        "is_small_sample": n < 30
    }


def evaluate_forecast_dataset(
    records: List[Dict[str, Any]],
    min_lead_h: int = MIN_LEAD_HOURS,
    threshold_mm: float = RAIN_THRESHOLD_MM
) -> List[Dict[str, Any]]:
    """
    Group forecast records by (city, source, lead_h) and evaluate verification metrics.
    Ensures lead time meets minimum threshold (>= 6 hours).
    """
    grouped: Dict[Tuple[str, str, int], List[Dict[str, float]]] = {}

    for r in records:
        lead_h = int(r.get("lead_h", 0))
        if lead_h < min_lead_h:
            # Exclude forecasts below minimum agreed lead time
            continue

        key = (r.get("city", "Unknown"), r.get("source", "Unknown"), lead_h)
        if key not in grouped:
            grouped[key] = []

        grouped[key].append({
            "forecast_mm": float(r.get("forecast_mm", 0.0)),
            "observed_mm": float(r.get("observed_mm", 0.0))
        })

    results: List[Dict[str, Any]] = []
    for (city, source, lead_h), pairs in grouped.items():
        metrics = compute_verification_metrics(pairs, threshold_mm=threshold_mm)
        results.append({
            "city": city,
            "source": source,
            "lead_h": lead_h,
            **metrics,
            "threshold_mm": threshold_mm,
            "is_simulated": any(r.get("is_simulated", False) for r in records)
        })

    return results


def export_verification_results(
    results: List[Dict[str, Any]],
    output_path: str = os.path.join("data", "results.json"),
    dataset_status: str = "VERIFIED"
) -> bool:
    """
    Export verified metrics to results.json strictly adhering to the integration schema.
    """
    payload = {
        "dataset_status": dataset_status,
        "rainfall_threshold_mm": RAIN_THRESHOLD_MM,
        "minimum_lead_hours": MIN_LEAD_HOURS,
        "generated_at": "2026-10-17T20:00:00Z",
        "records": results
    }
    try:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(payload, f, indent=2, ensure_ascii=False)
        return True
    except Exception as exc:
        print(f"Error saving results: {exc}")
        return False
