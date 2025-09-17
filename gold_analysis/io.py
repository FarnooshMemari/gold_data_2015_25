from pathlib import Path
import pandas as pd

# Expected columns in the raw CSV
REQUIRED_COLS = {"Date", "GLD", "SLV"}

def load_csv(path: str | Path) -> pd.DataFrame:
    """
    Load the gold/silver dataset from a CSV file.
    - Checks that file exists.
    - Checks that required columns are present.
    - Converts 'Date' to datetime.
    - Sorts rows by date.
    """
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(p)

    df = pd.read_csv(p)

    # Verify required columns exist
    missing = REQUIRED_COLS - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")

    # Ensure Date column is proper datetime
    df = df.copy()
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    if df["Date"].isna().any():
        # If any unparseable dates exist → stop
        raise ValueError("Unparseable dates detected")

    # Return sorted by Date for consistency
    return df.sort_values("Date").reset_index(drop=True)
