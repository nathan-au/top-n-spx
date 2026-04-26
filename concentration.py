import pandas as pd
import matplotlib.pyplot as plt
import json

with open("data/top-20-vs-spx-market-cap-by-year.json", 'r') as f:
    raw_data = json.load(f)

df = pd.DataFrame(raw_data).T

df['top_20_market_cap'] = df['top_20_market_cap'].str.replace('T', '').astype(float)
df['spx_market_cap'] = df['spx_market_cap'].str.replace('T', '').astype(float)

df.index = df.index.astype(int)
df = df.sort_index()

df['concentration_pct'] = (df['top_20_market_cap'] / df['spx_market_cap']) * 100

print(df)

plt.plot(df.index, df['concentration_pct'])
plt.title("Concentration of Top 20 SPX Companies")
plt.xlabel("Year")
plt.ylabel("Percentage")
plt.grid()
plt.show()