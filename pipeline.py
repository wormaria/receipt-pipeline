from __future__ import annotations
from datetime import datetime
from pathlib import Path

from config import AppConfig
from models import ReceiptInput, ReceiptOCR, ReceiptParsed, ReceiptEnriched, ReceiptRecord
from src.ocr.easyocr_engine import run_easyocr
from src.extract.parse_receipt import parse_receipt_fields
from src.output.save_image import save_receipt_image
from src.output.to_xlsx import append_row

def run_ocr(cfg: AppConfig, receipt_in: ReceiptInput, demo_text: str | None = None) -> ReceiptOCR:
    if demo_text is not None:
        return ReceiptOCR(raw_text=demo_text, confidence=0.99, engine="demo-cache")

    raw_text, conf = run_easyocr(receipt_in.image_path)
    return ReceiptOCR(raw_text=raw_text, confidence=conf, engine="easyocr")

def extract_fields(ocr: ReceiptOCR) -> ReceiptParsed:
    return parse_receipt_fields(ocr.raw_text)

def confirm_and_write(
    cfg: AppConfig,
    receipt_in: ReceiptInput,
    ocr: ReceiptOCR,
    parsed: ReceiptParsed,
    enriched: ReceiptEnriched,
) -> Path:
    saved_image_path = save_receipt_image(receipt_in.image_path, cfg.receipt_images_dir, receipt_in.image_id)

    record = ReceiptRecord(
        logged_at=datetime.now(),
        receipt_date=parsed.date,
        vendor=parsed.vendor,
        total=parsed.total,
        tax=parsed.tax,
        category=enriched.category_name,
        schedule_e_line=enriched.schedule_e_line,
        property=enriched.property_name,
        payment_method=parsed.payment_method,
        notes=enriched.notes,
        image_path=str(saved_image_path.relative_to(cfg.receipt_images_dir.parent)),
        ocr_confidence=ocr.confidence,
    )

    row = {
        "Logged At": record.logged_at.isoformat(timespec="seconds"),
        "Receipt Date": record.receipt_date,
        "Vendor": record.vendor,
        "Total": record.total,
        "Tax": record.tax,
        "Category": record.category,
        "Schedule E Line": record.schedule_e_line,
        "Property": record.property,
        "Payment Method": record.payment_method,
        "Notes": record.notes,
        "Image Path": record.image_path,
        "OCR Confidence": record.ocr_confidence,
    }

    append_row(cfg.spreadsheet_path, cfg.columns, row)
    return cfg.spreadsheet_path
