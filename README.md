# 🌦️ RainCheck — Weather Verification & Actionable Advice

> **Hackathon Project:** Climate-Change-Kasese  
> **Pilot Cities:** Kampala, Uganda & Pilot Pakistani City (e.g., Lahore)  
> **Target Personas:** Farmers, Riders (Boda-Boda/Couriers), Market Traders  
> **Module Owner:** Sobia (Advice, Languages & Web App)

---

## 📌 Project Overview
**RainCheck** is an evidence-grounded weather advice web application designed to help vulnerable daily earners (farmers, motorcycle riders, and open-air traders) make informed operational decisions based on verified forecast accuracy rather than blind faith or generic forecasts.

### Core Philosophy
1. **Evidence-Grounded**: Advice is directly tied to historical verification metrics (hit rate, false alarm ratio, mean absolute error).
2. **Numeric Safety Guard**: Prohibits hallucination. The system automatically inspects any AI-generated response and rejects unverified numbers or fake probabilities, instantly defaulting to a safe, deterministic template.
3. **Works Without Paid APIs**: 100% operational offline using rule-based deterministic fallback templates.
4. **Data Isolation**: Crowdsourced community feedback is strictly isolated from scientific forecast records and verification metrics.
5. **Academic & Ethical Transparency**: Clearly disclaims official warning status and tags non-reviewed translations until verified by fluent speakers.

---

## 🏗️ Architecture & Project Structure

```text
NYLP HACKATHON/
│
├── app.py                   # Streamlit interactive multi-page web application
├── weather_service.py       # Live Country Weather API integration (Open-Meteo WMO / National Models)
├── advice.py                # Advice generation engine, deterministic fallbacks & numeric safety guard
├── translations.py          # Multilingual dictionary (English, Urdu, Luganda) & review metadata
│
├── data/
│   ├── results.json         # Verification metrics from teammates (clearly labeled SIMULATED for demo)
│   └── feedback.json        # Community ground-truth observations (isolated from verification data)
│
├── tests/
│   └── test_advice.py       # Automated unit tests for advice guard, fallbacks & edge cases
│
├── requirements.txt         # Python package dependencies
├── .gitignore               # Ignores temp files, virtual environments, and secrets
└── README.md                # Project documentation and guide
```

### Purpose of Each File (Beginner-Friendly Guide)

| File | Purpose |
| :--- | :--- |
| **[app.py](file:///c:/Users/Sobia/Downloads/NYLP%20HACKATHON/app.py)** | The main web dashboard built with Streamlit. Orchestrates pages (**Evidence**, **Advice**, **Feedback**) with sleek animations, interactive Plotly gauges, and live weather ribbons. |
| **[weather_service.py](file:///c:/Users/Sobia/Downloads/NYLP%20HACKATHON/weather_service.py)** | Fetches real-time country-level weather from Open-Meteo for Uganda (Kampala) and Pakistan (Lahore, Karachi, Islamabad) with WMO code translation and offline caching. |
| **[advice.py](file:///c:/Users/Sobia/Downloads/NYLP%20HACKATHON/advice.py)** | Pure Python module containing the business logic. Classifies weather evidence, validates LLM responses with a **regex-based Numeric Safety Guard**, and provides offline deterministic templates. |
| **[translations.py](file:///c:/Users/Sobia/Downloads/NYLP%20HACKATHON/translations.py)** | Keeps UI text and fallback templates organized in English, Urdu, and Luganda. Holds metadata on whether a translation is verified or pending fluent speaker review. |
| **[data/results.json](file:///c:/Users/Sobia/Downloads/NYLP%20HACKATHON/data/results.json)** | Standardized integration contract for verification teammate (`city`, `source`, `lead_h`, `n`, `hits`, `misses`, `false_alarms`, `correct_negatives`, `hit_rate`, `false_alarm_ratio`, `mae_mm`). |
| **[data/feedback.json](file:///c:/Users/Sobia/Downloads/NYLP%20HACKATHON/data/feedback.json)** | JSON storage for crowd observations. Writes are isolated so community feedback never alters scientific metrics. |
| **[tests/test_advice.py](file:///c:/Users/Sobia/Downloads/NYLP%20HACKATHON/tests/test_advice.py)** | Pytest test suite demonstrating safety compliance: rejecting hallucinated rainfall numbers, testing live weather validation, testing small-sample flags ($N < 30$), and offline fallbacks. |

---

## 🚀 Setup & Execution Guide (Windows)

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
Verify safety guards and fallbacks:
```powershell
python -m pytest tests/test_advice.py
```
*Expected: 8 passed tests.*

### 5. Launch the Web Application
```powershell
streamlit run app.py
```
The browser will open automatically at `http://localhost:8501`.

---

## 🛡️ The Numeric Safety Guard: How it Works

Large Language Models (LLMs) frequently hallucinate numbers (e.g. inventing *"90% chance of 45mm rain"* when no such forecast exists). In RainCheck:

1. **Whitelist Extraction**: The guard parses the selected record from `results.json` and extracts every valid number (`lead_h`, `n`, `hit_rate`, `false_alarm_ratio`, `mae_mm`, etc.).
2. **LLM Output Scanning**: All numbers in the LLM response are extracted using regular expressions.
3. **Verification**: If any number in the generated advice is **not** on the whitelist, the output is rejected.
4. **Deterministic Fallback**: The system safely returns an offline, human-crafted template tailored to the persona and historical weather pattern.

---

## 🤝 Team Integration Guide

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

## ⚖️ Disclaimers & Ethics
- **Not an Official Warning Service**: RainCheck is an academic decision-support prototype. For emergency flood or storm warnings, always consult official national bodies: [Uganda National Meteorological Authority (UNMA)](https://www.unma.go.ug/) or [Pakistan Meteorological Department (PMD)](https://www.pmd.gov.pk/).
- **Translation Status**: Urdu and Luganda strings are machine translations marked as *pending review by fluent speakers*.
>>>>>>> 23b8ab2 (feat: RainCheck weather verification advice engine, multilingual support, live country API, and webapp)
