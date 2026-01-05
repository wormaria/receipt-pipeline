# 🧾 receipt → spreadsheet

a tiny demo app for turning messy paper receipts into clean, categorized spreadsheet rows.

built for my dad’s rental property business.  
also built to explore what “good” data pipelines look like when humans are actually part of the loop.

---
## 🚀 live demo

try it here:  
https://your-app-name.streamlit.app

note: the public demo runs in demo mode using sample data only.
no real financial or personal information is stored or transmitted.

---

## what this is

small rental property owners usually manage expenses with:
- piles of paper receipts
- manual data entry
- inconsistent categories
- lots of stress when tax season hits

this app turns that chaos into something calm:

upload a receipt → review the extracted fields → pick a property + category → confirm → done.  
a new row gets appended to an excel sheet, and the receipt image is saved for audit.

fast. simple. tax-ready.

---

## how it works (high level)

receipt image  
→ ocr (easyocr)  
→ field extraction (vendor, date, total, tax, etc.)  
→ user review + correction  
→ property & category enrichment  
→ append row to excel spreadsheet  
→ store receipt image for audit

the pipeline is fully modular:

src/ocr/        # ocr engine  
src/extract/    # structured field parsing  
src/transform/  # normalization + enrichment  
src/output/     # excel + image persistence  
pipeline.py     # orchestration layer  

everything is designed so pieces can be swapped out later (better ocr, different output format, database storage, etc).

---

## demo mode

the public demo runs in demo mode so recruiters (and friends) can play with it safely.

demo mode:
- uses sample receipts in demo/receipts/
- loads cached ocr results from demo/ocr_cache/
- avoids external ocr dependencies
- stays fast, stable, and reproducible

no real financial or personal data is stored or transmitted in the demo.

local usage supports full ocr and persistent storage.

---

## why i built this

i wanted to build something that feels:
- useful
- trustworthy
- human

a lot of data pipelines optimize for speed or automation alone.  
this one intentionally includes a human-in-the-loop step, because financial data needs context, judgment, and accountability.

also, my dad had a box of receipts on his kitchen table and i thought, “we can do better than this.”

---

## current status

this is a working prototype and ongoing project.  
the core pipeline is complete and functional. next steps include:

- supporting additional output formats (csv, database)
- adding multi-user support
- improving receipt field extraction robustness
- introducing basic analytics + summaries on the expense data

---

## tech stack

- python  
- streamlit  
- easyocr  
- pandas + openpyxl  
- pillow  

---

to run locally:

streamlit run app.py
