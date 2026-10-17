# RainCheck — Weather Verification & Actionable Advice

> **Hackathon Project:** Climate-Change-Kasese  
> **Pilot Cities:** Kampala, Uganda & Pilot Pakistani City (e.g., Lahore)  
> **Target Personas:** Farmers, Riders (Boda-Boda/Couriers), Market Traders  
> **Lead Full-Stack & UI/UX Developer:** Sobia

---

## Project Overview
**RainCheck** is an evidence-grounded weather advice web application designed to help vulnerable daily earners (farmers, motorcycle riders, and open-air traders) make informed operational decisions based on verified forecast accuracy rather than blind faith or generic forecasts.

### Core Philosophy
1. **Evidence-Grounded**: Advice is directly tied to historical verification metrics (hit rate, false alarm ratio, mean absolute error).
2. **Numeric Safety Guard**: Prohibits hallucination. The system automatically inspects any AI-generated response and rejects unverified numbers or fake probabilities, instantly defaulting to a safe, deterministic template.
3. **Works Without Paid APIs**: 100% operational offline using rule-based deterministic fallback templates.
4. **Data Isolation**: Crowdsourced community feedback is strictly isolated from scientific forecast records and verification metrics.
5. **Academic & Ethical Transparency**: Clearly disclaims official warning status and tags non-reviewed translations until verified by fluent speakers.

---

## Architecture & Project Structure

```text
NYLP HACKATHON/
│
├── app.py                   # Dual-view web app (FloodSimple Landing Page + Operational Dashboard)
├── icons.py                 # Pure inline SVG icon system (zero emojis)
├── weather_service.py       # Live Country Weather API integration (Open-Meteo WMO / National Models)
├── forecast_logger.py       # Automated forecast ingestion, valid/issue time logging & lead-time filtering (>=6h)
├── verifier.py              # Scientific Forecast Verification Engine (2x2 contingency matrix, 1.0mm threshold)
├── advice.py                # Advice generation engine, deterministic fallbacks & numeric safety guard
├── translations.py          # Multilingual dictionary (English, Urdu, Luganda) & review metadata
│
├── data/
│   ├── results.json         # Standardized verification metrics contract (hits, misses, FAR, MAE)
│   ├── forecast_logs.json   # Archival storage of paired forecast and station valid-time records
│   └── feedback.json        # Community ground-truth observations (isolated from scientific metrics)
│
├── tests/
│   ├── test_advice.py       # Unit tests for safety guard, numeric anti-hallucination, and fallbacks
│   └── test_verifier.py     # Unit tests for 1.0mm rain threshold, contingency table, and MAE math
│
├── requirements.txt         # Python package dependencies
├── .gitignore               # Ignores temp files, virtual environments, and secrets
└── README.md                # Project documentation and guide
```

### Purpose of Each File (Beginner-Friendly Guide)

