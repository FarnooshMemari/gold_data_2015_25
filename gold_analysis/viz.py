# Visualization helper functions for the gold/silver analysis project
import matplotlib

# Use a non-interactive backend so plots can be saved in headless environments
# (like VS Code Dev Containers or Docker). This avoids GUI errors with plt.show().
matplotlib.use("Agg")


def scatter_with_fit(df, fit_info, path="scatter_fit.png"):
    """
    Create and save a scatter plot of GLD_pct vs SLV_pct
    with the fitted OLS regression line overlaid.

    Args:
        df (pd.DataFrame): Data with columns "GLD_pct" and "SLV_pct".
        fit_info (dict): Output from fit_ols_gld_on_slv containing slope, intercept.
        path (str): File path where the PNG image will be saved.

    Returns:
        str: Path to the saved image file.
    """
    # Local import to respect backend setup order and avoid E402
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots()

    # Scatter plot of raw data points
    ax.scatter(df["SLV_pct"], df["GLD_pct"], s=10, alpha=0.6, label="Data")

    # Regression line
    m, b = fit_info["slope"], fit_info["intercept"]
    xs = df["SLV_pct"].to_numpy()
    ax.plot(xs, m * xs + b, color="red", label="OLS fit")

    # Labels and legend
    ax.set_xlabel("SLV_pct")
    ax.set_ylabel("GLD_pct")
    ax.set_title("GLD% vs SLV% with OLS line")
    ax.legend()

    fig.tight_layout()
    fig.savefig(path, dpi=150)
    plt.close(fig)
    return path
