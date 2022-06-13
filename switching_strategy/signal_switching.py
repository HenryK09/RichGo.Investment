import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rc
import matplotlib.dates as mdates
import quantstats as qs

rc('font', family='AppleGothic')
plt.rcParams['axes.unicode_minus'] = False


def load_data():
    credit_df = pd.read_excel('/Users/user/dataknows/switching/credit_data.xlsx')
    products_df = pd.read_csv('/Users/user/dataknows/richgo_growth_products_0321.csv')
    kos_mktcap_df = pd.read_excel('/Users/user/dataknows/switching/kos_mkt_cap.xlsx')
    daq_mktcap_df = pd.read_excel('/Users/user/dataknows/switching/daq_mkt_cap.xlsx')

    return credit_df, products_df, kos_mktcap_df, daq_mktcap_df


def data_cleansing():
    credit_df, products_df, kos_mktcap_df, daq_mktcap_df = load_data()

    credit_df = credit_df.rename(columns={'Unnamed: 0': 'date'})
    credit_df = credit_df.sort_values('date', ascending=True).set_index('date')
    kos_credit_sr = credit_df['유가증권']
    daq_credit_sr = credit_df['코스닥']

    products_df = products_df.set_index('base_dt')
    products_df = products_df.loc['2011-01-03': '2022-03-18', :]
    products_df = products_df[['KBSTAR 200TR', 'TIGER 미국채10년선물']]
    products_df = products_df.pct_change() + 1
    products_df.iloc[0] = 100
    products_df = products_df.cumprod()

    kos_mktcap_df = kos_mktcap_df.sort_values('구 분', ascending=True).set_index('구 분')
    kos_mktcap_sr = kos_mktcap_df['시가총액']

    daq_mktcap_df = daq_mktcap_df.sort_values('구분', ascending=True).set_index('구분')
    daq_mktcap_sr = daq_mktcap_df['시가총액']

    kos_df = pd.DataFrame([kos_credit_sr, kos_mktcap_sr]).T
    daq_df = pd.DataFrame([daq_credit_sr, daq_mktcap_sr]).T

    kos_df['credit_rate'] = kos_df['유가증권'] / kos_df['시가총액']
    daq_df['credit_rate'] = daq_df['코스닥'] / daq_df['시가총액']

    return kos_df, daq_df, products_df


def calc_disparity():
    kos_df, daq_df, products_df = data_cleansing()

    kos_df = kos_df.ffill()
    daq_df = daq_df.ffill()

    kos_df['moving_avrg'] = kos_df['credit_rate'].rolling(20).mean()
    daq_df['moving_avrg'] = daq_df['credit_rate'].rolling(20).mean()

    kos_df['disparity'] = kos_df['credit_rate'] - kos_df['moving_avrg']
    daq_df['disparity'] = daq_df['credit_rate'] - daq_df['moving_avrg']

    return kos_df, daq_df, products_df


def catch_signal():
    kos_df, daq_df, products_df = calc_disparity()

    kos_df['short_signal'] = kos_df['disparity'] > 0.0004
    kos_df['short_signal'] = kos_df['short_signal'].replace(False, "").replace(True, 0)
    kos_df['long_signal'] = kos_df['disparity'] < -0.0004
    kos_df['long_signal'] = kos_df['long_signal'].replace(False, "").replace(True, 1)
    kos_df['signal'] = kos_df['short_signal'].astype(str) + kos_df['long_signal'].astype(str)
    kos_df['signal'] = kos_df['signal'].replace("", np.nan)
    kos_df['signal'].iloc[0] = 0.5
    kos_df['signal'] = kos_df['signal'].ffill()
    kos_df.index = pd.to_datetime(kos_df.index).strftime('%Y-%m-%d')

    daq_df['short_signal'] = daq_df['disparity'] > 0.002
    daq_df['short_signal'] = daq_df['short_signal'].replace(False, "").replace(True, 0)
    daq_df['long_signal'] = daq_df['disparity'] < -0.002
    daq_df['long_signal'] = daq_df['long_signal'].replace(False, "").replace(True, 1)
    daq_df['signal'] = daq_df['short_signal'].astype(str) + daq_df['long_signal'].astype(str)
    daq_df['signal'] = daq_df['signal'].replace("", np.nan)
    daq_df['signal'].iloc[0] = 0.5
    daq_df['signal'] = daq_df['signal'].ffill()
    daq_df.index = pd.to_datetime(daq_df.index).strftime('%Y-%m-%d')

    return kos_df, daq_df, products_df


