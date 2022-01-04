import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv('C:/Users/user/Desktop/inflearn_pandas_part1_material/my_data/fin_statement_new.csv')

df = df.drop(['결산월','상장일'], axis=1)

df = df.rename(columns={"P/E(Adj., FY End)": "PER",
                        'P/B(Adj., FY End)': "PBR",
                        'P/FCF1(Adj., FY End)': 'PSR'})

# Filter
# ROA >= 0.5
filtered_df = df[df['ROA'] >= 0.05]
# 부채비율 <= 0.5
filtered_df['부채비율'] = filtered_df['비유동부채'] / filtered_df['자산총계']
filtered_df = filtered_df[filtered_df['부채비율'] <= 0.5]

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