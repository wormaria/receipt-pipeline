---
title: Receipt to Spreadsheet
emoji: 🧾
colorFrom: indigo
colorTo: green
sdk: streamlit
app_file: app.py
pinned: false
---

# 🧾 Receipt → Spreadsheet  
**Automated expense logging for small rental property owners**

This app converts receipt photos into clean, categorized spreadsheet entries using OCR, structured extraction, and a human-in-the-loop confirmation step.

Built for my dad’s rental property business — and designed to demonstrate production-grade data pipelines.

---

## 🚀 Live Demo
> *(Add Hugging Face Space link here once deployed)*

---

## 🧠 Problem

Small rental owners track expenses with:
- piles of paper receipts  
- manual data entry  
- inconsistent categorization  
- high audit risk  

Tax season becomes error-prone and painful.

---

## 💡 Solution

Upload a receipt → review extracted fields → select property & category → confirm → row is appended to a spreadsheet and receipt image is archived for audit.

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

### Pipeline modules

- `src/ocr/` — OCR engine
- `src/extract/` — structured field parsing
- `src/transform/` — enrichment & normalization
- `src/output/` — Excel + image persistence
- `pipeline.py` — orchestration

---

## 🧪 Demo Mode

For public demos (e.g. recruiters), the app runs in **Demo Mode**:
- uses sample receipts in `demo/receipts/`
- loads cached OCR from `demo/ocr_cache/`
- avoids external OCR dependencies
- stays fast, stable, and reproducible

Local usage supports real OCR and persistent storage.

---

## 🖥️ Run Locally

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
`