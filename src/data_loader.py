"""
Person A: load raw dataset CSV, derive importance scores, return list[Record].
"""

import pandas as pd
from src.schema import Record


def load_telemetry(csv_path: str, value_col: str, id_col: str = None, z_threshold: float = 2.0) -> list:
    df = pd.read_csv(csv_path)

    # derive importance via z-score outlier detection
    mean, std = df[value_col].mean(), df[value_col].std()
    df["zscore"] = (df[value_col] - mean) / std
    df["importance"] = (df["zscore"].abs() / df["zscore"].abs().max()).clip(0, 1)

    records = []
    for i, row in df.iterrows():
        records.append(Record(
            id=str(row[id_col]) if id_col else str(i),
            timestamp=float(row["ts"]) if "ts" in df.columns else float(i),  # replace with real timestamp column if available
            value=float(row[value_col]),
            importance=float(row["importance"]),
        ))
    return records
