import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rc
import requests
import json
from pandas import json_normalize
import matplotlib.dates as mdates
import quantstats as qs

rc('font', family='AppleGothic')
plt.rcParams['axes.unicode_minus'] = False


def fetch_data(market=None):
    today = pd.Timestamp.now(tz='Asia/Seoul').strftime('%Y%m%d')

    url = 'http://freesis.kofia.or.kr/meta/getMetaDataList.do'
    headers = {
        'Host': 'freesis.kofia.or.kr',
        'Origin': 'http://freesis.kofia.or.kr',
        'Referer': 'http://freesis.kofia.or.kr/stat/FreeSIS.do?parentDivId=MSIS10000000000000&serviceId=STATSCU0100000070'
    }
    credit_data = {"dmSearch": {
        "tmpV40": "1000000000",
        "tmpV41": "1",
        "tmpV1": "D",
        "tmpV45": "20110103",
        "tmpV46": f"{today}",
        "OBJ_NM": "STATSCU0100000070BO"
    }}
    request_credit = requests.post(url, json=credit_data, headers=headers).text
    cr_jl = json.loads(request_credit)
    cr_jn = json_normalize(cr_jl, 'ds1')
    credit_df = pd.DataFrame(cr_jn)
    credit_df = credit_df.drop(columns=['TMPV5', 'TMPV6', 'TMPV7', 'TMPV8', 'TMPV9'])
    credit_df = credit_df.rename(columns={
        'TMPV1': 'base_dt',
        'TMPV2': 'total_credit_loan',
        'TMPV3': 'kospi_credit_loan',
        'TMPV4': 'kosdaq_credit_loan',
    })
    credit_df['base_dt'] = pd.to_datetime(credit_df['base_dt'])
    sig_df = credit_df.sort_values('base_dt', ascending=True).set_index('base_dt')

    if market == kosdaq:
        market_data = {"dmSearch": {
            "tmpV40": "1000000000",
            "tmpV41": "10000",
            "tmpV1": "D",
            "tmpV45": "20110103",
            "tmpV46": f"{today}",
            "OBJ_NM": "STATSCU0100000030BO"
        }}
        sig_df = sig_df.rename(columns={'kosdaq_credit_loan': 'credit_loan'})
        sig_sr = sig_df['credit_loan']
    else:
        market_data = {"dmSearch": {
            "tmpV40": "1000000000",
            "tmpV41": "10000",
            "tmpV1": "D",
            "tmpV45": "20110103",
            "tmpV46": f"{today}",
            "OBJ_NM": "STATSCU0100000020BO"
        }}
        sig_df = sig_df.rename(columns={'kospi_credit_loan': 'credit_loan'})
        sig_sr = sig_df['credit_loan']

    request_market = requests.post(url, json=market_data, headers=headers).text
    load_mkt = json.loads(request_market)
    norm_mkt = json_normalize(load_mkt, 'ds1')
    mkt_df = pd.DataFrame(norm_mkt)
    mktcap_df = mkt_df[['TMPV1', 'TMPV5']]
    mktcap_df = mktcap_df.rename(columns={'TMPV1': 'base_dt',
                                          'TMPV5': 'mktcap'})
    mktcap_df['base_dt'] = pd.to_datetime(mktcap_df['base_dt'])
    mktcap_df = mktcap_df.sort_values('base_dt', ascending=True).set_index('base_dt')
    mktcap_sr = mktcap_df['mktcap']

    return sig_sr, mktcap_sr


def calc_disparity(sig_sr, mktcap_sr):
    df = pd.DataFrame([sig_sr, mktcap_sr]).T
    df['credit_rate'] = df['credit_loan'] / df['mktcap']
    df = df.ffill()
    df['moving_avrg'] = df['credit_rate'].rolling(20).mean()
    df['disparity'] = df['credit_rate'] - df['moving_avrg']
    return df


def catch_signal(market=None):
    if market == kosdaq:
        sig_sr, mktcap_sr = fetch_data(market)
        df = calc_disparity(sig_sr, mktcap_sr)
        threshold = 0.002
    else:
        sig_sr, mktcap_sr = fetch_data(market)
        df = calc_disparity(sig_sr, mktcap_sr)
        threshold = 0.0004

    df['short_signal'] = df['disparity'] > threshold
    df['short_signal'] = df['short_signal'].replace(False, "").replace(True, 0)
    df['long_signal'] = df['disparity'] < -threshold
    df['long_signal'] = df['long_signal'].replace(False, "").replace(True, 1)
    df['signal'] = df['short_signal'].astype(str) + df['long_signal'].astype(str)
    df['signal'] = df['signal'].replace("", np.nan)
    df['signal'].iloc[0] = 0.5
    df['signal'] = df['signal'].ffill()
    df.index = pd.to_datetime(df.index)

    return df


