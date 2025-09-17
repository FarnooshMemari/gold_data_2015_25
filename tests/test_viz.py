# tests/test_viz.py
# Purpose: sanity-check that the plotting helper saves a real PNG file.
# We DO NOT verify pixels or charts visually—just that a valid image is produced.

import pandas as pd
from gold_analysis.viz import scatter_with_fit

def test_scatter_with_fit_saves_png(tmp_path):
    # Minimal synthetic data for plotting
    df = pd.DataFrame({
        "SLV_pct": [-0.02, -0.01, 0.0, 0.01, 0.02],
        "GLD_pct": [-0.01, -0.005, 0.0, 0.006, 0.015],
    })
    # Minimal fit info (a simple slope/intercept pair)
    fit_info = {"slope": 0.7, "intercept": 0.0, "r2": 0.5, "model": None}

    # Save plot to a temp file inside pytest's tmp_path
    out_path = tmp_path / "plot.png"
    returned_path = scatter_with_fit(df, fit_info, path=str(out_path))

    # Assert the function returned the expected path
    assert str(out_path) == returned_path

    # Assert the file was created and is non-empty
    assert out_path.exists()
    assert out_path.stat().st_size > 0

    # Optional: quick PNG signature check (first 8 bytes of a PNG file)
    with open(out_path, "rb") as f:
        header = f.read(8)
    assert header == b"\x89PNG\r\n\x1a\n"
