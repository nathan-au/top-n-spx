import yfinance as yf
import pandas as pd
from data import top_20_spx_companies_by_year

for year in top_20_spx_companies_by_year.keys():
    start_date = str(year) + "-01-01"
    end_date = str(year) + "-12-31"

    spx_close_prices = yf.download("^GSPC", start=start_date, end=end_date, interval="1mo", progress=False)["Close"]
    spx_close_prices.to_csv("data/spx_close_1mo_" + str(year) + ".csv", index=True)
    print(str(year))


    company_tickers = []
    for company in top_20_spx_companies_by_year[year].values():
        company_ticker = company["ticker"]
        company_tickers.append(company_ticker)
    print(company_tickers)

    company_close_prices = yf.download(company_tickers, start=start_date, end=end_date, interval="1mo", progress=False)["Close"]
    company_close_prices.to_csv("data/top_20_close_1mo_" + str(year) + ".csv", index=True)
