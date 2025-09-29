# GLD vs SLV 📈

**Do large daily moves in Silver (SLV) spill over into Gold (GLD)?**

> A small, reproducible project that inspects 2015–2025 GLD/SLV ETF data, cleans it, stresses the tails, and tests a simple linear relation — with guardrails for missing packages, CI, linting, and notebooks.

---

## 📑 Table of Contents
- [🧠 Why This Analysis Matters](#-why-this-analysis-matters)
- [❓ Problem Statement](#-problem-statement)
- [🧹 Data Preparation](#-data-preparation-clean--documented)
- [🔎 Analysis & Visualizations](#-analysis--visualizations)
- [🖼️ Figures](#-figures)
- [🚀 Quickstart](#-quickstart)
- [🧰 Tooling & Project Structure](#-tooling--project-structure)
- [🔁 Reproducibility Checklist](#-reproducibility-checklist)
- [✅ Results Summary](#-results-summary)
- [🧪 Tests](#-tests)
- [📦 Extensions](#-extensions)

---

## 🧠 Why This Analysis Matters

Markets often feel tightly coupled, but **linkages can be conditional**. Rather than just correlating gold and silver, this repo **stress-tests tail regimes**: do **big silver days** coincide with meaningfully different gold behavior? We:

* Convert prices to **daily % returns** (scale-free).
* Define a **tail regime** (|SLV%| ≥ 90th percentile) to spotlight stress.
* Compare GLD behavior in normal vs stressed days and test **GLD% ~ SLV%** with inference.

In practice, investors and risk managers care less about what happens on an average day and much more about how assets behave during extreme moves.

---

## ❓ Problem Statement

> **Question:** *When silver makes unusually large moves, how do those shocks affect gold’s returns, and is that effect statistically significant?*

**Data**: `gold_data_2015_25.csv` with at least columns `Date`, `GLD`, `SLV` (daily close or adjusted close), spanning 2015–2025.

**Outcome of interest**: `GLD_pct` daily return.  
**Primary regressor**: `SLV_pct` daily return.

---

## 🧹 Data Preparation (Clean & Documented)

1. Dependency guard for missing packages with friendly install hints.
2. Robust dataset loading with explicit error messages.
3. Schema checks: ensure and sort `Date` chronologically.
4. Compute `GLD_pct` and `SLV_pct` daily percent returns.
5. Drop missing values consistently once.
6. Define a **big-SLV regime** (90th percentile of |SLV_pct|) and split into big vs normal days.

**Data dictionary**:

* `Date` *(datetime)* — trading date.  
# GLD vs SLV 📈

**Do large daily moves in Silver (SLV) spill over into Gold (GLD)?**

A small, reproducible project that inspects 2015–2025 GLD/SLV ETF data, cleans it, stresses the tails, and tests a simple linear relation — with guardrails for missing packages, CI, linting, and notebooks.

---

## 📑 Table of Contents
- [Why This Analysis Matters](#-why-this-analysis-matters)
- [Problem Statement](#-problem-statement)
- [Data Preparation](#-data-preparation-clean--documented)
- [Analysis & Visualizations](#-analysis--visualizations)
- [Figures](#-figures)
- [Quickstart](#-quickstart)
- [Tooling & Project Structure](#-tooling--project-structure)
- [Reproducibility Checklist](#-reproducibility-checklist)
- [Results Summary](#-results-summary)
- [Tests](#-tests)
- [Extensions](#-extensions)

---

## 🧠 Why This Analysis Matters

Markets often feel tightly coupled, but **linkages can be conditional**. Rather than just correlating gold and silver, this repo **stress-tests tail regimes**: do **big silver days** coincide with meaningfully different gold behavior? We:

- Convert prices to **daily % returns** (scale-free).
- Define a **tail regime** (|SLV%| ≥ 90th percentile) to spotlight stress.
- Compare GLD behavior in normal vs stressed days and test **GLD% ~ SLV%** with inference.

In practice, investors and risk managers care less about what happens on an average day and much more about how assets behave during extreme moves.

---

## ❓ Problem Statement

**Question:** *When silver makes unusually large moves, how do those shocks affect gold’s returns, and is that effect statistically significant?*

**Data**: `gold_data_2015_25.csv` with at least columns `Date`, `GLD`, `SLV` (daily close or adjusted close), spanning 2015–2025.

**Outcome of interest**: `GLD_pct` daily return.  
**Primary regressor**: `SLV_pct` daily return.

---

## 🧹 Data Preparation (Clean & Documented)

1. Dependency guard for missing packages with friendly install hints.
2. Robust dataset loading with explicit error messages.
3. Schema checks: ensure and sort `Date` chronologically.
4. Compute `GLD_pct` and `SLV_pct` daily percent returns.
5. Drop missing values consistently once.
6. Define a **big-SLV regime** (90th percentile of |SLV_pct|) and split into big vs normal days.

**Data dictionary**:

- `Date` *(datetime)* — trading date.  
- `GLD`, `SLV` *(float)* — ETF prices.  
- `GLD_pct`, `SLV_pct` *(float)* — daily % returns.  

---

## 🔎 Analysis & Visualizations

- **Distribution contrast**: GLD returns on normal vs big SLV days (boxplot).
- **Time-series context**: GLD & SLV returns plotted with big SLV days highlighted.
- **Regression test**: `GLD_pct ~ SLV_pct` with OLS (β, R², p-value).

**Takeaway template:**

- β estimate: … (sign & magnitude)  
- p-value: … (significant at 5%? yes/no)  
- R²: …  
- GLD return distribution widens/doesn’t widen on big SLV days.  

---

## 🖼️ Figures

Main plots generated by the analysis script. These images render on GitHub when the PNGs are present in `reports/figures/`.

### Boxplot: GLD returns on Normal vs Big SLV days
![Boxplot of GLD returns](reports/figures/boxplot_gld_normal_vs_bigslv.png)

### Time Series: GLD & SLV daily % changes (big SLV days highlighted)
![Time Series of returns](reports/figures/timeseries_gld_slv_pct.png)

### Regression: GLD vs SLV with OLS fit
![Regression scatter with OLS fit](reports/figures/regression_gld_on_slv.png)

---

## 🚀 Quickstart

```bash
python3 -m venv source
source source/bin/activate
pip install -r requirements.txt
python analysing_gold_data.py
```

Outputs: summary stats and PNG figures in `reports/figures/`.

---

## 🧰 Tooling & Project Structure

Tools: `black`, `ruff`, `pytest`, `pre-commit`, GitHub Actions CI.

Repository layout (top-level):

.
├── analysing_gold_data.py
├── gold_data_2015_25.csv
├── gold_analysis/
├── notebooks/
├── reports/figures/
│   ├── boxplot_gld_normal_vs_bigslv.png
│   ├── timeseries_gld_slv_pct.png
│   └── regression_gld_on_slv.png
├── requirements.txt
├── Dockerfile
├── Makefile
├── pyproject.toml
├── .pre-commit-config.yaml
└── .github/workflows/ci.yml

### requirements.txt

This file ensures anyone can recreate the same environment. It lists the Python dependencies so beginners don’t have to guess which packages to install.

Install with:

```bash
pip install -r requirements.txt
```

### Dockerfile (example)

```dockerfile
FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["python", "analysing_gold_data.py"]
```

Usage:

```bash
docker build -t gld-slv-analysis .
docker run --rm -v $(pwd)/reports/figures:/app/reports/figures gld-slv-analysis
```

Makefile (selected targets)

```makefile
setup:
	python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt

run:
	python analysing_gold_data.py

clean:
	rm -rf __pycache__ .pytest_cache reports/figures/*.png

docker-build:
	docker build -t gld-slv-analysis .

docker-run:
	docker run --rm -v $(pwd)/reports/figures:/app/reports/figures gld-slv-analysis
```

---

## 🔁 Reproducibility Checklist

- Use venv/conda & pin requirements.
- Set seeds if you add stochastic methods.
- Single-entry script: `analysing_gold_data.py`.
- CI runs analysis and uploads figures.
- Strip notebooks outputs before committing.

---

## ✅ Results Summary

Example (toy output) after running the analysis script:

| Metric | Value | Interpretation |
|---|---:|---|
| β (SLV → GLD) | 0.42 | Gold moves ~42% of silver’s move |
| p-value(β) | 0.001 | Statistically significant (5% level) |
| R² | 0.27 | Silver explains ~27% of gold’s variance |

Regime insight: On big SLV days, the distribution of GLD returns becomes noticeably wider than on normal days.

---

## 🧪 Tests

Run the test suite after setting up the environment:

```bash
pytest -q
```

---

## 📦 Extensions

- Separate positive/negative shocks.
- Nonlinear models.
- Volatility controls.
- Out-of-sample forecasting.
