import pandas as pd
from sklearn.linear_model import LinearRegression

def fit_ols_gld_on_slv(df: pd.DataFrame):
    """
    Fit an OLS regression: GLD_pct ~ SLV_pct
    - Uses sklearn's LinearRegression.
    - Returns slope, intercept, and R² score along with model.
    """
    X = df[["SLV_pct"]].to_numpy()
    y = df["GLD_pct"].to_numpy()

    # Empty dataset → cannot fit model
    if len(df) == 0:
        raise ValueError("Empty data for regression")

    model = LinearRegression().fit(X, y)
    return {
        "model": model,
        "slope": float(model.coef_[0]),
        "intercept": float(model.intercept_),
        "r2": float(model.score(X, y)),
    }
