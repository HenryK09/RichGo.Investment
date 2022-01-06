import pandas as pd

kospi = pd.read_csv('C:/Users/user/Desktop/practice_data/tiger_kospi200.csv', encoding='cp949', index_col=1)
sp500 = pd.read_csv('C:/Users/user/Desktop/practice_data/tiger_sp500.csv', encoding='cp949', index_col=1)
nikkei225 = pd.read_csv('C:/Users/user/Desktop/practice_data/tiger_nikkei225.csv', encoding='cp949', index_col=1)
csi300 = pd.read_csv('C:/Users/user/Desktop/practice_data/tiger_csi300.csv', encoding='cp949', index_col=1)

abc

kospi.index = pd.to_datetime(kospi.index)
sp500.index = pd.to_datetime(sp500.index)
nikkei225.index = pd.to_datetime(nikkei225.index)
csi300.index = pd.to_datetime(csi300.index)

kospi_pt = pd.pivot_table(kospi, index = 'date',
                          columns = 'asset_name',
                          values = 'price')
sp500_pt = pd.pivot_table(sp500, index = 'date',
                          columns = 'asset_name',
                          values = 'price')
nikkei225_pt = pd.pivot_table(nikkei225, index = 'date',
                              columns = 'asset_name',
                              values = 'price')
csi300_pt = pd.pivot_table(csi300, index = 'date',
                           columns = 'asset_name',
                           values = 'price')

df = pd.merge(kospi_pt, sp500_pt, how='left', on='date')
df = pd.merge(df, nikkei225_pt, how='left', on= 'date')
df = pd.merge(df, csi300_pt, how='left', on='date')

#resample daily data와 비교
# -> resample('M').last() = daily data의 마지막 날짜의 값과 동일
# -> resample('MS').first() = daily data의 첫번째 날짜의 값과 동일

ml_df = df.resample('M').last().copy()
mf_df = df.resample('MS').first().copy()

df = df.reset_index()
df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d')
df['date'] = df['date'].dt.strftime('%Y-%m-%d')
df = df.set_index('date')

# 월별 마지막 날짜로 이루어진 데이터
ml_df = ml_df.reset_index()
ml_df['date'] = ml_df['date'].dt.strftime('%Y-%m-%d')
# 월별 첫째 날로 이루어진 데이터
mf_df = mf_df.reset_index()
mf_df['date'] = mf_df['date'].dt.strftime('%Y-%m-%d')
# 날짜를 인덱스로 하는 데이터프레임 형성
ml_pt = ml_df.set_index('date')
mf_pt = mf_df.set_index('date')



import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# describe
df.describe().T
df.describe(percentiles=[0.01, 0.03, 0.99]).T.head()

# unique(), value_counts()
df.nunique()
df['TIGER 200'].unique()
df['TIGER 200'].value_counts(normalize=True) # 정규화

# 정렬
df.nsmallest(5, 'TIGER 200').nlargest(5,'TIGER 차이나CSI300')
df.sort_values(['TIGER 200','TIGER 미국S&P500선물(H)'], ascending=[False,True]) # 앞에 값이 중복될 경우 뒤에 값으로 정렬

# Subset 추출
# Subset 추출하기 by columns
df.filter(like="S")
df.filter(regex='일\w+5')
# Subset 추출하기 by dtype
df.select_dtypes(include=['float'])
# Subset 추출하기 by row
df.iloc[[0,2]]
df.T.loc['TIGER 200']
df.T.loc['TIGER 200']['2020-03-02']
df.loc[['2021-07-08','2021-09-08'], 'TIGER 200']
# range indexing(:)
df.loc['2021-08-01':'2021-09-30', 'TIGER 200']
df.iloc[[0,10], :]
df.iloc[[2,44],[1,2]]
# Subset 추출하기 by at
df.at['2020-03-04','TIGER 200']


# all(), any()
a = df['TIGER 200'] > 0
a.all()
a.any()

# Top 5 수익률 날짜 필터링
df['TIGER 200'].nlargest(5).index

# Dealing with nan value
5 > np.nan # => False
(df['TIGER 차이나CSI300'] == np.nan).any() # !이런식으로 check하면 nan값 0개 나옴
# Nan checking
df['TIGER 차이나CSI300'].hasnans
df.isnull()
df.isnull().any(axis=0) # 각 칼럼별로 nan이 하나라도 있는지에 대해서 bool값으로 나타냄
df['TIGER 차이나CSI300'].isna().sum()
df2 = df.copy().fillna(0)

# 두 개의 DataFrame이 같은지 판단하려면, equals 사용하기
df['TIGER 200'].equals(df['TIGER 차이나CSI300'])


# 수익률 구하기
df['rtn_kospi'] = df['TIGER 200'].pct_change()

# cut(), qcut()
df2_cuts = pd.cut(df['rtn_kospi'], [-np.inf, 0, np.inf])
df2_cuts_counts = df2_cuts.value_counts()
# cut()과 동시에 label 달아주기
bins = [-np.inf, 0, np.inf]
labels = ['손실','이익']
df_cuts = pd.cut(df['rtn_kospi'], bins=bins, labels=labels)
# qcut() 함수로 수익률 그룹 나누기
df2['rtn_kospi'] = df2['TIGER 200'].pct_change().shift(-1)
df2.loc[:, 'rtn_score'] = pd.qcut(df['rtn_kospi'], 10, labels=range(1,11))
df2['rtn_score'].value_counts()

# groupby() & aggregation
df2_obj = df2.groupby(['rtn_score','rtn_kospi'])
df2_obj.size().to_frame()

rtn_df = df2.groupby('rtn_score').agg({'rtn_kospi':'mean'})
rtn_df.plot(kind='bar')

# index가 하나라도 관여하면 join()
# 둘 다 column에 맞춰야하면 merge()

# Stateless(object-oriented)
fig, axes = plt.subplots(nrows=2, ncols=1, figsize = (15,3), sharex=True)
ax1 = axes[0]
ax2 = axes[1]
ax1.plot(df2['rtn_kospi'].index, df2['date'].index, linewidth=2, linestyle='--', label='rtn');
_ = ax1.set_title('kospi rtn', fontsize=15, family='Arial');
_ = ax1.set_ylabel('rtn', fontsize=15, family='Arial');
_ = ax1.set_xlabel('date', fontsize=15, family='Arial');
ax1.legend(loc="upper left")

ax2.bar(df.index, df, label='rtn');
_ = ax2.set_title('kospi rtn', fontsize=15, family='Arial');
_ = ax2.set_ylabel('rtn', fontsize=15, family='Arial');
_ = ax2.set_xlabel('date', fontsize=15, family='Arial');
ax2.legend(loc="upper left")

ipynb_py_convert /PycharmProjects/krx_data_crawl/etf_month_pivot.py /PycharmProjects/krx_data_crawl/etf_M_pivot.ipynb