def load_data():
    today = pd.Timestamp.now(tz='Asia/Seoul').strftime('%Y%m%d')

    products_df = pd.read_csv('/Users/user/dataknows/richgo_growth_products_0321.csv')
    products_df = products_df.set_index('base_dt')
    products_df = products_df.loc['2011-01-03': today, :]
    products_df = products_df[['KBSTAR 200TR', 'TIGER 미국채10년선물']]
    products_df = products_df.pct_change() + 1
    products_df.iloc[0] = 100
    products_df = products_df.cumprod()
    return products_df


def calc_returns(mkt_df, products_df):
    products_df['stock_returns'] = products_df['KBSTAR 200TR'].pct_change()
    products_df['bond_returns'] = products_df['TIGER 미국채10년선물'].pct_change()

    sig_port_df = products_df.join(mkt_df['signal'], how='outer')
    sig_port_df.iloc[0] = sig_port_df.iloc[0].fillna(0)
    sig_port_df = sig_port_df.dropna()
    sig_port_df['signal'] = sig_port_df['signal'].astype(float)

    sig_port_df['port_rtns'] = ""

    for i in range(0, len(sig_port_df['signal'])):
        if sig_port_df['signal'].iloc[i] == 0.5:
            sig_port_df['port_rtns'].iloc[i] = 0.5 * (
                    sig_port_df['stock_returns'].iloc[i] + sig_port_df['bond_returns'].iloc[i])
        elif sig_port_df['signal'].iloc[i] == 0:
            sig_port_df['port_rtns'].iloc[i] = sig_port_df['bond_returns'].iloc[i]
        elif sig_port_df['signal'].iloc[i] == 1:
            sig_port_df['port_rtns'].iloc[i] = sig_port_df['stock_returns'].iloc[i]

    sig_port_df['port_rtns'] = sig_port_df['port_rtns'] + 1
    sig_port_df['port_rtns'].iloc[0] = 100
    sig_port_df['port_rtns'] = sig_port_df['port_rtns'].cumprod()

    sig_port_df.index = pd.to_datetime(sig_port_df.index)

    return sig_port_df


def show_chart(portfolio, sig_port_df=None, daq_sig_port_df=None):
    fig, axes = plt.subplots(sharex=True)
    axes.plot(portfolio['port_rtns'], '-', color='orange', label='switching_portfolio_returns')
    axes.plot(portfolio['KBSTAR 200TR'], '-r', label='KBSTAR200TR_returns')
    axes.plot(portfolio['TIGER 미국채10년선물'], '-b', label='TIGER미국채10년선물_returns')
    axes.axis(ymin=0, ymax=300)
    if sig_port_df is not None:
        plt.xticks(sig_port_df.index, rotation=45)
    elif daq_sig_port_df is not None:
        plt.xticks(daq_sig_port_df.index, rotation=45)
    myFmt = mdates.DateFormatter('%Y')
    axes.xaxis.set_major_formatter(myFmt)
    plt.title('Margin_Loan_Ratio_signal_switching_strategy_portfolio_returns')
    axes.legend()
    # plt.savefig(f'{n}.png')
    plt.show()


def performance_analysis(sig_port_df):
    sig_port_df['port_rtns'] = sig_port_df['port_rtns'].astype(float)
    # pf.create_returns_tear_sheet(sig_port_df['port_rtns'].pct_change())
    # qs.stats.cagr(sig_port_df['port_rtns'].pct_change())
    # qs.stats.compare(sig_port_df['port_rtns'].pct_change(), sig_port_df['KBSTAR 200TR'].pct_change())
    # qs.stats.max_drawdown(sig_port_df['port_rtns'])
    # qs.stats.sharpe(sig_port_df['port_rtns'].pct_change())
    # qs.stats.volatility(sig_port_df['port_rtns'].pct_change())
    qs.reports.full(sig_port_df['port_rtns'].pct_change())


if __name__ == '__main__':
    kospi = 'kospi_market'
    kosdaq = 'kosdaq_market'

    mkt_df = catch_signal(market=kospi)
    # mkt_df = catch_signal(market=kosdaq)
    products_df = load_data()

    sig_port_df = calc_returns(mkt_df, products_df)

    show_chart(sig_port_df)
    performance_analysis(sig_port_df)

k = 0
