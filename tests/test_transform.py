# Tests for transformation functions (transform.py)

import pandas as pd
import pytest
from gold_analysis.transform import add_returns, select_top_abs_slv

# Helper: make a small fake dataset for testing
def _df():
    return pd.DataFrame({
        "Date": pd.date_range("2024-01-01", periods=6, freq="D"),
        "GLD": [100,101,100,102,101,103],
        "SLV": [50,49,50,52,51,53],
    })

def test_add_returns_drops_initial_na():
    # Case: After computing pct_change, the first row should be dropped (NaN)
    df = add_returns(_df())

    # Verify new columns are created
    assert {"GLD_pct","SLV_pct"} <= set(df.columns)

    # There should be 5 rows left (original 6 – 1 dropped)
    assert len(df) == 5

def test_select_top_abs_slv_quantile_and_threshold():
    # Case: Filter top 10% absolute SLV moves
    df = add_returns(_df())
    top, thr = select_top_abs_slv(df, 0.9)

    # Threshold should be numeric, and at least one row should be selected
    assert isinstance(thr, float)
    assert len(top) >= 1

def test_select_top_abs_slv_bounds():
    # Case: Quantile outside (0,1) → should raise ValueError
    df = add_returns(_df())
    with pytest.raises(ValueError): select_top_abs_slv(df, 0)
    with pytest.raises(ValueError): select_top_abs_slv(df, 1)
