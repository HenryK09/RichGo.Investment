import pandas as pd
import numpy as np
import FundCrawler as fc
import matplotlib.pyplot as plt
import datetime as dt


code_list = ['K55207BU0715',
             'K55370BU1789',
             'K55235BW6898',
             'K55307D05118',
             'K55213BX5796',
             'K55105BV3695',
             'K55229BU7300',
             'K55101BT7462',
             'K55301BV2426',
             'K55232BU5747',
             'K55370BU1987',
             'K55235BO4158',
             'K55235BY9403',
             'K55102BT6570',
             'K55213DA8043',
             'K55105D00562',
             'K55234CJ0997',
             'K55105D17574',
             'K55107D40440',
             'K55210BU2435',
             'K55105BT9928',
             'K55301BU6253',
             'K55207CP6031',
             'K55101BT7397',
             'K55223BT1450'
             ]

def crawling():

    adj_pr_list = []
    for c in code_list:
        adj_pr = fc.AdjStdPrice(c)
        adj_pr['code'] = c
        adj_pr_list.append(adj_pr)
    adj_pr_df = pd.concat(adj_pr_list)

    fund_data = []
    for c in code_list:
        funds = fc.fund_crawling(c, 20170101, 20220208)
        funds['code'] = c
        fund_data.append(funds)
    price_df = pd.concat(fund_data)

    return adj_pr_df, price_df

# adj_pr_df, price_df = crawling()

def to_csv():
    adj_pr_df.to_csv('~/dataknows/RichGo.Investment/adj_price/adj_pr.csv')
    price_df.to_csv('~/dataknows/RichGo.Investment/adj_price/fund_pr.csv')

# to_csv()

def read_data():

    adj_pr_df = pd.read_csv('adj_pr.csv')
    price_df = pd.read_csv('fund_pr.csv')
    kfr_df = pd.read_csv('kfr_Trading.csv')

    return adj_pr_df, price_df, kfr_df

adj_pr_df, price_df, kfr_df = read_data()


def pre_setting():

    adj_pr_df, price_df, kfr_df = read_data()

    adj_pr_df = adj_pr_df[['code', 'trustAccend', 'standardCot']].copy()
    adj_pr_df['trustAccend'] = pd.to_datetime(adj_pr_df['trustAccend'], format='%Y%m%d')
    adj_pr_df = adj_pr_df.sort_values(['code', 'trustAccend'], ascending=True)

    price_df = price_df[['code', 'standardDt', 'standardCot']].copy()
    price_df['standardDt'] = pd.to_datetime(price_df['standardDt'], format='%Y%m%d')
    price_df = price_df.sort_values(['code', 'standardDt'], ascending=True)

    return adj_pr_df, price_df

adj_pr_df, price_df = pre_setting()


one_pr = price_df[price_df['code'] == 'K55207BU0715']
one_adj = adj_pr_df[adj_pr_df['code'] == 'K55207BU0715']


one_sr = one_pr.set_index('standardDt')['standardCot']

one_adj['trustAccend'] = pd.to_datetime(one_adj['trustAccend'])
one_adj['trustAccend'] = one_adj['trustAccend'] + dt.timedelta(days=1)
end_date = one_adj['trustAccend'].tolist()

dvdnd_dt = []
for d in end_date:
    dvdnd_dt.append(one_sr.index[one_sr.index.get_loc(f'{d}', method='bfill')])

# one_df = one_adj.reindex(dvdnd_dt)
# one_df['code'] = 'K55207BU0715'
# one_df['standardCot'] = [1080.07000, 898.56000, 1016.87000, 1288.56000, 1404.72000]
one_adj.index = dvdnd_dt

one_df = one_adj.drop(columns=['code','trustAccend']).rename(columns={'standardCot':'dvdnd_pr'})

one_pr = one_pr.set_index('standardDt')
one_pr = one_pr.join(one_df, how='outer')

# one_pr['adj_pr'] = one_pr.replace(np.nan, one_pr['standardCot'])
# one_pr['dly_rtn'] = one_pr['standardCot'].pct_change


kfr_df.columns = ['date','code','price']
kfr_one = kfr_df[kfr_df['code'] == 'K55207BU0715']
kfr_one['date'] = pd.to_datetime(kfr_one['date'], format='%Y-%m-%d')
kfr_one = kfr_one.set_index('date')

one_pr['kfr_pr'] = kfr_one['price']
one_pr['dv_price'] = np.where(one_pr['dvdnd_pr'].notna(), one_pr.dvdnd_pr, one_pr.standardCot)
one_pr['dly_rtn_notna'] = np.where(one_pr['dvdnd_pr'].notna(), one_pr.dv_price.pct_change(), one_pr.dv_price/(one_pr.standardCot.shift(1)))
one_pr['dly_rtn_isna'] = np.where(one_pr['dvdnd_pr'].isna(), one_pr.dv_price.pct_change(), one_pr.dv_price/(one_pr.standardCot.shift(1)))

