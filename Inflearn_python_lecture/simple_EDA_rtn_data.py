import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv('C:/Users/user/Desktop/inflearn_pandas_part1_material/my_data/fin_statement_new.csv')

df = df.drop(['결산월','상장일'], axis=1) # 필요없는 열 제거

df = df.rename(columns={"P/E(Adj., FY End)": "PER",
                        'P/B(Adj., FY End)': "PBR",
                        'P/FCF1(Adj., FY End)': 'PSR'})

# companies by each year
df.groupby(['year'])['Name'].count()
# code-name mapping
df.groupby(['year'])['Name'].nunique()
df.groupby(['year'])['Code'].nunique() # 갯수만으로는 정확한 비교 불가
df.groupby(['year'])['Name'].nunique().equals(df.groupby(['year'])['Code'].nunique()) # => True
df.groupby(['year','Name'])['Code'].nunique().nunique() # => 1; code-name align
# yearly returns
yearly_price_df = df.pivot(index='year', columns='Name', values='수정주가')
# shift(-1) = xx년도에 xx만큼 수익이 났다고 해석하기 위함
yearly_rtn_df = yearly_price_df.pct_change(fill_method=None).shift(-1) # lagging 할 때 씀
yearly_rtn_df.isna().sum()

# top_n
indicator = 'ROA'
top_n = 10
roa_df = df.groupby(['year'])[indicator].nlargest(top_n).reset_index()
top_roa_df = df.loc[roa_df['level_1']]
indicator_df = top_roa_df.pivot(index='year', columns='Name', values='ROA')

asset_on_df = indicator_df.notna().astype(int).replace(0, np.nan)
# notna() -> nan값이 아닌 값을 True로 반환
# astype(int) -> True = 1, False = 0
# replace(0, np.nan) -> 나중에 데이터프레임끼리 곱할 때 수익률이 0인 것과 구분해주기 위함

selected_rtn_df = yearly_rtn_df * asset_on_df
selected_rtn_df.notna().sum(axis=1)

# 자주 쓸 코드 함수화
def get_rtn_sr(selected_rtn_df):
    rtn_sr = selected_rtn_df.mean(axis=1)
    cum_rtn_sr = (rtn_sr + 1).cumprod().dropna() # 누적수익률 구한 후 nan값 제거

    return rtn_sr, cum_rtn_sr

def plot_rtn(cum_rtn_sr, rtn_sr):
    fig, axes = plt.subplots(nrows=2, figsize=(15, 6), sharex=True)
    axes[0].plot(cum_rtn_sr.index, cum_rtn_sr, marker='o');
    axes[0].set_title('Cum return(line)');
    axes[1].bar(rtn_sr.index, rtn_sr);
    axes[1].set_title('yearly return(bar)')

# quantile
qt_y_sr = df.groupby(['year'])[indicator].quantile(0.9) # indicator = ROA, quantile(0.9) -> 이상치 제거
qt_indicator_df = df.join(qt_y_sr, how='left', on='year', rsuffix='_quantile')
qt_indicator_df = qt_indicator_df[
    qt_indicator_df[indicator] >= qt_indicator_df['{}_quantile'.format(indicator)]
]
qt_indicator_df.groupby('year')['Code'].count() # 연도별 위 조건에 해당되는 종목코드 개수 추출

indicator_df2 = df.loc[qt_indicator_df.index].pivot(index='year', columns='Name', values=indicator)
asset_on_df2 = indicator_df2.notna().astype(int).replace(0,np.nan)
selected_rtn_df2 = yearly_rtn_df * asset_on_df2

get_rtn_sr(selected_rtn_df2)
plot_rtn(cum_rtn_sr, rtn_sr)
