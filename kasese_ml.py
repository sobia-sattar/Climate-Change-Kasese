"""
kasese_ml.py — Random Forest Weather Forecast Model for Kasese, Uganda.

Pipeline:
  1. Load hourly historical data (from kasese_weather.py).
  2. Engineer lag features + time features.
  3. Create binary labels: rain event >= 1.0 mm for 6h and 24h windows.
  4. Chronological train/test split (no data leakage: first 80% train, last 20% test).
  5. Fit RandomForestClassifier (rain/no-rain) and RandomForestRegressor (amount).
  6. Compute full verification metrics:
       N, Hits, Misses, False Alarms, Correct Negatives,
       Accuracy, Hit Rate (POD), False Alarm Ratio (FAR), CSI, MAE.
  7. Return structured results matching results.json schema.
"""

import json
import os
import logging
from datetime import datetime
from typing import Dict, Any, List, Optional, Tuple

import numpy as np

logger = logging.getLogger(__name__)

RAIN_THRESHOLD_MM = 1.0
RESULTS_FILE = os.path.join("data", "results.json")


# ---------------------------------------------------------------------------
# Feature Engineering
# ---------------------------------------------------------------------------
def _build_features(records: List[Dict]) -> Tuple[np.ndarray, np.ndarray, np.ndarray, List[str]]:
    """
    Build feature matrix X, binary rain labels y_cls, continuous y_reg,
    and list of feature names.

    Features (for each hour i):
      - Current: temp, humidity, wind, pressure, cloud_cover, precip
      - Lag-1h to Lag-6h: precipitation_mm
      - Time: hour_of_day (sin/cos), month (sin/cos), day_of_week (sin/cos)
    """
    MIN_IDX = 7   # Need at least 6 lag hours + current
    n = len(records)
    rows_X, rows_y_cls, rows_y_reg = [], [], []

    for i in range(MIN_IDX, n):
        r = records[i]
        try:
            ts = datetime.fromisoformat(r["timestamp"])
        except Exception:
            continue

        # ----- Base features -----
        row = [
            r.get("temperature_c", 24.0),
            r.get("humidity_pct", 68.0),
            r.get("wind_speed_kmh", 5.0),
            r.get("pressure_hpa", 1013.0),
            r.get("cloud_cover_pct", 50.0),
            r.get("precipitation_mm", 0.0),
        ]

        # ----- Lag precipitation (1h .. 6h) -----
        for lag in range(1, 7):
            row.append(records[i - lag].get("precipitation_mm", 0.0))

        # ----- Cyclical time features -----
        h = ts.hour
        m = ts.month
        d = ts.weekday()
        row += [
            np.sin(2 * np.pi * h / 24), np.cos(2 * np.pi * h / 24),
            np.sin(2 * np.pi * m / 12), np.cos(2 * np.pi * m / 12),
            np.sin(2 * np.pi * d / 7),  np.cos(2 * np.pi * d / 7),
        ]

        rows_X.append(row)
        # Label: rainfall at current step (classifying current step as event)
        precip = r.get("precipitation_mm", 0.0)
        rows_y_cls.append(1 if precip >= RAIN_THRESHOLD_MM else 0)
        rows_y_reg.append(precip)

    feature_names = [
        "temperature_c", "humidity_pct", "wind_speed_kmh", "pressure_hpa",
        "cloud_cover_pct", "precip_current",
        "precip_lag1h", "precip_lag2h", "precip_lag3h",
        "precip_lag4h", "precip_lag5h", "precip_lag6h",
        "hour_sin", "hour_cos", "month_sin", "month_cos",
        "weekday_sin", "weekday_cos",
    ]
    return (
        np.array(rows_X, dtype=np.float32),
        np.array(rows_y_cls, dtype=np.int32),
        np.array(rows_y_reg, dtype=np.float32),
        feature_names,
    )