dividend_dates = one_pr['dvdnd_pr'].dropna().index
one_pr['dly_rtn_notna'][dividend_dates] = one_pr['dly_rtn_isna'][dividend_dates]

one_pr['adj_pr'] = one_pr['dly_rtn_notna']
one_pr['adj_pr'].iloc[0] = one_pr['dv_price'].iloc[0]
one_pr['adj_pr'] = one_pr['adj_pr'].cumprod()
# one_pr['adj_pr'] = one_pr.adj_pr * one_pr.dly_rtn_notna.shift(-1)

one_pr = one_pr.drop(columns='dly_rtn_isna').rename(columns={'dly_rtn_notna':'dly_rtn'})

# one_pr.to_csv('')


# num_list = list(range(0,1105))
# for i in num_list:
#     one_pr['dv_price'] = np.where(one_pr.dvdnd_pr.iloc[i]==np.nan, one_pr.standardCot.iloc[i], one_pr.dvdnd_pr.iloc[i])
#
#
# for i in
# if one_pr['dvdnd_pr'].loc() == np.nan:
#     one_pr['dv_price'] = one_pr['standardCot'].values
# else:
#     one_pr['dv_price'] = one_pr['dvdnd_pr']
#
# one_pr['dly_rtn'] =

one_pr = price_df[price_df['code'] == 'K55207BU0715']
one_adj = adj_pr_df[adj_pr_df['code'] == {'K55207BU0715'}]

one_sr = one_pr.set_index('standardDt')['standardCot']

one_adj['trustAccend'] = pd.to_datetime(one_adj['trustAccend'])
one_adj['trustAccend'] = one_adj['trustAccend'] + dt.timedelta(days=1)
end_date = one_adj['trustAccend'].tolist()

dvdnd_dt = []
for d in end_date:
    dvdnd_dt.append(one_sr.index[one_sr.index.get_loc(f'{d}', method='bfill')])

one_adj.index = dvdnd_dt

one_df = one_adj.drop(columns=['code', 'trustAccend']).rename(columns={'standardCot': 'dvdnd_pr'})

one_pr = one_pr.set_index('standardDt')
one_pr = one_pr.join(one_df, how='outer')

kfr_df.columns = ['date', 'code', 'price']
kfr_one = kfr_df[kfr_df['code'] == {'K55207BU0715'}]
kfr_one['date'] = pd.to_datetime(kfr_one['date'], format='%Y-%m-%d')
kfr_one = kfr_one.set_index('date')

one_pr['kfr_pr'] = kfr_one['price']
one_pr['dv_price'] = np.where(one_pr['dvdnd_pr'].notna(), one_pr.dvdnd_pr, one_pr.standardCot)
one_pr['dly_rtn_notna'] = np.where(one_pr['dvdnd_pr'].notna(), one_pr.dv_price.pct_change(),
                                   one_pr.dv_price / (one_pr.standardCot.shift(1)))
one_pr['dly_rtn_isna'] = np.where(one_pr['dvdnd_pr'].isna(), one_pr.dv_price.pct_change(),
                                  one_pr.dv_price / (one_pr.standardCot.shift(1)))

dividend_dates = one_pr['dvdnd_pr'].dropna().index
one_pr['dly_rtn_notna'][dividend_dates] = one_pr['dly_rtn_isna'][dividend_dates]

one_pr['adj_pr'] = one_pr['dly_rtn_notna']
one_pr['adj_pr'].iloc[0] = one_pr['dv_price'].iloc[0]
one_pr['adj_pr'] = one_pr['adj_pr'].cumprod()
# one_pr['adj_pr'] = one_pr.adj_pr * one_pr.dly_rtn_notna.shift(-1)

one_pr = one_pr.drop(columns='dly_rtn_isna').rename(columns={'dly_rtn_notna': 'dly_rtn'})

dropna_df = one_pr.dropna()

def plot_rtn():
    fig, axes = plt.subplots()
    axes.plot(one_pr['kfr_pr'], '-r', label='KFR_Adjusted_NAV')
    axes.plot(one_pr['adj_pr'], '-b', label='KOFIA_Adjusted_Price')
    axes.axis('equal')
    # axes.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
    # axes.xaxis.set_major_locator(mdates.YearLocator())
    plt.xticks(rotation=45)
    axes.legend()

    plt.show()


# one_pr.to_csv('~/dataknows/RichGo.Investment/adj_price/one_pr_v2.csv')


# kfr_df = kfr_df.pivot(index='date', columns='code', values='price')




