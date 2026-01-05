from __future__ import annotations
from pathlib import Path
from typing import Tuple, Optional

import easyocr

# Cache the reader across calls (important for performance)
_READER: Optional[easyocr.Reader] = None

def _get_reader() -> easyocr.Reader:
    global _READER
    if _READER is None:
        # English only for receipts; add languages if needed.
        _READER = easyocr.Reader(["en"], gpu=False)
    return _READER

def run_easyocr(image_path: Path) -> Tuple[str, Optional[float]]:
    """
    Returns (raw_text, confidence).
    Confidence is a rough average of EasyOCR line confidences.
    """
    reader = _get_reader()
    results = reader.readtext(str(image_path))
    if not results:
        return "", None

    texts = []
    confs = []
    for bbox, text, conf in results:
        if text:
            texts.append(text)
        if conf is not None:
            confs.append(float(conf))

    raw_text = "\n".join(texts).strip()
    avg_conf = sum(confs) / len(confs) if confs else None
    return raw_text, avg_conf
