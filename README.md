# 🧾 Receipt → Spreadsheet  
**Automated expense logging for small rental property owners**

This app converts receipt photos into clean, categorized spreadsheet entries using OCR, structured extraction, and a human-in-the-loop confirmation step.

Built for my dad’s rental property business — and designed to demonstrate production-grade data pipelines and thoughtful product engineering.

---

## 🚀 Live Demo
**Try it here:**  
> https://your-app-name.streamlit.app


## ⚠️ Demo Disclaimer

This application is a functional prototype and portfolio demonstration.  
The public demo runs in **Demo Mode**, using sample data and cached OCR results to ensure fast, stable performance.

No real financial or personal data is stored or transmitted in the public demo.  
Local usage supports full receipt processing and persistent storage.


---

## 🧰 Tech Stack

**Core**
- Python
- Streamlit (UI)
- EasyOCR (optical character recognition)
- Pandas + OpenPyXL (spreadsheet output)
- Pillow (image handling)

**Design & Architecture**
- Modular pipeline design
- Human-in-the-loop validation
- Config-driven property & category mapping
- Audit-ready data storage

---

## 🧠 Problem

Small rental owners typically manage expenses with:
- piles of paper receipts  
- manual data entry  
- inconsistent categorization  
- high audit risk  

Tax season becomes error-prone, time-consuming, and stressful.

---

## 💡 Solution

Upload a receipt → review extracted fields → select property & category → confirm →  
a new row is appended to an Excel spreadsheet and the receipt image is archived for audit.

This keeps the process **fast, trustworthy, and tax-ready**.

---

## 🧱 Architecture

Receipt Image
↓
OCR (EasyOCR or cached demo OCR)
↓
Field Extraction (vendor, date, total, tax, etc.)
↓
User Review + Correction
↓
Property & Category Enrichment
↓
Append Row → Excel Spreadsheet
↓
Store Receipt Image for Audit


### Pipeline Modules

- `src/ocr/` — OCR engine
- `src/extract/` — structured field parsing
- `src/transform/` — enrichment & normalization
- `src/output/` — Excel + image persistence
- `pipeline.py` — orchestration layer

---

## 🧪 Demo Mode

For public demos (e.g. recruiters), the app runs in **Demo Mode**:
- uses sample receipts in `demo/receipts/`
- loads cached OCR from `demo/ocr_cache/`
- avoids external OCR dependencies
- remains fast, stable, and reproducible

Local usage supports full OCR processing and persistent storage.

---

## 🖥️ Run Locally

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py