import matplotlib.pyplot as plt
import pandas as pd
import json


def backtest_strategy(start_year, end_year, top_n, interval):
    with open("data/top-20-spx-companies-by-market-cap-by-year.json", "r") as f:
        top_20_spx_companies_by_market_cap_by_year = json.load(f)

    backtest_returns = []

    years = []
    for year in range(start_year, end_year + 1):
        years.append(year)

    for year in years:

        spx_close_prices = pd.read_csv("data/spx/" + str(year) + "-" + interval + ".csv", index_col=0)

        spx_start_price = spx_close_prices.iloc[0].item()
        spx_end_price = spx_close_prices.iloc[-1].item()
        spx_percent_return = (spx_end_price - spx_start_price) / spx_start_price * 100

        year_returns = []
        
        company_close_prices = pd.read_csv("data/top-20/" + str(year) + "-" + interval + ".csv", index_col=0)

        top_n_tickers = []
        for n in range(1, top_n + 1 ):
            top_n_tickers.append(top_20_spx_companies_by_market_cap_by_year[str(year)][str(n)]["ticker"])
        
        top_n_close_prices = company_close_prices[top_n_tickers]

        year_returns = (top_n_close_prices.iloc[-1] - top_n_close_prices.iloc[0]) / top_n_close_prices.iloc[0] * 100

        strategy_return = year_returns.mean()
        backtest_returns.append({
            "year": year,
            "strategy": strategy_return,
            "spx": spx_percent_return
        })

    df = pd.DataFrame(backtest_returns).sort_values("year")
    df["strategy_cum"] = (df["strategy"] / 100 + 1).cumprod()
    df["spx_cum"] = (df["spx"] / 100 + 1).cumprod()
    df["year"] = df["year"].astype(int)

    with open("data/fama-french-risk-free-rates-by-year.json", "r") as f:
        fama_french_risk_free_rates_by_year = json.load(f)

    df["rf"] = df["year"].astype(str).map(fama_french_risk_free_rates_by_year)

    df["strategy_excess"] = df["strategy"] - df["rf"]
    df["spx_excess"] = df["spx"] - df["rf"]

    strategy_sharpe = df["strategy_excess"].mean() / df["strategy"].std()
    spx_sharpe = df["spx_excess"].mean() / df["spx"].std()

    strategy_downside = df.loc[df["strategy_excess"] < 0, "strategy_excess"]
    spx_downside = df.loc[df["spx_excess"] < 0, "spx_excess"]

    strategy_sortino = df["strategy_excess"].mean() / strategy_downside.std()
    spx_sortino = df["spx_excess"].mean() / spx_downside.std()
 
    df["strategy_peak"] = df["strategy_cum"].cummax()
    df["spx_peak"] = df["spx_cum"].cummax()

    df["strategy_dd"] = (df["strategy_cum"] - df["strategy_peak"]) / df["strategy_peak"]
    df["spx_dd"] = (df["spx_cum"] - df["spx_peak"]) / df["spx_peak"]

    strategy_max_dd = df["strategy_dd"].min() * 100
    spx_max_dd = df["spx_dd"].min() * 100

    strategy_worst_year = df.loc[df["strategy_dd"] == df["strategy_dd"].min(), "year"].values[0]
    spx_worst_year = df.loc[df["spx_dd"] == df["spx_dd"].min(), "year"].values[0]

    strategy_final_return = (df["strategy_cum"].iloc[-1] - 1) * 100
    spx_final_return = (df["spx_cum"].iloc[-1] - 1) * 100

    label_width = 20
    column_width = 15
    table_width = label_width + 3 + column_width + 3 + column_width
    
    print(f"{f"Top {top_n} SPX Strategy ({start_year} - {end_year})":^{table_width}}")
    print("-" * table_width)
    print(f"{"Metric":<{label_width}} | {"Strategy":<{column_width}} | {"SPX":<{column_width}}")
    print("-" * table_width)
    print(f"{"Total Return":<{label_width}} | {f"{strategy_final_return:.2f}%":<{column_width}} | {f"{spx_final_return:.2f}%":<{column_width}}")
    print(f"{"Sharpe Ratio":<{label_width}} | {strategy_sharpe:<{column_width}.2f} | {spx_sharpe:<{column_width}.2f}")
    print(f"{"Sortino Ratio":<{label_width}} | {strategy_sortino:<{column_width}.2f} | {spx_sortino:<{column_width}.2f}")
    print(f"{"Max Drawdown":<{label_width}} | {f"{strategy_max_dd:.2f}%":<{column_width}} | {f"{spx_max_dd:.2f}%":<{column_width}}")
    print(f"{"Worst Year":<{label_width}} | {str(strategy_worst_year):<{column_width}} | {str(spx_worst_year):<{column_width}}")
    print("-" * table_width)

    return {
        "params": {
            "start_year": start_year,
            "end_year": end_year,
            "top_n": top_n,
            "interval": interval
        },
        "metrics": {
            "strategy_total_return": strategy_final_return,
            "spx_total_return": spx_final_return,
            "strategy_sharpe": strategy_sharpe,
            "spx_sharpe": spx_sharpe,
            "strategy_sortino": strategy_sortino,
            "spx_sortino": spx_sortino,
            "strategy_max_drawdown": strategy_max_dd,
            "spx_max_drawdown": spx_max_dd,
            "strategy_worst_year": strategy_worst_year,
            "spx_worst_year": spx_worst_year
        },
        "data": df  # full yearly data
    }

