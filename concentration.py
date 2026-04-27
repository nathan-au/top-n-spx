import pandas as pd
import matplotlib.pyplot as plt
import json

with open("data/top-20-vs-spx-market-cap-by-year.json", "r") as f:
    top_20_vs_spx_market_cap_by_year = json.load(f)

df = pd.DataFrame(top_20_vs_spx_market_cap_by_year).T

df["top_20"] = df["top_20_market_cap"].str.replace("T", "").astype(float)
df["spx"] = df["spx_market_cap"].str.replace("T", "").astype(float)
df = df.drop(columns=["top_20_market_cap", "spx_market_cap"])

df.index = df.index.astype(int)
df = df.sort_index()

df["concentration"] = (df["top_20"] / df["spx"]) * 100

print(df)

plt.plot(df.index, df["concentration"])
plt.title("Market Cap Concentration of Top 20 SPX Companies")
plt.xlabel("Year")
plt.ylabel("Percentage")
plt.grid()
plt.show()