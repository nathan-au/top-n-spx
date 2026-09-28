# Data as of April 24, 2026, 16:00 ET
# top-20-spx-companies-by-market-cap-by-year.json
# top-20-vs-spx-market-cap-by-year.json

import json
import yfinance as yf
import os
import time

def setup_directory(directory):
    sub_directories = ["spx", "held"]

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
            # ^SP500TR is the S&P 500 TOTAL RETURN index (dividends reinvested), not the
            # price-only ^GSPC. The held stocks are downloaded with auto_adjust=True (total
            # return), so the benchmark must also be total return or it understates SPX by
            # ~1.5-2%/year of forgone dividends, making the strategy look better than it is.
            spx_close_prices = yf.download(tickers="^SP500TR", start=start, end=end, interval=interval, auto_adjust=True, progress=False)["Close"]
            print("Saving SPX data")
            spx_close_prices.to_csv(path_or_buf=spx_csv_path, index=True)

        time.sleep(2)

def download_and_save_held_data(interval, target_year, overwrite):
    # Prices for the stocks HELD during a year: the previous year-end top 20, from December of
    # the previous year (the purchase price) through December of the target year.
    with open("data/top-20-spx-companies-by-market-cap-by-year.json", 'r') as f:
        top_20_spx_companies_by_market_cap_by_year = json.load(f)

    years = []
    if target_year == -1:
        for year in top_20_spx_companies_by_market_cap_by_year.keys():
            # 2026 is still in progress (the JSON's "2026" entry is a live snapshot, not a
            # year-end close), and the backtest only ever runs through 2025, so skip it here too.
            if int(year) > 2025:
                continue
            if str(int(year) - 1) in top_20_spx_companies_by_market_cap_by_year:
                years.append(year)
    else:
        years.append(str(target_year))

    for year in years:

        prior_year = str(int(year) - 1)
        start = prior_year + "-12-01"
        end = str(year) + "-12-31"
        print("========== " + str(year) + " (held: " + prior_year + " top 20) ==========")

        held_csv_path = "data/held/" + str(year) + "-" + interval + ".csv"
        if not overwrite and os.path.exists(held_csv_path):
            print("Skipping held data (already exists)")
            continue

        company_tickers = []
        for company in top_20_spx_companies_by_market_cap_by_year[prior_year].values():
            company_tickers.append(company["ticker"])

        print("Downloading held top 20 SPX companies data")
        held_close_prices = yf.download(tickers=company_tickers, start=start, end=end, interval=interval, auto_adjust=True, progress=False)["Close"]
        print("Saving held top 20 SPX companies data")
        held_close_prices.to_csv(path_or_buf=held_csv_path, index=True)

        time.sleep(2)

if __name__ == "__main__":
    setup_directory(directory="data")
    download_and_save_data(interval="1mo", target_year=-1, overwrite=False)
    download_and_save_held_data(interval="1mo", target_year=-1, overwrite=False)