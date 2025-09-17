import numpy as np
import pandas as pd

def add_returns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Compute daily percentage returns for GLD and SLV.
    - Uses pct_change() which introduces a NaN in the first row.
    - Drops the first row (no extra imputations).
    """
    out = df.copy()
    out["GLD_pct"] = out["GLD"].pct_change()
    out["SLV_pct"] = out["SLV"].pct_change()

    # Drop first row with NaNs created by pct_change
    return out.dropna(subset=["GLD_pct", "SLV_pct"]).reset_index(drop=True)

def select_top_abs_slv(df: pd.DataFrame, quantile: float = 0.9) -> tuple[pd.DataFrame, float]:
    """
    Filter rows where the absolute SLV return is in the top quantile.
    - quantile = 0.9 → keep the biggest 10% absolute SLV moves.
    - Returns (filtered_dataframe, threshold_value).
    """
    if not 0 < quantile < 1:
        raise ValueError("quantile must be between 0 and 1")

    thr = np.quantile(np.abs(df["SLV_pct"]), quantile)
    top = df[np.abs(df["SLV_pct"]) >= thr].reset_index(drop=True)
    return top, float(thr)