if __name__ == "__main__":
    # min start_year = 1989, max end_year = 2026, max top_n = 20
    # for n in range (1, 20):
    #     backtest_strategy(start_year=2000, end_year=2025, top_n=n, interval="1mo")

    results = []

    for n in range(1, 21):
        result = backtest_strategy(
            start_year=2000,
            end_year=2025,
            top_n=n,
            interval="1mo"
        )
        results.append(result)
    summary = []

    for r in results:
        summary.append({
            "top_n": r["params"]["top_n"],
            "return": r["metrics"]["strategy_total_return"],
            "sharpe": r["metrics"]["strategy_sharpe"],
            "sortino": r["metrics"]["strategy_sortino"],
            "max_dd": r["metrics"]["strategy_max_drawdown"]
        })

    summary_df = pd.DataFrame(summary)
    summary_df = summary_df.sort_values("return", ascending=False)
    summary_df = summary_df.reset_index(drop=True)
    print(summary_df)

    plt.figure(figsize=(10, 6))
    plt.scatter(summary_df["max_dd"].abs(), summary_df["return"], c=summary_df["top_n"], cmap='viridis', s=100)
    plt.colorbar(label='Top N Value')

    # Label each point with its N
    for i, txt in enumerate(summary_df["top_n"]):
        plt.annotate(txt, (summary_df["max_dd"].abs()[i], summary_df["return"][i]), xytext=(5,5), textcoords='offset points')

        # 1. Sort by risk (Max Drawdown)
    sorted_df = summary_df.sort_values("max_dd", ascending=False) # max_dd is negative, so this goes left-to-right

    frontier_x = []
    frontier_y = []
    current_max_return = -1

    # 2. Iterate and find 'un-dominated' points
    for _, row in sorted_df.iterrows():
        risk = abs(row["max_dd"])
        ret = row["return"]
        
        if ret > current_max_return:
            frontier_x.append(risk)
            frontier_y.append(ret)
            current_max_return = ret

    # 3. Plot the curve on your existing chart
    plt.plot(frontier_x, frontier_y, color='red', linestyle='--', linewidth=2, label='Efficient Frontier')
    plt.legend()

    plt.title("Top n SPX Efficiency Frontier")
    plt.xlabel("Risk (Max Drawdown %)")
    plt.ylabel("Reward (Total Return %)")
    plt.grid(True, alpha=0.3)
    plt.show()