def _build_window_labels(
    records: List[Dict],
    start_indices: List[int],
    window_hours: int,
) -> Tuple[np.ndarray, np.ndarray]:
    """
    For each index in start_indices, sum precipitation over the next
    `window_hours` hours to get window-level binary label and total.
    Records that don't have enough future steps are dropped.
    """
    n = len(records)
    y_cls, y_reg = [], []
    valid_mask = []

    for i in start_indices:
        end = i + window_hours
        if end > n:
            valid_mask.append(False)
            y_cls.append(0)
            y_reg.append(0.0)
            continue
        total = sum(records[j].get("precipitation_mm", 0.0) for j in range(i, end))
        y_cls.append(1 if total >= RAIN_THRESHOLD_MM else 0)
        y_reg.append(total)
        valid_mask.append(True)

    return (
        np.array(y_cls, dtype=np.int32),
        np.array(y_reg, dtype=np.float32),
        np.array(valid_mask, dtype=bool),
    )


# ---------------------------------------------------------------------------
# Metrics computation
# ---------------------------------------------------------------------------
def _compute_metrics(
    y_true: np.ndarray,
    y_pred: np.ndarray,
    y_reg_true: np.ndarray,
    y_reg_pred: np.ndarray,
    lead_h: int,
    source: str,
    city: str = "Kasese, Uganda",
) -> Dict[str, Any]:
    """Compute full 2x2 contingency table and derived metrics."""
    hits = int(np.sum((y_true == 1) & (y_pred == 1)))
    misses = int(np.sum((y_true == 1) & (y_pred == 0)))
    false_alarms = int(np.sum((y_true == 0) & (y_pred == 1)))
    correct_neg = int(np.sum((y_true == 0) & (y_pred == 0)))
    n = hits + misses + false_alarms + correct_neg

    hit_rate = round(hits / (hits + misses), 4) if (hits + misses) > 0 else 0.0
    far = round(false_alarms / (false_alarms + hits), 4) if (false_alarms + hits) > 0 else 0.0
    accuracy = round((hits + correct_neg) / n, 4) if n > 0 else 0.0
    csi_denom = hits + misses + false_alarms
    csi = round(hits / csi_denom, 4) if csi_denom > 0 else 0.0
    mae = round(float(np.mean(np.abs(y_reg_true - y_reg_pred))), 4)

    return {
        "city": city,
        "source": source,
        "lead_h": lead_h,
        "n": n,
        "hits": hits,
        "misses": misses,
        "false_alarms": false_alarms,
        "correct_negatives": correct_neg,
        "accuracy": accuracy,
        "hit_rate": hit_rate,
        "false_alarm_ratio": far,
        "critical_success_index": csi,
        "mae_mm": mae,
        "is_simulated": False,
        "model": "Random Forest (sklearn)",
        "threshold_mm": RAIN_THRESHOLD_MM,
        "train_test_split": "chronological_80_20",
        "evaluated_at": datetime.utcnow().isoformat() + "Z",
    }


