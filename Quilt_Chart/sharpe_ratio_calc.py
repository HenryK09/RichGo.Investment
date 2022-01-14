import pandas as pd
import numpy as np


df = pd.read_csv('raw_data.csv', encoding='utf-8-sig')
richgo_df = pd.read_csv('richgo_historical_data.csv', encoding='cp949')
brk_df = pd.read_csv('brk_a.csv',  encoding='utf-8-sig')

df = df.ffill().bfill()
df['Date'] = pd.to_datetime(df['Date'])
richgo_df['base_dt'] = pd.to_datetime(richgo_df['base_dt'])
brk_df['Date'] = pd.to_datetime(brk_df['Date'])
brk_df = brk_df.rename(columns={'Date':'date'})

richgo_df = richgo_df.pivot(index='base_dt', columns='name_kr', values='price')
richgo_df = richgo_df.reset_index()


df = pd.merge(df, richgo_df, left_on='Date', right_on='base_dt')
df = pd.merge(df, brk_df, left_on='Date', right_on='date')

df = df.drop(columns=['base_dt','date'])

df = df.set_index(['Date'])

df.index = pd.to_datetime(df.index)

price_sr = df.astype(float)
price_sr = price_sr.reindex(pd.date_range(pd.Timestamp(f'{price_sr.index[0].year}0101'), price_sr.index[-1]))
price_sr = price_sr.ffill().bfill()[:'20211231']

# 일별 수익률 계산
returns_df = price_sr.pct_change()

# 무위험이자율
riskfree_sr = pd.read_csv('daily_riskfree.csv')
riskfree_sr = riskfree_sr.rename(columns={'Unnamed: 0':'Date'})
riskfree_sr['Date'] = pd.to_datetime(riskfree_sr['Date'])
riskfree_sr = riskfree_sr.set_index('Date')
riskfree_sr = riskfree_sr.loc['2000-01-01':'2021-12-31']

#price_sr[pd.Timestamp(f'{price_sr.index[0].year - 1}1231')] = 1
yearly_returns_df = price_sr.resample('Y').last().pct_change()
yearly_riskfree_df = (riskfree_sr + 1).cumprod().resample('Y').last().pct_change()

yearly_returns_df = yearly_returns_df.rename(columns={'BRK/A':'BRK_A',
                                        'NDUEEGF Index': 'EM',
                                        'RMSG Index': 'REITs',
                                        'SPTRMDCP Index': 'Mid_Cap',
                                        'SPTRSMCP Index': 'Small_Cap',
                                        'NDDUEAFE Index': 'Intl_Stocks',
                                        'LBUTTRUU Index': 'TIPS',
                                        'LBUSTRUU Index': 'Bonds',
                                        'BCOMTR Index': 'Comdty',
                                        'LD12TRUU Index': 'Cash',
                                        'SPXT Index': 'Large_Cap',
                                        '리치고 성장형': '리치고_성장형',
                                        '리치고 안정형': '리치고_안정형',
                                        '리치고 중립형': '리치고_중립형'
                                        })
returns_df = returns_df.rename(columns={'BRK/A':'BRK_A',
                                        'NDUEEGF Index': 'EM',
                                        'RMSG Index': 'REITs',
                                        'SPTRMDCP Index': 'Mid_Cap',
                                        'SPTRSMCP Index': 'Small_Cap',
                                        'NDDUEAFE Index': 'Intl_Stocks',
                                        'LBUTTRUU Index': 'TIPS',
                                        'LBUSTRUU Index': 'Bonds',
                                        'BCOMTR Index': 'Comdty',
                                        'LD12TRUU Index': 'Cash',
                                        'SPXT Index': 'Large_Cap',
                                        '리치고 성장형': '리치고_성장형',
                                        '리치고 안정형': '리치고_안정형',
                                        '리치고 중립형': '리치고_중립형'
                                        })

# 연환산변동성
vol_y = returns_df.resample('Y').std(ddof=0) * np.sqrt(365)

names = returns_df.columns.tolist()
sr_list = []
for i in names:
    sharpe_ratio = (yearly_returns_df[f'{i}'] - yearly_riskfree_df['riskfree']) / vol_y[f'{i}']
    sr_list.append(sharpe_ratio)

sharpe_ratio_df = pd.DataFrame(sr_list)
sharpe_ratio_df['asset_name'] = names
sharpe_ratio_df = sharpe_ratio_df.set_index('asset_name')

sharpe_ratio_df.T.to_csv('C:/Users/user/Desktop/sharpe_ratio_data.csv', encoding='utf-8-sig')