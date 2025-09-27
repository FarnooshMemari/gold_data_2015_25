import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression


df_gold = pd.read_csv("gold_data_2015_25.csv")


def data_inspection(df_gold):
    # sanity check: structure, stats, and missing values
    print(df_gold.head())
    df_gold.info()
    print(df_gold.describe())
    print("Missing values:\n", df_gold.isnull().sum())


data_inspection(df_gold)

# ensure proper time ordering for return calculations
df_gold["Date"] = pd.to_datetime(df_gold["Date"])
df_gold = df_gold.sort_values("Date").reset_index(drop=True)

# stationarity: use % changes instead of raw prices
df_gold["GLD_pct"] = df_gold["GLD"].pct_change()
df_gold["SLV_pct"] = df_gold["SLV"].pct_change()

# focus on extreme silver moves (top 10%) for stress testing
slv_treshold = df_gold["SLV_pct"].abs().quantile(0.90)
large_move_slv = df_gold["SLV_pct"].abs() >= slv_treshold
subset = df_gold[large_move_slv]
print("GLD% on those big SLV movement days:", subset["GLD_pct"].describe())

# drop NaNs so regression isn’t biased
returns_clean = df_gold.dropna(subset=["GLD_pct", "SLV_pct"])
X = returns_clean[["SLV_pct"]].values  # predictor
y = returns_clean["GLD_pct"].values  # response

# linear model: measure GLD’s sensitivity to SLV moves
model = LinearRegression().fit(X, y)

print("\nPredicting GLD percent change using SLV percent change")
print(
    "slope:",
    model.coef_[0],
    " intercept:",
    model.intercept_,
    " R^2:",
    model.score(X, y),
)

# visualize relation + fitted line to check model fit
slv_predict_range = np.linspace(X.min(), X.max(), 200).reshape(-1, 1)
plt.scatter(X, y, alpha=0.5, label="daily returns")
plt.plot(
    slv_predict_range, model.predict(slv_predict_range), linewidth=2, label="OLS fit"
)

# reference lines for easier interpretation
plt.axhline(0, color="gray", linestyle="--")
plt.axvline(0, color="gray", linestyle="--")

plt.xlabel("SLV daily % change")
plt.ylabel("GLD daily % change")
plt.title("Linear relation: GLD% ~ SLV%")
plt.legend()
plt.tight_layout()
plt.show()
