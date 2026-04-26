from data import top_20_spx_companies_by_year
import yfinance as yf
import matplotlib.pyplot as plt
import pandas as pd

year = 2020

start_date = str(year) + "-01-01"
end_date = str(year) + "-12-31"

spx_close_prices = yf.download("^GSPC", start=start_date, end=end_date, interval="1mo", progress=False)["Close"]
spx_start_price = spx_close_prices.iloc[0].item()
spx_end_price = spx_close_prices.iloc[-1].item()
spx_total_return = spx_end_price - spx_start_price
spx_percent_return = (spx_end_price - spx_start_price) / spx_start_price * 100
# print(round(spx_total_return, 2))
print(round(spx_percent_return, 2))

returns = []

for company in top_20_spx_companies_by_year[year].values():
    company_name = company["name"]
    company_ticker = company["ticker"]
    company_close_prices = yf.download(company_ticker, start=start_date, end=end_date, interval="1mo", progress=False)["Close"]
    company_start_price = company_close_prices.iloc[0].item()
    company_end_price = company_close_prices.iloc[-1].item()
    company_total_return = company_end_price - company_start_price
    company_percent_return = (company_end_price - company_start_price) / company_start_price * 100
    # print(round(company_total_return, 2))
    # print(round(company_percent_return, 2))
    returns.append({"ticker": company_ticker, "return": company_percent_return})


df = pd.DataFrame(returns)
plt.bar(df["ticker"], df["return"])
plt.xticks(rotation=90)
plt.axhline(y=spx_percent_return)
plt.show()

plt.plot(spx_close_prices)
plt.title("SPX (" + str(year) + ")")
plt.xlabel("Date")
plt.ylabel("Price")
plt.grid()
plt.show()