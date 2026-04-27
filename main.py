import matplotlib.pyplot as plt
import pandas as pd
import json


def backtest_strategy(start_year, end_year, top_n=1, interval="1mo"):
    with open("data/top-20-spx-companies-by-market-cap-by-year.json", 'r') as f:
        top_20_spx_companies_by_market_cap_by_year = json.load(f)

    interval = "1mo"
    top_n = 5

    all_returns = []

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
        for n in range(1, top_n + 1):
            top_n_tickers.append(top_20_spx_companies_by_market_cap_by_year[str(year)][str(n)]["ticker"])
        
        top_n_close_prices = company_close_prices[top_n_tickers]

        year_returns = (top_n_close_prices.iloc[-1] - top_n_close_prices.iloc[0]) / top_n_close_prices.iloc[0] * 100

        strategy_return = year_returns.mean()
        all_returns.append({
            "year": year,
            "spx": spx_percent_return,
            "strategy": strategy_return
        })

    df_all = pd.DataFrame(all_returns).sort_values("year")
    df_all["spx_cum"] = (df_all["spx"] / 100 + 1).cumprod()
    df_all["strategy_cum"] = (df_all["strategy"] / 100 + 1).cumprod()
    df_all["year"] = df_all["year"].astype(int)
    # print(df_all)

    # 1. Load the Fama-French RF data
    with open("data/fama-french-risk-free-rates-by-year.json", 'r') as f:
        rf_data = json.load(f)

    # 2. Map the RF to each year in your results dataframe
    # Ensures both are strings for a proper match
    df_all["rf"] = df_all["year"].astype(str).map(rf_data)

    # 3. Calculate Annual Excess Returns
    df_all["excess_strategy"] = df_all["strategy"] - df_all["rf"]
    df_all["excess_spx"] = df_all["spx"] - df_all["rf"]

    # --- SHARPE RATIO ---
    # Formula: Mean(Excess Returns) / Standard Deviation(Returns)
    strategy_sharpe = df_all["excess_strategy"].mean() / df_all["strategy"].std()
    spx_sharpe = df_all["excess_spx"].mean() / df_all["spx"].std()

    # --- SORTINO RATIO ---
    # 1. Isolate the downside (only years where strategy underperformed the risk-free rate)
    strategy_downside = df_all.loc[df_all["excess_strategy"] < 0, "excess_strategy"]
    spx_downside = df_all.loc[df_all["excess_spx"] < 0, "excess_spx"]

    # 2. Calculate Downside Deviation
    strategy_downside_dev = strategy_downside.std()
    spx_downside_dev = spx_downside.std()

    # 3. Final Ratio Calculation
    strategy_sortino = df_all["excess_strategy"].mean() / strategy_downside_dev
    spx_sortino = df_all["excess_spx"].mean() / spx_downside_dev
 
    # 1. Calculate Strategy Max Drawdown
    # .cummax() keeps track of the highest value seen up to that date
    df_all["strategy_peak"] = df_all["strategy_cum"].cummax()
    df_all["strategy_dd"] = (df_all["strategy_cum"] - df_all["strategy_peak"]) / df_all["strategy_peak"]
    max_dd_strategy = df_all["strategy_dd"].min() * 100

    # 2. Calculate SPX Max Drawdown
    df_all["spx_peak"] = df_all["spx_cum"].cummax()
    df_all["spx_dd"] = (df_all["spx_cum"] - df_all["spx_peak"]) / df_all["spx_peak"]
    max_dd_spx = df_all["spx_dd"].min() * 100

    # 3. Find the "Pain Year" (When did the worst drop happen?)
    worst_year_strategy = df_all.loc[df_all["strategy_dd"] == df_all["strategy_dd"].min(), "year"].values[0]
    worst_year_spx = df_all.loc[df_all["spx_dd"] == df_all["spx_dd"].min(), "year"].values[0]

     # --- OUTPUT ---
    print("-" * 50)
    print(f"Strategy | Sharpe: {strategy_sharpe:.2f} | Sortino: {strategy_sortino:.2f} | Max Drawdown: {max_dd_strategy:.2f}% ({worst_year_strategy})")
    print(f"SPX  | Sharpe: {spx_sharpe:.2f} | Sortino: {spx_sortino:.2f} | Max Drawdown: {max_dd_spx:.2f}% ({worst_year_spx})")

    plt.plot(df_all["year"], df_all["spx_cum"], label="SPX")
    plt.plot(df_all["year"], df_all["strategy_cum"], label="Top " + str(top_n))

    plt.legend()
    plt.title("Cumulative Performance")
    plt.grid()
    plt.show()

if __name__ == "__main__":
    # 1989 - 2026
    # max top_n = 20
    backtest_strategy(start_year=2018, end_year=2025, top_n=5)