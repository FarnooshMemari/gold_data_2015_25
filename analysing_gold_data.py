import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import statsmodels.api as sm
import matplotlib.dates as mdates
import matplotlib.ticker as mtick
import seaborn as sns

sns.set_style("whitegrid")

# --- Load dataset (regular read; will raise if missing) ---
gld_slv_df = pd.read_csv("gold_data_2015_25.csv")


# Inspect data early to catch schema/quality surprises
def data_inspection(df):
    print(df.head())
    df.info()
    print(df.describe())
    print("Missing values:\n", df.isnull().sum())


data_inspection(gld_slv_df)

# Ensure dates are ordered so returns reflect trading sequence
gld_slv_df["Date"] = pd.to_datetime(gld_slv_df["Date"])
gld_slv_df = gld_slv_df.sort_values("Date").reset_index(drop=True)

# Use % changes instead of prices to remove trends/scale effects
gld_slv_df["GLD_pct"] = gld_slv_df["GLD"].pct_change()
gld_slv_df["SLV_pct"] = gld_slv_df["SLV"].pct_change()

# Clean once so later analysis is consistent
gld_slv_df = gld_slv_df.dropna(subset=["GLD_pct", "SLV_pct"])

# Define “big SLV” regime to stress-test tails
slv_threshold = gld_slv_df["SLV_pct"].abs().quantile(0.90)
slv_big_move_mask = gld_slv_df["SLV_pct"].abs() >= slv_threshold
slv_big_move_df = gld_slv_df[slv_big_move_mask]
normal_df = gld_slv_df[~slv_big_move_mask]

# ========= DESCRIPTIVES =========

# Boxplot: show GLD variability in normal vs big SLV days
plt.figure(figsize=(7, 5))
plt.boxplot(
    [normal_df["GLD_pct"].values, slv_big_move_df["GLD_pct"].values],
    labels=["Normal Days", "Big SLV Days"],
    showfliers=True,
)
plt.ylabel("GLD daily % change")
plt.title("Distribution of GLD returns: Normal vs Big SLV Days")
plt.tight_layout()
plt.show()

# Time series: show shocks and co-movement patterns


plt.figure(figsize=(12, 5))
plt.plot(gld_slv_df["Date"], gld_slv_df["GLD_pct"], label="GLD % change", linewidth=1)
plt.plot(
    gld_slv_df["Date"],
    gld_slv_df["SLV_pct"],
    label="SLV % change",
    alpha=0.8,
    linewidth=1,
)
plt.scatter(
    slv_big_move_df["Date"],
    slv_big_move_df["SLV_pct"],
    s=30,
    marker="o",
    label="Big SLV days",
    color="tab:red",
    zorder=3,
)
plt.axhline(0, color="gray", linestyle="--", linewidth=1)
plt.xlabel("Date")
plt.ylabel("Daily % change")
plt.title("Time Series of Daily Returns (GLD & SLV)")
plt.legend()

# Format x-axis dates and y-axis as percents
ax = plt.gca()
ax.xaxis.set_major_locator(mdates.AutoDateLocator())
ax.xaxis.set_major_formatter(mdates.ConciseDateFormatter(ax.xaxis.get_major_locator()))
ax.yaxis.set_major_formatter(mtick.PercentFormatter(xmax=1.0))
plt.xticks(rotation=30, ha="right")
plt.grid(alpha=0.25)
plt.tight_layout()
plt.show()

# ========= REGRESSION WITH P-VALUE =========


# Feature prep for clarity
def prepare_features(df, x_col="SLV_pct", y_col="GLD_pct"):
    X = df[[x_col]].values
    y = df[y_col].values
    return X, y


X_all, y_all = prepare_features(gld_slv_df)
if (
    len(X_all) < 10
    or np.allclose(X_all, X_all.mean())
    or np.allclose(y_all, y_all.mean())
):
    print("❌ Not enough/usable data for regression inference.")
    sys.exit(1)

# Use statsmodels to test significance of beta
X_sm = sm.add_constant(X_all)
ols = sm.OLS(y_all, X_sm).fit()

beta = float(ols.params[1])
alpha = float(ols.params[0])
r2 = float(ols.rsquared)
p_value = float(ols.pvalues[1])

print("\nOLS Results (GLD_pct ~ SLV_pct) via statsmodels")
print(f"alpha (intercept): {alpha:.6f}")
print(f"beta (slope)    : {beta:.6f}")
print(f"R^2             : {r2:.6f}")
print(f"p-value (beta)  : {p_value:.6g}")

# Interpret at 5% level to turn stats into a decision
if p_value < 0.05:
    direction = "positive" if beta > 0 else "negative"
    print(f"✅ At 5% significance: beta is statistically significant and {direction}.")
else:
    print("⚠️ At 5% significance: beta is NOT statistically significant.")

# Optional: scatter + fitted line to sanity-check regression visually
sk_model = LinearRegression().fit(X_all, y_all)
x_line = np.linspace(X_all.min(), X_all.max(), 200).reshape(-1, 1)
plt.scatter(X_all, y_all, alpha=0.5, label="daily returns")
plt.plot(x_line, sk_model.predict(x_line), linewidth=2, label="OLS fit")
plt.axhline(0, color="gray", linestyle="--")
plt.axvline(0, color="gray", linestyle="--")
plt.xlabel("SLV daily % change")
plt.ylabel("GLD daily % change")
plt.title("Linear relation: GLD% ~ SLV% (with OLS line)")
plt.legend()
plt.tight_layout()
plt.show()
