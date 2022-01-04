import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv('C:/Users/user/Desktop/inflearn_pandas_part1_material/my_data/fin_statement_new.csv')

df = df.drop(['결산월','상장일'], axis=1)

df = df.rename(columns={"P/E(Adj., FY End)": "PER",
                        'P/B(Adj., FY End)': "PBR",
                        'P/FCF1(Adj., FY End)': 'PSR'})

# Filter
# 시가총액 하위 20%
market_cap_qt_sr = df.groupby('year')['시가총액'].quantile(.2)
filtered_df = df.join(market_cap_qt_sr, on='year', how='left', rsuffix='20%_quantile')
filtered_df = filtered_df[filtered_df['시가총액'] <= filtered_df['시가총액20%_quantile']]

# Selector
# PBR >= 0.2 중 PBR 작은 20개 종목
filtered_df = filtered_df[filtered_df['PBR'] >= 0.2]

smallest_pbr_sr = filtered_df.groupby('year')['PBR'].nsmallest(20)
selected_ix = smallest_pbr_sr.index.get_level_values(1)

selector_df = filtered_df.loc[selected_ix].pivot(
    index='year', columns='Name', values='PBR'
)

yearly_price_df = df.pivot(index='year', columns='Name', values='수정주가')
yearly_rtn_df = yearly_price_df.pct_change(fill_method=None).shift(-1)
asset_on_df = selector_df.notna().astype(int).replace(0, np.nan)
selector_rtn_df = yearly_rtn_df * asset_on_df

rtn_sr = selector_rtn_df.mean(axis=1)
cum_rtn_sr = (rtn_sr + 1).cumprod().dropna()

def get_rtn_sr(selector_rtn_df):
    rtn_sr = selector_rtn_df.mean(axis=1)
    cum_rtn_sr = (rtn_sr + 1).cumprod().dropna()
    return rtn_sr, cum_rtn_sr

def plot_rtn(cum_rtn_sr, rtn_sr):
    fig, axes = plt.subplots(nrows=2, figsize=(15, 6), sharex=True)
    axes[0].plot(cum_rtn_sr.index, cum_rtn_sr, marker='o');
    axes[0].set_title('Cum return(line)');
    axes[1].bar(rtn_sr.index, rtn_sr);
    axes[1].set_title('yearly return(bar)')

rtn_sr, cum_rtn_sr = get_rtn_sr(selector_rtn_df)
plot_rtn(cum_rtn_sr, rtn_sr)