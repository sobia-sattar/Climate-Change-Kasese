"""
test_verifier.py - Test suite for RainCheck Forecast Verification Engine.

Tests:
1. 2x2 Contingency Table binary scoring (Hits, Misses, False Alarms, Correct Negatives).
2. Agreed 1.0 mm precipitation event threshold.
3. Metric calculations: Hit Rate, False Alarm Ratio, CSI, and MAE.
4. Exclusion of forecasts with lead time < 6 hours.
5. Small sample uncertainty detection (N < 30).
6. Safe division-by-zero resilience on edge-case zero events.
"""

import pytest
from verifier import (
    calculate_contingency_counts,
    compute_verification_metrics,
    evaluate_forecast_dataset,
    RAIN_THRESHOLD_MM,
    MIN_LEAD_HOURS
)


def test_contingency_table_with_1mm_threshold():
    """Verify that the 1.0 mm threshold correctly categorizes forecast vs observed pairs."""
    pairs = [
        {"forecast_mm": 2.5, "observed_mm": 3.0},  # Hit (both >= 1.0)
        {"forecast_mm": 0.2, "observed_mm": 1.5},  # Miss (observed >= 1.0, forecast < 1.0)
        {"forecast_mm": 1.8, "observed_mm": 0.0},  # False Alarm (forecast >= 1.0, observed < 1.0)
        {"forecast_mm": 0.5, "observed_mm": 0.2},  # Correct Negative (both < 1.0)
        {"forecast_mm": 1.0, "observed_mm": 1.0},  # Boundary Hit (exact 1.0mm)
        {"forecast_mm": 0.99, "observed_mm": 0.99} # Boundary Correct Negative (< 1.0mm)
    ]

    counts = calculate_contingency_counts(pairs, threshold_mm=1.0)

    assert counts["hits"] == 2
    assert counts["misses"] == 1
    assert counts["false_alarms"] == 1
    assert counts["correct_negatives"] == 2
    assert counts["n"] == 6


def test_hit_rate_and_far_calculations():
    """
    Hit Rate = Hits / (Hits + Misses)
    False Alarm Ratio = False Alarms / (Hits + False Alarms)
    """
    pairs = [
        {"forecast_mm": 2.0, "observed_mm": 2.0},  # Hit
        {"forecast_mm": 3.0, "observed_mm": 2.0},  # Hit
        {"forecast_mm": 4.0, "observed_mm": 2.0},  # Hit
        {"forecast_mm": 0.0, "observed_mm": 2.0},  # Miss
        {"forecast_mm": 2.0, "observed_mm": 0.0},  # False Alarm
        {"forecast_mm": 0.0, "observed_mm": 0.0},  # Correct Negative
    ]
    # Hits: 3, Misses: 1, FA: 1, CN: 1
    # Observed Rain = 4 -> Hit Rate = 3/4 = 0.75
    # Forecast Rain = 4 -> FAR = 1/4 = 0.25
    metrics = compute_verification_metrics(pairs, threshold_mm=1.0)

    assert metrics["hit_rate"] == 0.75
    assert metrics["false_alarm_ratio"] == 0.25
    assert metrics["n"] == 6


def test_mae_calculation():
    """MAE = average of absolute differences."""
    pairs = [
        {"forecast_mm": 5.0, "observed_mm": 2.0},  # |5 - 2| = 3.0
        {"forecast_mm": 1.0, "observed_mm": 2.0},  # |1 - 2| = 1.0
        {"forecast_mm": 4.0, "observed_mm": 4.0},  # |4 - 4| = 0.0
    ]
    # Sum = 4.0, N = 3 -> MAE = 1.33
    metrics = compute_verification_metrics(pairs)
    assert metrics["mae_mm"] == 1.33


def test_minimum_lead_time_filtering():
    """Forecasts with lead time < 6h must be filtered out of evaluation."""
    records = [
        {"city": "Kampala", "source": "ECMWF", "lead_h": 2, "forecast_mm": 2.0, "observed_mm": 2.0},  # Filtered (<6h)
        {"city": "Kampala", "source": "ECMWF", "lead_h": 6, "forecast_mm": 2.0, "observed_mm": 2.0},  # Included (6h)
        {"city": "Kampala", "source": "ECMWF", "lead_h": 24, "forecast_mm": 2.0, "observed_mm": 2.0}, # Included (24h)
    ]

    eval_results = evaluate_forecast_dataset(records, min_lead_h=6)
    lead_times = [r["lead_h"] for r in eval_results]

    assert 2 not in lead_times
    assert 6 in lead_times
    assert 24 in lead_times


def test_small_sample_flag():
    """Sample size N < 30 must be flagged as small sample."""
    small_pairs = [{"forecast_mm": 1.0, "observed_mm": 1.0}] * 10
    large_pairs = [{"forecast_mm": 1.0, "observed_mm": 1.0}] * 35

    res_small = compute_verification_metrics(small_pairs)
    res_large = compute_verification_metrics(large_pairs)

    assert res_small["is_small_sample"] is True
    assert res_large["is_small_sample"] is False


def test_zero_division_safety():
    """Empty dataset or all-dry conditions must not raise ZeroDivisionError."""
    empty_res = compute_verification_metrics([])
    assert empty_res["hit_rate"] is None
    assert empty_res["n"] == 0

    all_dry = [{"forecast_mm": 0.0, "observed_mm": 0.0}] * 5
    dry_res = compute_verification_metrics(all_dry)
    assert dry_res["hit_rate"] == 0.0
    assert dry_res["false_alarm_ratio"] == 0.0
    assert dry_res["mae_mm"] == 0.0
