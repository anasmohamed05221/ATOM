"""Cut the 31 GB Expedia dataset down to about 3% of flights.

Why: the full file does not fit in memory (16 GB RAM). We keep whole flights
(every row of a chosen legId), so each flight keeps its full price history.

How a flight is chosen: legId is a random-looking hex code. We turn its first
8 characters into a number, take the remainder after dividing by 100 (0-99),
and keep the flight if that number is below SAMPLE_PERCENT. The same flights
are chosen every time, so the result is reproducible.

Run from the project root:  uv run python scripts/make_sample.py
"""

import zipfile
from pathlib import Path

import pandas as pd

ZIP_PATH = Path("data/raw/flightprices.zip")
CSV_NAME = "itineraries.csv"
OUT_PATH = Path("data/processed/flights_sample_3pct.parquet")
SAMPLE_PERCENT = 3          # keep flights whose bucket is 0, 1 or 2 (out of 0-99)
CHUNK_ROWS = 1_000_000      # read the file one million rows at a time


def flight_bucket(leg_ids: pd.Series) -> pd.Series:
    """Map each legId to a fixed number from 0 to 99."""
    return leg_ids.str[:8].apply(lambda h: int(h, 16) % 100)


def main() -> None:
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    kept_chunks = []
    rows_read = 0

    with zipfile.ZipFile(ZIP_PATH) as zf, zf.open(CSV_NAME) as f:
        for chunk in pd.read_csv(f, chunksize=CHUNK_ROWS):
            rows_read += len(chunk)
            keep = flight_bucket(chunk["legId"]) < SAMPLE_PERCENT
            kept_chunks.append(chunk[keep])
            print(f"read {rows_read:,} rows, kept {sum(len(c) for c in kept_chunks):,}", flush=True)

    sample = pd.concat(kept_chunks, ignore_index=True)
    sample.to_parquet(OUT_PATH, index=False)

    print("\nDone.")
    print(f"Total rows in full dataset: {rows_read:,}")
    print(f"Rows kept: {len(sample):,} ({len(sample) / rows_read:.2%})")
    print(f"Flights kept: {sample['legId'].nunique():,}")
    print(f"Saved to {OUT_PATH}")


if __name__ == "__main__":
    main()
