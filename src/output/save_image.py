from __future__ import annotations
from pathlib import Path
import shutil

def save_receipt_image(src_path: Path, dest_dir: Path, image_id: str) -> Path:
    dest_dir.mkdir(parents=True, exist_ok=True)
    suffix = src_path.suffix.lower() if src_path.suffix else ".jpg"
    dest_path = dest_dir / f"{image_id}{suffix}"
    shutil.copy2(src_path, dest_path)
    return dest_path
