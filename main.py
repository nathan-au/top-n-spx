from data import top_20_spx_companies_by_year
import yfinance as yf
import matplotlib.pyplot as plt
import pandas as pd

year = 2020

all_returns = []

for year in top_20_spx_companies_by_year.keys():

    spx_close_prices = pd.read_csv("data/spx_close_1mo_" + str(year) + ".csv", index_col=0)

    spx_start_price = spx_close_prices.iloc[0].item()
    spx_end_price = spx_close_prices.iloc[-1].item()
    spx_percent_return = (spx_end_price - spx_start_price) / spx_start_price * 100

    print(round(spx_percent_return, 2))

    year_returns = []
    
    
    company_close_prices = pd.read_csv("data/top_20_close_1mo_" + str(year) + ".csv", index_col=0)

    year_returns = (company_close_prices.iloc[-1] - company_close_prices.iloc[0]) / company_close_prices.iloc[0] * 100
    
    df = year_returns.reset_index()
    df.columns = ["ticker", "return"]
    print(df.head())
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


# plt.plot(df_all["year"], df_all["spx_cum"], label="SPX")
# plt.plot(df_all["year"], df_all["strategy_cum"], label="Top 20")

# plt.legend()
# plt.title("Cumulative Performance")
# plt.grid()
# plt.show()