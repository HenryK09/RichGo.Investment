import pandas as pd
import numpy as np
import datetime as dt
import FundCrawler as fc


# todayFund_df = pd.read_csv(f"""~/dataknows/RichGo.Investment/{datetime.today().strftime('%Y%m%d')}.csv""", encoding='utf-8-sig')
# code_list = todayFund_df['펀드코드'].tolist()

code_list = ['K55207BU0715',
             'K55370BU1789',
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
        funds = fc.fund_crawling(c, 20170101, 20220218)
        funds['code'] = c
        fund_data.append(funds)
    price_df = pd.concat(fund_data)

    return adj_pr_df, price_df

# adj_pr_df, price_df = crawling()

def pre_setting():
    adj_pr_df, price_df = crawling()

    adj_pr_df = adj_pr_df[['code', 'trustAccend', 'standardCot']].copy()
    adj_pr_df['trustAccend'] = pd.to_datetime(adj_pr_df['trustAccend'], format='%Y%m%d')
    adj_pr_df = adj_pr_df.sort_values(['code', 'trustAccend'], ascending=True)

    price_df = price_df[['code', 'standardDt', 'standardCot', 'standardassStdCot', 'uOriginalAmt']].copy()
    price_df['standardDt'] = pd.to_datetime(price_df['standardDt'], format='%Y%m%d')
    price_df = price_df.sort_values(['code', 'standardDt'], ascending=True)

    return adj_pr_df, price_df

adj_pr_df, price_df = pre_setting()

def AdjustedPrice(code):
    one_pr = price_df[price_df['code'] == code].copy()
    one_adj = adj_pr_df[adj_pr_df['code'] == code].copy()

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

    one_pr = one_pr.drop(columns='dly_rtn_isna').rename(columns={'dly_rtn_notna': 'dly_rtn'})

    return one_pr

data_list = []
for f in code_list:
    data_list.append(AdjustedPrice(f))

df = pd.concat(data_list, axis=0)

df = df.reset_index()
daily_df = df.copy()
daily_df = daily_df.rename(columns={
    'code': 'ticker',
    'index': 'base_dt',
    'standardCot': 'nav',
    'standardassStdCot': 'tax_base_pr',
    'uOriginalAmt': 'aum'
}
)
daily_df = daily_df.drop(columns=['dvdnd_pr', 'dv_price', 'dly_rtn'])

def to_csv():
    daily_df.to_csv('~/dataknows/RichGo.Investment/productDaily.csv')

kkk=0