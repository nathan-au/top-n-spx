import yfinance as yf

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