# Main script that ties together loading, transforming,
# modeling, and now plotting of the gold/silver dataset.

from gold_analysis.io import load_csv
from gold_analysis.transform import add_returns, select_top_abs_slv
from gold_analysis.model import fit_ols_gld_on_slv
from gold_analysis.viz import scatter_with_fit  # <-- Import plotting helper


def main(csv_path="gold_data_2015_25.csv"):
    # Step 1: load raw CSV data
    df = load_csv(csv_path)

    # Step 2: calculate daily percentage returns for GLD and SLV
    df_r = add_returns(df)

    # Step 3: identify "big move" days (top 10% SLV absolute moves)
    big, thr = select_top_abs_slv(df_r, 0.9)

    # Step 4: fit OLS regression (GLD_pct ~ SLV_pct)
    fit = fit_ols_gld_on_slv(df_r)

    # Print analysis results to terminal
    print(f"Top-10% |SLV| threshold: {thr:.4f}")
    print(
        f"Slope: {fit['slope']:.6f}, Intercept: {fit['intercept']:.6f},\n"
        f"R²: {fit['r2']:.6f}"
    )
    print(f"Big-move rows: {len(big)} / {len(df_r)}")

    # Step 5: Save scatter plot with regression line to an image file
    out_path = scatter_with_fit(df_r, fit, path="image.png")
    print(f"Saved plot to {out_path}")


if __name__ == "__main__":
    # Run the analysis workflow if the script is called directly
    main()
