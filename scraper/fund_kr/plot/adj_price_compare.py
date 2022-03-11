import matplotlib.pyplot as plt
from matplotlib import rc
from scraper.fund_kr.api.fund_daily_by_ticker import get_adj_pr
from scraper.fund_kr.api.backup import get_fund_name_sr
import pymysql
import sqlalchemy
import os
import pandas as pd
from scraper.common import get_engine_read

rc('font', family='AppleGothic')
plt.rcParams['axes.unicode_minus'] = False


def add_kfr_data(ticker):
    df = get_adj_pr(ticker)

    connect = pymysql.connect(
        host='dev-richgo-finance-instance-1.ca4ksn7jhida.ap-northeast-2.rds.amazonaws.com',
        user='rf_read',
        password=os.getenv('FUND_READ_PW'),
        db='fund_kr',
        port=2206
    )

    query = f"select AsOfDate, Symbol, AdjustedNAV from Trading where Symbol = '{ticker}'"
    # kfr_df = pd.read_sql(query, connect)
    # print(kfr_df)

    try:
        with connect.cursor() as cur:
            query = f"select AsOfDate, Symbol, AdjustedNAV from Trading where Symbol = '{ticker}'"
            cur.execute(query)
            # connect.commit()
            kfr_df = cur.fetchall()
            kfr_df = pd.DataFrame(kfr_df)
            kfr_df.columns = ['date', 'code', 'price']
            print(kfr_df)
    finally:
        connect.close()

    # kfr_df = kfr_df.rename(columns={'AsOfDate': 'date',
    #                                 'Symbol': 'code',
    #                                 'AdjustedNAV': 'price'})
    # kfr_df.columns = ['date', 'code', 'price']

    kfr_one = kfr_df[kfr_df['code'] == ticker].copy()
    kfr_one['date'] = pd.to_datetime(kfr_one['date'])
    kfr_one['date'] = kfr_one['date'].dt.strftime('%Y-%m-%d')
    kfr_one = kfr_one.set_index(['date', 'code'])
    df['kfr_pr'] = kfr_one['price']
    adj_df = df.reset_index().set_index('base_dt')
    adj_df.index = pd.to_datetime(adj_df.index)
    return adj_df


def show_graphs(ticker, base_dt):
    fig, axes = plt.subplots()
    axes.plot(add_kfr_data(ticker)['adj_pr'], '-b', label='KOFIA_Adjusted_Price')
    axes.plot(add_kfr_data(ticker)['kfr_pr'], '-r', label='KFR_Adjusted_NAV')
    axes.axis('equal')
    plt.xticks(rotation=45)
    code_name_sr = get_fund_name_sr(base_dt)
    # plt.title(f'{code_name_sr.loc[ticker].iloc[0]}')
    plt.title(f'{code_name_sr.loc[ticker]}')
    axes.legend()
    plt.show()
    # plt.savefig(f'{n}.png')
