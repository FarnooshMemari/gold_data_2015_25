<!-- .github/copilot-instructions.md - Guidance for AI coding agents working on this repo -->
# Copilot / AI agent instructions — gold_data_2015_25

This repository analyzes daily returns for gold (GLD) vs silver (SLV). The guidance below is concise and focused on patterns, workflows, and repository-specific constraints an AI coding agent should follow to be immediately productive.

1) Big picture (why / architecture)
- Purpose: compute daily % returns, identify large SLV moves, fit a simple OLS model GLD_pct ~ SLV_pct, and produce plots. The code is intentionally small and modular for clarity and reproducibility.
- Main modules (see `gold_analysis/`):
  - `io.py` — CSV loading, required columns: `Date`, `GLD`, `SLV`. Validates dates and sorts by `Date`.
  - `transform.py` — computes `GLD_pct` and `SLV_pct` with `pct_change()` and drops the initial NA; selects top absolute SLV moves via quantile.
  - `model.py` — wraps sklearn's `LinearRegression` and returns slope, intercept, r2, and the model object.
  - `viz.py` — plotting helpers; uses `matplotlib.use('Agg')` to be headless-safe and returns the path to saved PNGs.
- Single-script orchestrator: `analysing_gold_data.py` demonstrates an end-to-end flow but also contains duplicated logic vs. the `gold_analysis/` modules (prefer using the modular functions for edits and tests).

2) Key developer workflows & commands (use these exactly)
- Install deps: `pip install -r requirements.txt` (Dev Container uses Python 3.11 in `.devcontainer/devcontainer.json` and runs a postCreateCommand that installs requirements).
- Run tests: `pytest` (CI runs `pytest -q`).
- Lint: `flake8 .` (CI runs flake8; local Makefile has a `lint` target but it calls a specific flake8 invocation — prefer `flake8 .`).
- Run main script: `python analysing_gold_data.py` (expects `gold_data_2015_25.csv` in the repo root).

3) Project-specific conventions & patterns
- Prefer using functions in `gold_analysis/` rather than inlining logic into `analysing_gold_data.py`. Tests import from `gold_analysis.*` and `tests/conftest.py` ensures repo root is on `sys.path`.
- Data validation is strict: `io.load_csv()` raises `ValueError` for missing required columns or unparseable dates. Keep that behavior when refactoring.
- `transform.add_returns()` drops the first row created by `pct_change()` (tests expect this). Do not silently impute or keep that NA row.
- `viz.scatter_with_fit()` uses `matplotlib.use('Agg')` at module-import time; avoid changing backend selection order. Also, `viz.scatter_with_fit()` returns the saved path (tests assert this and check PNG signature).

4) Tests and CI expectations
- Tests exercise small, deterministic slices (unit + e2e). Preserve signatures and exceptions that tests assert (e.g., `load_csv()` raising `ValueError`, `fit_ols_gld_on_slv()` raising `ValueError` on empty input).
- CI uses Python 3.12 in `.github/workflows/main.yml` and runs `pip install -r requirements.txt`, `flake8 .`, then `pytest -q`. Keep compatibility with Python 3.11+ (Dev Container uses 3.11). Prefer not to use syntax that is only valid in 3.12 unless intentionally upgrading CI.

5) Integration points & external dependencies
- Primary dependencies in `requirements.txt`: pandas, numpy, scikit-learn, matplotlib, pytest, pytest-cov, flake8, black.
- No network calls or external APIs. The dataset `gold_data_2015_25.csv` is expected to be present in repo root for `analysing_gold_data.py` and the E2E test; tests create temporary files where necessary.

6) Safe change rules for AI edits (must follow)
- Do not change function signatures used by tests in `gold_analysis/*.py` (e.g., `load_csv(path)`, `add_returns(df)`, `select_top_abs_slv(df, quantile)`, `fit_ols_gld_on_slv(df)`, `scatter_with_fit(df, fit_info, path)`).
- Preserve error types and messages that tests rely on (raising `ValueError` vs returning None). If changing behavior, update tests accordingly and run the test suite.
- Keep `matplotlib.use('Agg')` in `viz.py` to avoid headless failures.
- Avoid adding heavy new dependencies unless added to `requirements.txt` and CI is updated.

7) Examples / snippets (use these as templates)
- Loading data (use `gold_analysis.io.load_csv`) instead of `pd.read_csv` for consistency and validation:
  - Example: `from gold_analysis.io import load_csv; df = load_csv('gold_data_2015_25.csv')`
- Add returns & select top moves:
  - `from gold_analysis.transform import add_returns, select_top_abs_slv`
  - `df_r = add_returns(df); top, thr = select_top_abs_slv(df_r, 0.9)`
- Fit model:
  - `from gold_analysis.model import fit_ols_gld_on_slv`
  - `fit = fit_ols_gld_on_slv(df_r)` → `fit['slope']`, `fit['r2']`

8) Small operational notes
- `.gitignore` excludes `*.csv` and `*.png` → adding or updating the CSV in repo root requires removing it from `.gitignore` if you intend to commit it.
- `Makefile` contains `install`, `format` (black), and `lint` targets. The `lint` target in Makefile has a duplicate `lint:` line; prefer invoking `flake8 .` directly.

9) When to propose larger changes
- If you refactor to remove duplication between `analysing_gold_data.py` and `gold_analysis/` modules, update `README.md` and ensure `tests/test_system_e2e.py` still runs. Run `pytest` and `flake8` before committing.

If anything here is unclear or you'd like me to expand any section (examples, CI tips, or add common PR templates), tell me which part to iterate on.