# ---------------------------------------------------------------------------
# Main training + evaluation function
# ---------------------------------------------------------------------------
def run_kasese_ml_pipeline(records: List[Dict]) -> List[Dict]:
    """
    Full ML pipeline for Kasese. Returns list of metric dicts
    (one per lead time: 6h, 24h) for both classifier and regressor.
    """
    try:
        from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
        from sklearn.preprocessing import StandardScaler
    except ImportError:
        logger.error("scikit-learn is required. Install with: pip install scikit-learn")
        return []

    if len(records) < 200:
        logger.warning("Insufficient historical records (%d). Need >= 200.", len(records))
        return []

    # Build full feature set
    X, y_cls_now, y_reg_now, feat_names = _build_features(records)
    n_total = len(X)
    split = int(n_total * 0.80)

    if split < 50 or (n_total - split) < 20:
        logger.warning("Dataset too small after feature engineering (%d rows).", n_total)
        return []

    MIN_IDX = 7   # offset used in _build_features
    feature_indices = list(range(MIN_IDX, MIN_IDX + n_total))

    results = []

    for lead_hours in [6, 24]:
        logger.info("Training RF pipeline for %dh lead time...", lead_hours)

        # Build window labels aligned to feature rows
        y_cls_w, y_reg_w, valid = _build_window_labels(records, feature_indices, lead_hours)

        # Apply validity mask
        X_valid = X[valid]
        y_cls_valid = y_cls_w[valid]
        y_reg_valid = y_reg_w[valid]

        if len(X_valid) < 100:
            continue

        n_valid = len(X_valid)
        split_v = int(n_valid * 0.80)

        X_train, X_test = X_valid[:split_v], X_valid[split_v:]
        y_cls_train, y_cls_test = y_cls_valid[:split_v], y_cls_valid[split_v:]
        y_reg_train, y_reg_test = y_reg_valid[:split_v], y_reg_valid[split_v:]

        # Classifier
        clf = RandomForestClassifier(
            n_estimators=200,
            max_depth=12,
            min_samples_leaf=5,
            class_weight="balanced",
            random_state=42,
            n_jobs=-1,
        )
        clf.fit(X_train, y_cls_train)
        y_pred_cls = clf.predict(X_test)

        # Regressor
        reg = RandomForestRegressor(
            n_estimators=200,
            max_depth=12,
            min_samples_leaf=5,
            random_state=42,
            n_jobs=-1,
        )
        reg.fit(X_train, y_reg_train)
        y_pred_reg = reg.predict(X_test).clip(min=0)

        result = _compute_metrics(
            y_cls_test,
            y_pred_cls,
            y_reg_test,
            y_pred_reg,
            lead_h=lead_hours,
            source="Random Forest (Open-Meteo Historical)",
        )
        result["feature_importances"] = dict(
            sorted(
                zip(feat_names, clf.feature_importances_.tolist()),
                key=lambda x: x[1],
                reverse=True,
            )
        )
        results.append(result)

    return results


# ---------------------------------------------------------------------------
# Save / Load pipeline results
# ---------------------------------------------------------------------------
def load_or_run_pipeline(records: Optional[List[Dict]]) -> Tuple[List[Dict], str]:
    """
    Load cached ML results if fresh, otherwise re-run the full pipeline.
    Returns (results_list, status_message).
    """
    PIPELINE_CACHE = os.path.join("data", "kasese_ml_results.json")
    CACHE_TTL_H = 12

    # Check freshness
    import time
    if os.path.exists(PIPELINE_CACHE):
        age_h = (time.time() - os.path.getmtime(PIPELINE_CACHE)) / 3600
        if age_h < CACHE_TTL_H:
            try:
                with open(PIPELINE_CACHE, "r") as f:
                    data = json.load(f)
                if data:
                    return data, "Loaded from local cache (< 12h old)"
            except Exception:
                pass

    if not records:
        # Return simulated fallback results
        return _simulated_fallback(), "Simulated benchmark (no historical data fetched)"

    logger.info("Running full Random Forest pipeline on %d hourly records...", len(records))
    results = run_kasese_ml_pipeline(records)

    if results:
        os.makedirs("data", exist_ok=True)
        with open(PIPELINE_CACHE, "w") as f:
            json.dump(results, f, indent=2)
        return results, f"Trained on {len(records)} historical hours"
    else:
        return _simulated_fallback(), "Simulated benchmark (pipeline returned empty)"


def _simulated_fallback() -> List[Dict]:
    """Realistic simulated metrics when real data is unavailable."""
    base = {
        "city": "Kasese, Uganda",
        "source": "Random Forest — Simulated Benchmark",
        "is_simulated": True,
        "model": "Random Forest (sklearn)",
        "threshold_mm": 1.0,
        "train_test_split": "chronological_80_20",
    }
    return [
        {**base, "lead_h": 6,  "n": 432, "hits": 98,  "misses": 27, "false_alarms": 21, "correct_negatives": 286, "accuracy": 0.8889, "hit_rate": 0.7840, "false_alarm_ratio": 0.1765, "critical_success_index": 0.6712, "mae_mm": 1.32},
        {**base, "lead_h": 24, "n": 432, "hits": 74,  "misses": 51, "false_alarms": 38, "correct_negatives": 269, "accuracy": 0.7940, "hit_rate": 0.5920, "false_alarm_ratio": 0.3390, "critical_success_index": 0.4540, "mae_mm": 2.87},
    ]
