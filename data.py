# Data as of April 24, 2026, 16:00 ET
# top-20-spx-companies-by-market-cap-by-year.json
# top-20-vs-spx-market-cap-by-year.json

import json
import yfinance as yf
import os
import time

def setup_directory(directory):
    sub_directories = ["spx", "top-20"]

    for sub_directory in sub_directories:
        sub_directory_path = os.path.join(directory, sub_directory)    
        if not os.path.exists(sub_directory_path):
            os.makedirs(sub_directory_path)
            print("Created " + sub_directory_path + "directory")


def download_and_save_data(interval, target_year, overwrite):

    with open("data/top-20-spx-companies-by-market-cap-by-year.json", 'r') as f:
        top_20_spx_companies_by_market_cap_by_year = json.load(f)

    years = []
    if target_year == -1:
        years = top_20_spx_companies_by_market_cap_by_year.keys()
    else:
        years.append(str(target_year))

    for year in years:

        start = str(year) + "-01-01"
        end = str(year) + "-12-31"
        print("========== " + str(year) + " ==========")

        spx_csv_path = "data/spx/" + str(year) + "-" + interval + ".csv"
        if not overwrite and os.path.exists(spx_csv_path):
            print("Skipping SPX data (already exists)")
        else:
            print("Downloading SPX data")
            spx_close_prices = yf.download(tickers="^GSPC", start=start, end=end, interval=interval, auto_adjust=True, progress=False)["Close"]
            print("Saving SPX data")
            spx_close_prices.to_csv(path_or_buf=spx_csv_path, index=True)

        top_20_csv_path = "data/top-20/" + str(year) + "-" + interval + ".csv"
        if not overwrite and os.path.exists(top_20_csv_path):
            print("Skipping top 20 data (already exists)")
        else:
            company_tickers = []
            for company in top_20_spx_companies_by_market_cap_by_year[year].values():
                company_ticker = company["ticker"]
                company_tickers.append(company_ticker)

            print("Downloading top 20 SPX companies data")
            company_close_prices = yf.download(tickers=company_tickers, start=start, end=end, interval=interval, auto_adjust=True, progress=False)["Close"]
            print("Saving top 20 SPX companies data")
            company_close_prices.to_csv(path_or_buf=top_20_csv_path, index=True)
        
        time.sleep(2)

if __name__ == "__main__":
    setup_directory(directory="data")
    download_and_save_data(interval="1mo", target_year=2020, overwrite=False)