| File | Purpose |
| :--- | :--- |
| **[app.py](file:///c:/Users/Sobia/Downloads/NYLP%20HACKATHON/app.py)** | Dual-mode web platform: FloodSimple Insurtech public landing page + operational advisory & verification dashboard. |
| **[icons.py](file:///c:/Users/Sobia/Downloads/NYLP%20HACKATHON/icons.py)** | Professional inline SVG vector icon library (strict zero-emoji standard). |
| **[weather_service.py](file:///c:/Users/Sobia/Downloads/NYLP%20HACKATHON/weather_service.py)** | Real-time country-level weather from Open-Meteo for Uganda (Kampala) and Pakistan (Lahore, Karachi, Islamabad) with WMO code translation and offline caching. |
| **[forecast_logger.py](file:///c:/Users/Sobia/Downloads/NYLP%20HACKATHON/forecast_logger.py)** | Archives multi-hourly forecasts with explicit issue times, valid times, and filters forecasts for lead times $\ge 6\text{h}$. |
| **[verifier.py](file:///c:/Users/Sobia/Downloads/NYLP%20HACKATHON/verifier.py)** | The scientific verification engine computing $2\times 2$ contingency tables (Hits, Misses, False Alarms, Correct Negatives) at the agreed **$1.0\text{ mm}$ rain threshold**, Hit Rate (POD), False Alarm Ratio (FAR), and Mean Absolute Error (MAE). |
| **[advice.py](file:///c:/Users/Sobia/Downloads/NYLP%20HACKATHON/advice.py)** | Business logic module. Classifies weather evidence, validates LLM responses with a **regex-based Numeric Safety Guard**, and provides offline deterministic templates. |
| **[translations.py](file:///c:/Users/Sobia/Downloads/NYLP%20HACKATHON/translations.py)** | Keeps UI text and fallback templates organized in English, Urdu, and Luganda. Holds metadata on whether a translation is verified or pending fluent speaker review. |
| **[data/results.json](file:///c:/Users/Sobia/Downloads/NYLP%20HACKATHON/data/results.json)** | Standardized integration contract (`city`, `source`, `lead_h`, `n`, `hits`, `misses`, `false_alarms`, `correct_negatives`, `hit_rate`, `false_alarm_ratio`, `mae_mm`). |
| **[data/feedback.json](file:///c:/Users/Sobia/Downloads/NYLP%20HACKATHON/data/feedback.json)** | JSON storage for crowd observations. Writes are isolated so community feedback never alters scientific metrics. |
| **[tests/test_advice.py](file:///c:/Users/Sobia/Downloads/NYLP%20HACKATHON/tests/test_advice.py)** | Automated unit tests proving hallucinated rainfall numbers are rejected and offline templates operate reliably. |
| **[tests/test_verifier.py](file:///c:/Users/Sobia/Downloads/NYLP%20HACKATHON/tests/test_verifier.py)** | Automated unit tests proving that $1.0\text{ mm}$ threshold categorization, lead-time filters ($\ge 6\text{h}$), and contingency scoring math are correct. |

---

## Setup & Execution Guide (Windows)

### 1. Prerequisites
Ensure Python 3.9+ and Git are installed:
```powershell
python --version
git --version
```

### 2. Create and Activate Virtual Environment
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```
*(If PowerShell shows an execution policy error, run `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser` once.)*

### 3. Install Dependencies
```powershell
pip install -r requirements.txt
```

### 4. Run the Unit Tests
Verify safety guards, verifier math, contingency matrices, and fallbacks:
```powershell
python -m pytest
```
*Expected: 15 passed tests.*

### 5. Launch the Web Application
```powershell
streamlit run app.py
```
The browser will open automatically at `http://localhost:8501`.

---

## The Numeric Safety Guard: How it Works

Large Language Models (LLMs) frequently hallucinate numbers (e.g. inventing *"90% chance of 45mm rain"* when no such forecast exists). In RainCheck:

1. **Whitelist Extraction**: The guard parses the selected record from `results.json` and extracts every valid number (`lead_h`, `n`, `hit_rate`, `false_alarm_ratio`, `mae_mm`, etc.).
2. **LLM Output Scanning**: All numbers in the LLM response are extracted using regular expressions.
3. **Verification**: If any number in the generated advice is **not** on the whitelist, the output is rejected.
4. **Deterministic Fallback**: The system safely returns an offline, human-crafted template tailored to the persona and historical weather pattern.

---

## Team Integration Guide

- **For the Verification Teammate**: Output your evaluation pipeline into `data/results.json` following the schema below:
  ```json
  {
    "city": "Kampala, Uganda",
    "source": "Open-Meteo (ECMWF IFS)",
    "lead_h": 24,
    "n": 60,
    "hits": 18,
    "misses": 7,
    "false_alarms": 8,
    "correct_negatives": 27,
    "hit_rate": 0.72,
    "false_alarm_ratio": 0.31,
    "mae_mm": 2.8,
    "is_simulated": false
  }
  ```
- **For the Data Engineer**: Deploy `app.py` directly using Streamlit Community Cloud or Docker. No mandatory external API keys are required for the application to function.

---

## Disclaimers & Ethics
- **Not an Official Warning Service**: RainCheck is an academic decision-support prototype. For emergency flood or storm warnings, always consult official national bodies: [Uganda National Meteorological Authority (UNMA)](https://www.unma.go.ug/) or [Pakistan Meteorological Department (PMD)](https://www.pmd.gov.pk/).
- **Translation Status**: Urdu and Luganda strings are machine translations marked as *pending review by fluent speakers*.