def calc_returns():
    kos_df, daq_df, products_df = catch_signal()

    products_df['stock_returns'] = products_df['KBSTAR 200TR'].pct_change()
    products_df['bond_returns'] = products_df['TIGER 미국채10년선물'].pct_change()

    kos_sig_port_df = products_df.join(kos_df['signal'], how='outer')
    kos_sig_port_df.iloc[0] = kos_sig_port_df.iloc[0].fillna(0)
    kos_sig_port_df = kos_sig_port_df.dropna()
    kos_sig_port_df['signal'] = kos_sig_port_df['signal'].astype(float)

    kos_sig_port_df['port_rtns'] = ""

    for i in range(0, len(kos_sig_port_df['signal'])):
        if kos_sig_port_df['signal'].iloc[i] == 0.5:
            kos_sig_port_df['port_rtns'].iloc[i] = 0.5 * (
                    kos_sig_port_df['stock_returns'].iloc[i] + kos_sig_port_df['bond_returns'].iloc[i])
        elif kos_sig_port_df['signal'].iloc[i] == 0:
            kos_sig_port_df['port_rtns'].iloc[i] = kos_sig_port_df['bond_returns'].iloc[i]
        elif kos_sig_port_df['signal'].iloc[i] == 1:
            kos_sig_port_df['port_rtns'].iloc[i] = kos_sig_port_df['stock_returns'].iloc[i]

    kos_sig_port_df['port_rtns'] = kos_sig_port_df['port_rtns'] + 1
    kos_sig_port_df['port_rtns'].iloc[0] = 100
    kos_sig_port_df['port_rtns'] = kos_sig_port_df['port_rtns'].cumprod()

    kos_sig_port_df.index = pd.to_datetime(kos_sig_port_df.index)

    # 코스닥 시장
    daq_sig_port_df = products_df.join(daq_df['signal'], how='outer')
    daq_sig_port_df.iloc[0] = daq_sig_port_df.iloc[0].fillna(0)
    daq_sig_port_df = daq_sig_port_df.dropna()
    daq_sig_port_df['signal'] = daq_sig_port_df['signal'].astype(float)

    daq_sig_port_df['port_rtns'] = ""

    for i in range(0, len(daq_sig_port_df['signal'])):
        if daq_sig_port_df['signal'].iloc[i] == 0.5:
            daq_sig_port_df['port_rtns'].iloc[i] = 0.5 * (
                    daq_sig_port_df['stock_returns'].iloc[i] + daq_sig_port_df['bond_returns'].iloc[i])
        elif daq_sig_port_df['signal'].iloc[i] == 0:
            daq_sig_port_df['port_rtns'].iloc[i] = daq_sig_port_df['bond_returns'].iloc[i]
        elif daq_sig_port_df['signal'].iloc[i] == 1:
            daq_sig_port_df['port_rtns'].iloc[i] = daq_sig_port_df['stock_returns'].iloc[i]

    daq_sig_port_df['port_rtns'] = daq_sig_port_df['port_rtns'] + 1
    daq_sig_port_df['port_rtns'].iloc[0] = 100
    daq_sig_port_df['port_rtns'] = daq_sig_port_df['port_rtns'].cumprod()

    daq_sig_port_df.index = pd.to_datetime(daq_sig_port_df.index)

    return kos_sig_port_df, daq_sig_port_df


kos_sig_port_df, daq_sig_port_df = calc_returns()


def show_chart(portfolio):
    fig, axes = plt.subplots(sharex=True)
    axes.plot(portfolio['port_rtns'], '-', color='orange', label='switching_portfolio_returns')
    axes.plot(portfolio['KBSTAR 200TR'], '-r', label='KBSTAR200TR_returns')
    axes.plot(portfolio['TIGER 미국채10년선물'], '-b', label='TIGER미국채10년선물_returns')
    axes.axis(ymin=0, ymax=300)
    plt.xticks(kos_sig_port_df.index, rotation=45)
    myFmt = mdates.DateFormatter('%Y')
    axes.xaxis.set_major_formatter(myFmt)
    plt.title('Margin_Loan_Ratio_signal_switching_strategy_portfolio_returns')
    axes.legend()
    # plt.savefig(f'{n}.png')
    plt.show()


# show_chart(kos_sig_port_df)


def performance_analysis():
    kos_sig_port_df['port_rtns'] = kos_sig_port_df['port_rtns'].astype(float)
    # pf.create_returns_tear_sheet(kos_sig_port_df['port_rtns'].pct_change())
    # qs.stats.cagr(kos_sig_port_df['port_rtns'].pct_change())
    # qs.stats.compare(kos_sig_port_df['port_rtns'].pct_change(), kos_sig_port_df['KBSTAR 200TR'].pct_change())
    # qs.stats.max_drawdown(kos_sig_port_df['port_rtns'])
    # qs.stats.sharpe(kos_sig_port_df['port_rtns'].pct_change())
    # qs.stats.volatility(kos_sig_port_df['port_rtns'].pct_change())
    qs.reports.full(kos_sig_port_df['port_rtns'].pct_change())


performance_analysis()
