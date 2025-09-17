# End-to-end test: runs the entire pipeline on the real CSV
# This checks integration of io.py, transform.py, and model.py together.

from gold_analysis.io import load_csv
from gold_analysis.transform import add_returns, select_top_abs_slv
from gold_analysis.model import fit_ols_gld_on_slv

def test_e2e_repo_csv():
    # Load the actual project CSV
    df = load_csv("gold_data_2015_25.csv")

    # Add percentage returns
    df_r = add_returns(df)

    # Select the biggest 10% SLV moves
    top, thr = select_top_abs_slv(df_r, 0.9)

    # Fit regression on full returns dataset
    fit = fit_ols_gld_on_slv(df_r)

    # Assertions: dataset not empty, big moves selected, regression valid
    assert len(df_r) > 0
    assert len(top) > 0
    assert 0 <= fit["r2"] <= 1
