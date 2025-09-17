# Tests for the data loading functions (io.py)

import pandas as pd
import pytest
from gold_analysis.io import load_csv

def test_load_csv_happy_path(tmp_path):
    # Case: CSV has correct structure → should load without errors
    p = tmp_path/"d.csv"
    p.write_text("Date,GLD,SLV\n2024-01-01,100,50\n2024-01-02,101,51\n")
    df = load_csv(p)

    # Verify columns and parsed datetime
    assert list(df.columns)[:3] == ["Date","GLD","SLV"]
    assert df.Date.iloc[0].year == 2024

def test_load_csv_missing_cols(tmp_path):
    # Case: CSV missing the SLV column → should raise ValueError
    p = tmp_path/"m.csv"
    p.write_text("Date,GLD\n2024-01-01,100\n")

    with pytest.raises(ValueError):
        load_csv(p)

def test_load_csv_bad_date(tmp_path):
    # Case: Invalid date string in Date column → should raise ValueError
    p = tmp_path/"b.csv"
    p.write_text("Date,GLD,SLV\nNOTADATE,100,50\n")

    with pytest.raises(ValueError):
        load_csv(p)
