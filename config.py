from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

@dataclass(frozen=True)
class AppConfig:
    # Data/config files
    properties_path: Path = BASE_DIR / "data" / "properties.json"
    categories_path: Path = BASE_DIR / "data" / "categories.json"

    # Outputs
    exports_dir: Path = BASE_DIR / "data" / "exports"
    spreadsheet_path: Path = BASE_DIR / "data" / "exports" / "expenses.xlsx"
    receipt_images_dir: Path = BASE_DIR / "data" / "receipt_images"

    # Demo assets
    demo_receipts_dir: Path = BASE_DIR / "demo" / "receipts"
    demo_ocr_cache_dir: Path = BASE_DIR / "demo" / "ocr_cache"

    # Spreadsheet columns (stable contract!)
    columns: tuple[str, ...] = (
        "Logged At",
        "Receipt Date",
        "Vendor",
        "Total",
        "Tax",
        "Category",
        "Schedule E Line",
        "Property",
        "Payment Method",
        "Notes",
        "Image Path",
        "OCR Confidence",
    )
