from __future__ import annotations
import re
from dataclasses import asdict
from datetime import datetime
from typing import Optional, Tuple

from dateutil import parser as dateparser

from models import ReceiptParsed

_MONEY_RE = re.compile(r"(?<!\d)(\d{1,3}(?:[,\s]\d{3})*(?:\.\d{2})|\d+\.\d{2})(?!\d)")
_DATE_HINTS = ["date", "dated", "transaction", "purchase"]

def _to_float(money_str: str) -> Optional[float]:
    try:
        cleaned = money_str.replace(",", "").replace(" ", "")
        return float(cleaned)
    except Exception:
        return None

def _find_total(text: str) -> Optional[float]:
    """
    Heuristic: look for lines containing TOTAL/AMOUNT and grab the last money-like number.
    Fallback: take the largest money-like number in the text.
    """
    lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
    candidates = []

    for ln in lines:
        upper = ln.upper()
        if any(k in upper for k in ["TOTAL", "AMOUNT", "BALANCE DUE", "GRAND TOTAL"]):
            nums = _MONEY_RE.findall(ln)
            for n in nums:
                val = _to_float(n)
                if val is not None:
                    candidates.append(val)

    if candidates:
        return candidates[-1]

    # fallback: largest value
    all_nums = _MONEY_RE.findall(text)
    vals = [_to_float(n) for n in all_nums]
    vals = [v for v in vals if v is not None]
    return max(vals) if vals else None

def _find_tax(text: str) -> Optional[float]:
    lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
    for ln in lines:
        upper = ln.upper()
        if "TAX" in upper:
            nums = _MONEY_RE.findall(ln)
            if nums:
                val = _to_float(nums[-1])
                if val is not None:
                    return val
    return None

def _find_vendor(text: str) -> str:
    """
    Simple heuristic: vendor tends to be first non-empty line, stripped of noise.
    """
    lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
    if not lines:
        return ""
    vendor = lines[0]
    vendor = re.sub(r"[^A-Za-z0-9&\-\.\s]", "", vendor).strip()
    return vendor[:60]

def _find_date(text: str) -> str:
    """
    Try to parse a date from text. Returns ISO date string or "".
    """
    # First pass: search for patterns like 01/05/2026 or 2026-01-05
    date_patterns = [
        r"\b\d{1,2}/\d{1,2}/\d{2,4}\b",
        r"\b\d{4}-\d{1,2}-\d{1,2}\b",
        r"\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Sept|Oct|Nov|Dec)[a-z]*\s+\d{1,2},?\s+\d{2,4}\b",
    ]
    for pat in date_patterns:
        m = re.search(pat, text, flags=re.IGNORECASE)
        if m:
            try:
                dt = dateparser.parse(m.group(0), fuzzy=True)
                if dt:
                    return dt.date().isoformat()
            except Exception:
                pass

    # Second pass: look for lines with date hints
    lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
    for ln in lines:
        upper = ln.lower()
        if any(h in upper for h in _DATE_HINTS):
            try:
                dt = dateparser.parse(ln, fuzzy=True)
                if dt:
                    return dt.date().isoformat()
            except Exception:
                continue

    return ""

def parse_receipt_fields(raw_text: str) -> ReceiptParsed:
    parsed = ReceiptParsed()
    parsed.vendor = _find_vendor(raw_text)
    parsed.date = _find_date(raw_text)
    parsed.total = _find_total(raw_text)
    parsed.tax = _find_tax(raw_text)
    parsed.meta = {
        "extraction_version": "v1-heuristic",
    }
    return parsed
