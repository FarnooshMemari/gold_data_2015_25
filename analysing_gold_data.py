# Import necessary libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

# 1) Load the dataset
df = pd.read_csv("gold_data_2015_25.csv")

# 2) Initial data inspection
print(df.head())  # Preview the first few rows
df.info()  # Get column types and non-null counts
print(df.describe())  # Basic stats summary
print("Missing values:\n", df.isnull().sum())  # Check for missing data

# Convert the 'Date' column to datetime format and sort the data over time
df["Date"] = pd.to_datetime(df["Date"])
df = df.sort_values("Date").reset_index(drop=True)

# 3) Feature engineering: compute daily percentage changes for GLD and SLV
df["GLD_pct"] = df["GLD"].pct_change()
df["SLV_pct"] = df["SLV"].pct_change()

# Define threshold: 90th percentile of absolute SLV daily changes
thr = df["SLV_pct"].abs().quantile(0.90)

# Filter: select days where SLV had large moves (top 10%)
subset = df[df["SLV_pct"].abs() >= thr]
print("GLD% on those big SLV movement days:\n", subset["GLD_pct"].describe())

# 4) Prepare data for linear regression: remove rows with NaN % changes
ret = df.dropna(subset=["GLD_pct", "SLV_pct"])
X = ret[["SLV_pct"]].values  # Independent variable: SLV daily % changes
y = ret["GLD_pct"].values  # Dependent variable: GLD daily % changes

# Fit a linear regression model
model = LinearRegression().fit(X, y)

# Output model parameters
print("\nPredicting GLD percent change using SLV percent change")
print(
    "slope:",
    model.coef_[0],
    " intercept:",
    model.intercept_,
    " R^2:",
    model.score(X, y),
)

# 5) Plot: scatter of actual returns and fitted regression line
xs = np.linspace(X.min(), X.max(), 200).reshape(
    -1, 1
)  # Linearly spaced values for plotting
plt.scatter(X, y, alpha=0.5, label="daily returns")  # Scatter plot of data
plt.plot(xs, model.predict(xs), linewidth=2, label="OLS fit")  # Fitted line

# Add reference lines at 0 for visual aid
plt.axhline(0, color="gray", linestyle="--")
plt.axvline(0, color="gray", linestyle="--")

# Labeling and final touches
plt.xlabel("SLV daily % change")
plt.ylabel("GLD daily % change")
plt.title("Linear relation: GLD% ~ SLV%")
plt.legend()
plt.tight_layout()
plt.show()
