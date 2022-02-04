import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

fixed_price_df = pd.read_csv('fixed_price.csv')
trading_df = pd.read_csv('Trading.csv')

fp_df = fixed_price_df[['기준일자', 'fixed_price']]
tri_df = trading_df[['AsOfDate', 'TotalReturnIndex', 'AdjustedNAV', 'NAV', 'DailyReturn']].copy()
tri_df['AsOfDate'] = pd.to_datetime(tri_df['AsOfDate'])
fp_df['기준일자'] = pd.to_datetime(fp_df['기준일자'])

df = pd.merge(tri_df, fp_df, left_on='AsOfDate', right_on='기준일자')
df = df.drop(columns='기준일자').set_index('AsOfDate')

df = df.loc['2006-04-02':'2022-01-25']

df['adjnav_pc'] = df['AdjustedNAV'].pct_change()
df['FP_pc'] = df['fixed_price'].pct_change()
df['nav_chg'] = df['NAV'].pct_change()

tr_sr = df['adjnav_pc'] + 1
fp_sr = df['FP_pc'] + 1

tr_sr.iloc[0] = 1000
fp_sr.iloc[0] = 1000

df['adjnav_pc'] = tr_sr.cumprod()
df['FP'] = fp_sr.cumprod()

df = df[['adjnav_pc', 'FP']]

df = df.reset_index()
df['AsOfDate'] = pd.to_datetime(df['AsOfDate'], format='%Y-%m-%d')
df = df.set_index(['AsOfDate'])

fig, axes = plt.subplots()
axes.plot(df['adjnav_pc'], '-r', label='AdjNAV')
axes.plot(df['FP'], '-b', label='FixedPrice')
axes.axis('equal')
axes.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
axes.xaxis.set_major_locator(mdates.YearLocator())
plt.xticks(rotation=45)
leg = axes.legend()

plt.show()
