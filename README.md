# Gold vs Silver — Linear Relationship 

## Overview
This mini–data-engineering project analyzes how **gold (GLD)** and **silver (SLV)** move together. It follows the assignment workflow end-to-end:

- import the dataset
- inspect and validate data quality
- create meaningful subsets (filtering)
- summarize with `groupby`
- run a simple **linear regression** (GLD% ~ SLV%)
- produce one plot
- document decisions, limitations, and next steps

> **Dataset**: `gold_data_2015_25.csv` (Kaggle: *Gold Price 2015–2025*)  
> **Goal**: Show a clear, interpretable **linear relation** between two variables in the dataset.  
> **Choice**: **GLD (gold)** vs **SLV (silver)** — these precious metals typically co-move and yield a clean linear fit for a beginner project.

---

## What I did (Step by Step)

1. **Import the dataset**
   - Loaded `gold_data_2015_25.csv` using Pandas.
   - Saved code in `analysing_gold_simple.py`.

2. **Inspect the data**
   - Used `df.head()`, `df.info()`, and `df.describe()` to understand shapes, dtypes, and summary statistics.
   - Checked missing values with `df.isnull().sum()` (no critical NAs expected).
   - Converted the `Date` column to `datetime` and sorted by date.

3. **Create returns & apply a meaningful filter**
   - Calculated daily percent changes (returns): `GLD_pct = GLD.pct_change()` and `SLV_pct = SLV.pct_change()`.
   - Defined “**big SLV moves**” as the **top 10%** of absolute daily SLV returns (90th percentile).
   - Filtered those days and described gold’s reaction on the same days (`subset["GLD_pct"].describe()`).

4. **Summarize with `groupby` (optional extension)**
   - For monthly summaries you can add:
     ```python
     df["YYYY_MM"] = df["Date"].dt.to_period("M").astype(str)
     monthly = df.groupby("YYYY_MM")[["GLD","SLV"]].agg(["mean","count"])
     ```
   - This provides monthly average levels and observation counts.

5. **Explore a machine-learning algorithm (Linear Regression)**
   - Fitted **ordinary least squares** on daily returns:
     - **Model**: `GLD_pct ~ SLV_pct`
     - Reported **slope**, **intercept**, and **R²**.
   - Using returns (instead of levels) avoids spurious regression on trending price series.

6. **Visualization**
   - Produced a single **scatter plot** (SLV% on x-axis, GLD% on y-axis) and added the **fitted OLS line**.
   - This visually confirms the positive linear relation.

7. **Documentation (this README)**
   - Explained goals, steps, decisions, and how to reproduce.

---

## Data Dictionary (from the CSV)

| Column   | Description                                 | Type      |
|----------|---------------------------------------------|-----------|
| Date     | Trading date                                | date      |
| SPX      | S&P 500 index level                         | float     |
| GLD      | Gold price (ETF proxy)                      | float     |
| USO      | Oil price (ETF proxy)                       | float     |
| SLV      | Silver price (ETF proxy)                    | float     |
| EUR/USD  | Euro to U.S. Dollar exchange rate           | float     |

Derived columns created in the script:
- `GLD_pct` = daily % change of GLD  
- `SLV_pct` = daily % change of SLV

---

## Results (fill with your run)
After running the script, copy the printed values here:

- **Missing values (per column)**: `Nothing`
- **Threshold for “big SLV moves”** (|SLV%| ≥): `2.4%`
- **GLD% on big-SLV days** (`describe()`):
  - mean: `0.04%`, median: `0.48%`, std: `1.77%`, min/max: `−5.37% / 4.85%`
- **Linear Regression (returns)** `GLD_pct ~ SLV_pct`:
  - slope: `0.4125557763407186` (expected **positive**)
  - intercept: `0.0002271795180790635`
  - **R²**: `0.5796355903962935` (closer to 1 ⇒ stronger linear fit)

**Interpretation (example wording):**  
> GLD and SLV exhibit a **positive linear relationship** on a daily basis. The OLS slope is positive and the R² of ~`…` suggests a meaningful (though not perfect) co-movement. On days with **large silver moves** (top 10% by absolute change), gold’s distribution widens, indicating stronger co-movement during volatile periods. These results show **correlation**, not causation.

---

## How to Run

### Local (Python 3.10+ recommended)
```bash
# optional: use a virtual environment
# python -m venv .venv
# source .venv/bin/activate   # Windows: .venv\Scripts\activate

pip install -r requirements.txt
python analysing_gold_simple.py
