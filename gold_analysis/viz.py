# Visualization helpers for the gold/silver analysis project
import matplotlib

# Use a non-interactive backend so plots can be saved in headless environments
# (avoids GUI errors with plt.show())
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

    # Use a clean style to improve readability in saved figures.
    # Try seaborn first (if installed), otherwise fall back to a matplotlib
    # style name and finally to a safe builtin style.
    try:
        import seaborn as sns

        sns.set_style("whitegrid")
    except Exception:
        # If seaborn not available, only use a named style if it's present
        try:
            if "seaborn-whitegrid" in plt.style.available:
                plt.style.use("seaborn-whitegrid")
            else:
                plt.style.use("ggplot")
        except Exception:
            # Fallback to matplotlib defaults if anything goes wrong
            pass

    fig, ax = plt.subplots(figsize=(7, 5))

    # Scatter plot of raw data points
    ax.scatter(
        df["SLV_pct"], df["GLD_pct"], s=18, alpha=0.7, edgecolor="none", label="Data"
    )

    # Regression line: sort x for a clean line plot (avoids zig-zag if df not sorted)
    m, b = fit_info["slope"], fit_info["intercept"]
    xs = df["SLV_pct"].to_numpy()
    order = xs.argsort()
    xs_sorted = xs[order]
    ax.plot(xs_sorted, m * xs_sorted + b, color="red", linewidth=2, label="OLS fit")

    # Axis formatting: show pct-like numbers (multiply by 100 visually)
    try:
        import matplotlib.ticker as mtick

        ax.xaxis.set_major_formatter(mtick.PercentFormatter(xmax=1.0))
        ax.yaxis.set_major_formatter(mtick.PercentFormatter(xmax=1.0))
    except Exception:
        # If formatter unavailable, continue without raising — not critical for tests
        pass

    # Labels, title, and legend placed unobtrusively
    ax.set_xlabel("SLV daily % change")
    ax.set_ylabel("GLD daily % change")
    ax.set_title("GLD% vs SLV% with OLS line")
    ax.legend(frameon=True)

    fig.tight_layout()
    fig.savefig(path, dpi=200)
    plt.close(fig)
    return path
