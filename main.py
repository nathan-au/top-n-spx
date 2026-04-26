import matplotlib.pyplot as plt
import pandas as pd
import json

with open("data/top-20-spx-companies-by-market-cap-by-year.json", 'r') as f:
    top_20_spx_companies_by_market_cap_by_year = json.load(f)

interval = "1mo"
top_n = 1

all_returns = []

for year in top_20_spx_companies_by_market_cap_by_year.keys():

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
    
    # df = year_returns.reset_index()
    # df.columns = ["ticker", "return"]
    # print(df.head())
    # plt.bar(df["ticker"], df["return"])
    # plt.xticks(rotation=90)
    # plt.axhline(y=spx_percent_return)
    # plt.title(str(year))
    # plt.tight_layout()
    # plt.grid()
    # plt.savefig("plots/" + str(year) + ".png")
    # plt.close()

    strategy_return = year_returns.mean()
    all_returns.append({
        "year": year,
        "spx": spx_percent_return,
        "strategy": strategy_return
    })

df_all = pd.DataFrame(all_returns).sort_values("year")
df_all["spx_cum"] = (df_all["spx"] / 100 + 1).cumprod()
df_all["strategy_cum"] = (df_all["strategy"] / 100 + 1).cumprod()

print(df_all)


plt.plot(df_all["year"], df_all["spx_cum"], label="SPX")
plt.plot(df_all["year"], df_all["strategy_cum"], label="Top 20")

plt.legend()
plt.title("Cumulative Performance")
plt.xticks(rotation=90)
plt.grid()
plt.show()