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