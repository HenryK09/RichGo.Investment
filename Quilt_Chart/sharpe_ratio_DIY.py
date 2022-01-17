import pandas as pd
import numpy as np


def load_data():
    # price
    df = pd.read_csv('raw_data2.csv', index_col=0)
    df2 = pd.read_csv('richgo_historical_data.csv', encoding='cp949')

    df = df.stack().reset_index()
    df.columns = ['date','name','price']
    df2.columns = ['name', 'date', 'price']

    df = df.append(df2)
    df['date'] = pd.to_datetime(df['date'])

    df = df.pivot(index='date', columns='name', values='price').ffill().bfill()
    price_df = df['19991231':'20211231']

    # riskfree
    rf_sr = pd.read_csv('riskfree.csv', index_col=0, header=None)
    rf_sr = rf_sr[rf_sr.columns[0]]
    rf_sr.index = pd.to_datetime(rf_sr.index).strftime('%Y')
    rf_sr = rf_sr['2000':'2021']

    return price_df, rf_sr


def calc_yearly_return(price_df):
    df = price_df.resample('Y').last().pct_change().dropna(axis=0, how='all')
    df.index = df.index.strftime('%Y')
    return df


def calc_yearly_volatility(price_df):
    df = price_df.pct_change().resample('Y').std(ddof=0).dropna(axis=0, how='all') * np.sqrt(365)
    df.index = df.index.strftime('%Y')
    return df


def calc_sharpe_ratio(yr_df, yv_df, rf_sr):
    return yr_df.subtract(rf_sr.astype(float), axis=0) / yv_df


def main():
    price_df, rf_sr = load_data()
    yr_df = calc_yearly_return(price_df)
    yv_df = calc_yearly_volatility(price_df)
    sr_df = calc_sharpe_ratio(yr_df, yv_df, rf_sr)
    sr_df = sr_df.where(sr_df > 0, 1 / sr_df) # sharpe ratio < 0 이면 역수로 전환해서 순위 비교
    stop = 0
    sr_df.to_csv('C:/Users/user/Desktop/sharpe_ratio.csv', encoding='utf-8-sig')

if __name__ == '__main__':
    main()