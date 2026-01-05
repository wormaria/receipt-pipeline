from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Any

@dataclass
class ReceiptInput:
    image_path: Path
    image_id: str  # uuid string
    original_filename: str

@dataclass
class ReceiptOCR:
    raw_text: str
    confidence: Optional[float] = None  # 0..1, may be None
    engine: str = "easyocr"

@dataclass
class ReceiptParsed:
    vendor: str = ""
    date: str = ""   # ISO: YYYY-MM-DD preferred
    total: Optional[float] = None
    tax: Optional[float] = None
    payment_method: str = ""
    # Optional per-field confidence signals
    meta: Dict[str, Any] = field(default_factory=dict)

@dataclass
class ReceiptEnriched:
    property_name: str
    category_name: str
    schedule_e_line: str = ""
    notes: str = ""

@dataclass
class ReceiptRecord:
    logged_at: datetime
    receipt_date: str
    vendor: str
    total: Optional[float]
    tax: Optional[float]
    category: str
    schedule_e_line: str
    property: str
    payment_method: str
    notes: str
    image_path: str
    ocr_confidence: Optional[float]
