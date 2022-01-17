import pandas as pd

df = pd.read_csv('raw_data2.csv', index_col=0)
df = df.astype(float)
df.index = pd.to_datetime(df.index)
df = df.ffill().bfill()


y_df = df.resample('Y').last().pct_change().dropna(axis=0, how='all').copy()
y_df.index = y_df.index.strftime('%Y')
y_df = y_df.append(((y_df.iloc[:-1] + 1).mean() - 1).rename('CAGR'))
y_df.to_csv('C:/Users/user/Desktop/y_returns.csv')