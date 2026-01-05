from __future__ import annotations
from pathlib import Path
from typing import Sequence

import pandas as pd

ENGINE = "openpyxl"

def ensure_workbook(path: Path, columns: Sequence[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)

    # If file exists but is empty/corrupted, rebuild it.
    if path.exists() and path.stat().st_size < 100:  # tiny file is almost certainly invalid
        path.unlink()

    if not path.exists():
        df = pd.DataFrame(columns=list(columns))
        df.to_excel(path, index=False, engine=ENGINE)

def append_row(path: Path, columns: Sequence[str], row: dict) -> None:
    ensure_workbook(path, columns)

    # Force engine to avoid pandas guessing issues
    df_existing = pd.read_excel(path, engine=ENGINE)

    # Ensure all columns exist even if schema evolves
    for c in columns:
        if c not in df_existing.columns:
            df_existing[c] = None

    df_new = pd.DataFrame([row])
    df_out = pd.concat([df_existing, df_new], ignore_index=True)

    # Keep stable column ordering
    df_out = df_out.reindex(columns=list(columns))
    df_out.to_excel(path, index=False, engine=ENGINE)