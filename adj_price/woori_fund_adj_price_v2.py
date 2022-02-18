import pandas as pd
import numpy as np
import FundCrawler as fc
import datetime


code_list = ['K55207BU0715',
             # 'K55370BU1789',
             # 'K55235BW6898',
             # 'K55307D05118',
             # 'K55213BX5796',
             # 'K55105BV3695',
             # 'K55229BU7300',
             # 'K55101BT7462',
             # 'K55301BV2426',
             # 'K55232BU5747',
             # 'K55370BU1987',
             # 'K55235BO4158',
             # 'K55235BY9403',
             # 'K55102BT6570',
             # 'K55213DA8043',
             # 'K55105D00562',
             # 'K55234CJ0997',
             # 'K55105D17574',
             # 'K55107D40440',
             # 'K55210BU2435',
             # 'K55105BT9928',
             # 'K55301BU6253',
             # 'K55207CP6031',
             # 'K55101BT7397',
             # 'K55223BT1450'
             ]

adj_pr_list = []
for c in code_list:
    adj_pr = fc.AdjStdPrice(c)
    adj_pr['code'] = c
    adj_pr_list.append(adj_pr)

adj_pr_df = pd.concat(adj_pr_list)
adj_pr_df = adj_pr_df[['code', 'trustAccend', 'standardCot']].copy()
adj_pr_df['trustAccend'] = pd.to_datetime(adj_pr_df['trustAccend'], format='%Y%m%d')
adj_pr_df = adj_pr_df.sort_values(['code', 'trustAccend'], ascending=True)
# adj_pr_df = adj_pr_df.set_index(['code', 'trustAccend'])
# adj_pr_df = adj_pr_df.pivot(index='trustAccend', columns='code', values='standardCot')
# adj_pr_df.index = pd.to_datetime(adj_pr_df.index, format='%Y%m%d')
# adj_pr_df.index = adj_pr_df.index + datetime.timedelta(days=1)


price_sr.index[price_sr.index.get_loc('20201218')+1]


fund_data = []
for c in code_list:
    funds = fc.fund_crawling(c, 20170101, 20220208)
    funds['code'] = c
    fund_data.append(funds)

price_df = pd.concat(fund_data)
price_df = price_df[['code', 'standardDt', 'standardCot']].copy()
price_df['standardDt'] = pd.to_datetime(price_df['standardDt'], format='%Y%m%d')
price_df = price_df.sort_values(['code', 'standardDt'], ascending=True)
price_sr = price_df.set_index('standardDt')['standardCot']
kkk = 0
# price_df = price_df.set_index(['code', 'standardDt'])
# price_df = price_df.pivot(index='standardDt', columns='code', values='standardCot')
# price_df.index = pd.to_datetime(price_df.index, format='%Y%m%d')

# std_pr_df = price_df.join(adj_pr_df, how='outer', lsuffix='_std', rsuffix='_adj')

#
#
# price_df = price_df.reset_index()
# adj_pr_df = adj_pr_df.reset_index()
# std_pr_df = pd.merge(adj_pr_df, price_df, how='inner', left_on='trustAccend', right_on='standardDt')
# price_df.replace()


# full_date = pd.date_range('20170727', '20220208')
# adj_pr_df = adj_pr_df.reindex(full_date)
# price_df = price_df.reindex(full_date)
#
#
#
#
#
# n=0
# while n <= (price_df.index.nunique() + adj_pr_df.nunique()):
#     if (adj_pr_df.iloc[n] != np.nan) and (price_df.iloc[n] != np.nan):
#         price_df.replace(price_df.values, adj_pr_df.values)
#     else:
#         adj_pr_df.iloc[n] + datetime.timedelta(days=1)
#     n = n + 1
#
#
#
# # std_pr_df = price_df.replace(adj_pr_df)
# std_pr_df = price_df.join(adj_pr_df, how='right', lsuffix='_std', rsuffix='_adj')
# # std_pr_df