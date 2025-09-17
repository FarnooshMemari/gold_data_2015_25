# Tests for regression fitting (model.py)

import numpy as np
import pandas as pd
import pytest
from gold_analysis.model import fit_ols_gld_on_slv

def test_fit_ok():
    # Case: Normal dataset with correlation between SLV and GLD
    rng = np.random.default_rng(0)
    slv = rng.normal(size=200)
    gld = 0.4*slv + rng.normal(scale=0.5, size=200)

    df = pd.DataFrame({"SLV_pct": slv, "GLD_pct": gld})
    out = fit_ols_gld_on_slv(df)

    # Verify outputs make sense
    assert 0 <= out["r2"] <= 1         # R² is valid
    assert "slope" in out              # slope returned
    assert "intercept" in out          # intercept returned

def test_fit_raises_on_empty():
    # Case: Regression with empty dataset → should raise ValueError
    df = pd.DataFrame({"SLV_pct": [], "GLD_pct": []})
    with pytest.raises(ValueError):
        fit_ols_gld_on_slv(df)
