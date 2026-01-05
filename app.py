from __future__ import annotations

import json
import os
import uuid
from pathlib import Path

import streamlit as st
from PIL import Image

from config import AppConfig
from models import ReceiptInput
from pipeline import run_ocr, extract_fields, confirm_and_write
from src.transform.enrich import enrich_selection
from src.output.to_xlsx import ensure_workbook

cfg = AppConfig()

st.set_page_config(page_title="Receipt → Spreadsheet", page_icon="🧾", layout="centered")

def load_json(path: Path) -> dict:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))

def list_demo_receipts(demo_dir: Path) -> list[Path]:
    if not demo_dir.exists():
        return []
    return sorted([p for p in demo_dir.iterdir() if p.suffix.lower() in [".jpg", ".jpeg", ".png"]])

def read_demo_ocr(cache_dir: Path, image_path: Path) -> str | None:
    txt = cache_dir / f"{image_path.stem}.txt"
    return txt.read_text(encoding="utf-8") if txt.exists() else None

def save_uploaded_file(uploaded_file) -> Path:
    tmp_dir = Path("tmp_uploads")
    tmp_dir.mkdir(exist_ok=True)
    ext = Path(uploaded_file.name).suffix or ".jpg"
    file_id = uuid.uuid4().hex
    path = tmp_dir / f"{file_id}{ext}"
    path.write_bytes(uploaded_file.getbuffer())
    return path

# --- Header
st.title("🧾 Receipt → Spreadsheet")
st.caption("Upload a receipt, review extracted fields, select property/category, and confirm to append a row to Excel.")

# --- Demo mode (default ON in Hugging Face)
# Hugging Face sets SPACE_ID; use that as a hint.
is_hf = bool(os.getenv("SPACE_ID"))
default_demo = True if is_hf else False
demo_mode = st.toggle("Demo Mode (recommended for public demos)", value=default_demo)

# Ensure spreadsheet exists
ensure_workbook(cfg.spreadsheet_path, cfg.columns)

# Load properties/categories
props = load_json(cfg.properties_path).get("properties", [])
cats = load_json(cfg.categories_path).get("categories", [])

prop_names = [p.get("name", "Unknown") for p in props] if props else ["(Add properties.json)"]
cat_names = [c.get("name", "Unknown") for c in cats] if cats else ["(Add categories.json)"]
cat_to_schedule = {c.get("name", ""): c.get("schedule_e_line", "") for c in cats} if cats else {}

# --- Receipt selection
st.subheader("1) Add a receipt")

selected_demo_path: Path | None = None
demo_text: str | None = None

if demo_mode:
    demo_receipts = list_demo_receipts(cfg.demo_receipts_dir)
    if demo_receipts:
        labels = [p.name for p in demo_receipts]
        choice = st.selectbox("Choose a sample receipt", labels)
        selected_demo_path = cfg.demo_receipts_dir / choice
        demo_text = read_demo_ocr(cfg.demo_ocr_cache_dir, selected_demo_path)
        if demo_text is None:
            st.warning("No cached OCR text found for this sample. Add a matching .txt in demo/ocr_cache/.")
    else:
        st.info("No demo receipts found. Add images to demo/receipts/ and OCR text files to demo/ocr_cache/.")

    image_path = selected_demo_path
else:
    uploaded = st.file_uploader("Upload a receipt image (jpg/png)", type=["jpg", "jpeg", "png"])
    image_path = save_uploaded_file(uploaded) if uploaded else None

if image_path:
    st.image(Image.open(image_path), caption=f"Receipt: {Path(image_path).name}", use_container_width=True)

    # Create ReceiptInput
    receipt_in = ReceiptInput(
        image_path=Path(image_path),
        image_id=uuid.uuid4().hex,
        original_filename=Path(image_path).name,
    )

    # --- OCR + Extract
    with st.spinner("Running OCR + extracting fields..."):
        ocr = run_ocr(cfg, receipt_in, demo_text=demo_text)
        parsed = extract_fields(ocr)

    st.subheader("2) Review extracted fields")

    col1, col2 = st.columns(2)
    with col1:
        vendor = st.text_input("Vendor", value=parsed.vendor or "")
        date = st.text_input("Date (YYYY-MM-DD)", value=parsed.date or "")
        payment = st.text_input("Payment Method (optional)", value=parsed.payment_method or "")
    with col2:
        total = st.number_input("Total", value=float(parsed.total) if parsed.total is not None else 0.0, step=0.01, format="%.2f")
        tax = st.number_input("Tax (optional)", value=float(parsed.tax) if parsed.tax is not None else 0.0, step=0.01, format="%.2f")
        st.caption(f"OCR engine: **{ocr.engine}** | confidence: **{ocr.confidence if ocr.confidence is not None else '—'}**")

    with st.expander("Show raw OCR text"):
        st.text(ocr.raw_text[:4000] + ("..." if len(ocr.raw_text) > 4000 else ""))

    # Push edits back into parsed
    parsed.vendor = vendor.strip()
    parsed.date = date.strip()
    parsed.total = float(total) if total is not None else None
    parsed.tax = float(tax) if tax is not None else None
    parsed.payment_method = payment.strip()

    st.subheader("3) Categorize + Confirm")

    property_name = st.selectbox("Property", prop_names)
    category_name = st.selectbox("Category", cat_names)
    schedule_line = cat_to_schedule.get(category_name, "")
    schedule_e_line = st.text_input("Schedule E line (auto)", value=schedule_line)
    notes = st.text_area("Notes (optional)", value="")

    enriched = enrich_selection(property_name, category_name, schedule_e_line, notes)

    if st.button("✅ Confirm and append to spreadsheet", type="primary"):
        path = confirm_and_write(cfg, receipt_in, ocr, parsed, enriched)
        st.success("Saved! Row appended and image stored.")

    st.divider()
    st.subheader("4) Download")
    if cfg.spreadsheet_path.exists():
        data = cfg.spreadsheet_path.read_bytes()
        st.download_button(
            label="⬇️ Download expenses.xlsx",
            data=data,
            file_name="expenses.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )
else:
    st.info("Upload a receipt (or choose a sample in Demo Mode) to start.")
