from __future__ import annotations
from models import ReceiptEnriched

def enrich_selection(property_name: str, category_name: str, schedule_e_line: str, notes: str) -> ReceiptEnriched:
    return ReceiptEnriched(
        property_name=property_name,
        category_name=category_name,
        schedule_e_line=schedule_e_line,
        notes=notes,
    )
