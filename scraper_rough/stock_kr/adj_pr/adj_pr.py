import pandas as pd
import numpy as np
from scraper_rough.stock_kr.api.stock_daily_by_ticker import get_stock_price
from scraper_rough.stock_kr.api.seibro_info_v1 import get_changed_shares_info
from scraper_rough.stock_kr.api.seibro_info_v1 import get_adj_dps_info
import os

PREFIX_pr = 'cached_pr'
PREFIX_sh = 'cached_sh'
PREFIX_dvd = 'cached_dvd'
CACHE_PATH = os.getenv('CACHE_PATH', '../..')


def get_stock_data(start_dt, end_dt, ticker, name_kr):
    cache_file_path_pr = f'{CACHE_PATH}/{PREFIX_pr}_{name_kr}.csv'
    cache_file_path_sh = f'{CACHE_PATH}/{PREFIX_sh}_{name_kr}.csv'
    cache_file_path_dvd = f'{CACHE_PATH}/{PREFIX_dvd}_{name_kr}.csv'

    if os.path.isfile(cache_file_path_pr and cache_file_path_sh and cache_file_path_dvd):
        std_pr_df = pd.read_csv(cache_file_path_pr, index_col=0)
        shares_df = pd.read_csv(cache_file_path_sh)
        dvd_df = pd.read_csv(cache_file_path_dvd)
    else:
        std_pr_df = get_stock_price(start_dt=start_dt, end_dt=end_dt, ticker=ticker)
        shares_df = get_changed_shares_info(from_dt=start_dt, to_dt=end_dt, name_kr=name_kr)
        dvd_df = get_adj_dps_info(from_dt=start_dt, to_dt=end_dt, name_kr=name_kr)

        std_pr_df.to_csv(cache_file_path_pr)
        shares_df.to_csv(cache_file_path_sh)
        dvd_df.to_csv(cache_file_path_dvd)

    df = std_pr_df.join(shares_df.reset_index().set_index('issue_dt')[['issue_reason', 'listing_dt']], how='outer')
    df = df.join(dvd_df.reset_index().set_index('base_dt')[
                     ['adj_DPS_cash', 'dividend_rate_stock', 'par_value']],
                 how='outer')
    df.index = pd.to_datetime(df.index)

    inc_df = df.copy()
    inc_df['listing_dt'] = pd.to_datetime(inc_df['listing_dt'])
    inc_df['adj_DPS'] = ''

    return inc_df


# 액면분할
def mng_stock_split():
    inc_df = get_stock_data(start_dt, end_dt, ticker, name_kr)
    split_dt = inc_df.query('issue_reason == "액면분할"').index[0]
    split_ratio = (inc_df.shift(-1).loc[inc_df.index == split_dt]['listed_shares'].item()) / (
        inc_df.loc[inc_df.index == split_dt]['listed_shares'].item())

    inc_df.loc[inc_df.index <= split_dt, 'adj_DPS'] = (
            inc_df['adj_DPS_cash'] * inc_df['par_value'] * split_ratio / 100).shift(-2)
    inc_df.loc[inc_df.index <= split_dt, 'split_adj_pr'] = inc_df['std_pr'] / split_ratio
    inc_df.loc[inc_df.index > split_dt, 'adj_DPS'] = (inc_df['adj_DPS_cash'] * inc_df['par_value'] / 100).shift(-2)
    inc_df.loc[inc_df.index > split_dt, 'split_adj_pr'] = inc_df['std_pr']

    return inc_df


# 액면병합
def mng_reverse_stock_split():
    inc_df = get_stock_data(start_dt, end_dt, ticker, name_kr)
    rev_split_dt = inc_df.query('issue_reason == "액면병합"')['listing_dt'].item()
    rev_split_ratio = (inc_df.loc[inc_df.index == rev_split_dt]['listed_shares'].item()) / (
        inc_df.shift(1).loc[inc_df.index == rev_split_dt]['listed_shares'].item())
    inc_df['adj_DPS'] = np.nan
    inc_df.loc[inc_df.index >= rev_split_dt, 'adj_DPS'] = (
                inc_df.loc[inc_df.index >= rev_split_dt, 'adj_DPS_cash'] * inc_df.loc[
            inc_df.index >= rev_split_dt, 'par_value'] * rev_split_ratio / 100).shift(-2)
    inc_df['rev_split_adj_pr'] = ''
    inc_df.loc[inc_df.index >= rev_split_dt, 'rev_split_adj_pr'] = inc_df.loc[
                                                                       inc_df.index >= rev_split_dt, 'std_pr'] * rev_split_ratio
    inc_df.loc[inc_df.index < rev_split_dt, 'adj_DPS'] = (
                inc_df.loc[inc_df.index < rev_split_dt, 'adj_DPS_cash'] * inc_df.loc[
            inc_df.index < rev_split_dt, 'par_value'] / 100).shift(-2)
    inc_df.loc[inc_df.index < rev_split_dt, 'rev_split_adj_pr'] = inc_df.loc[inc_df.index < rev_split_dt, 'std_pr']

    return inc_df


# 주당배당금
def mng_dps():
    inc_df = get_stock_data(start_dt, end_dt, ticker, name_kr)
    # 액면분할이 있는 주식일 경우
    if len(inc_df.loc[inc_df['issue_reason'] == '액면분할']) != 0:
        inc_df = mng_stock_split()
        # 현금배당 cumsum
        try:
            inc_df['adj_DPS_cash_cumsum'] = inc_df['adj_DPS'].cumsum()
        except:
            inc_df['adj_DPS_cash_cumsum'] = np.nan
    # 액면병합이 있는 주식일 경우
    elif len(inc_df.loc[inc_df['issue_reason'] == '액면병합']) != 0:
        inc_df = mng_reverse_stock_split()
        # 현금배당 cumsum
        try:
            inc_df['adj_DPS_cash_cumsum'] = inc_df['adj_DPS'].cumsum()
        except:
            inc_df['adj_DPS_cash_cumsum'] = np.nan
    # 액면분할이나 액면병합이 없는 주식일 경우
    else:
        inc_df['adj_DPS'] = (inc_df['adj_DPS_cash'] * inc_df['par_value'] / 100).shift(-2)
        # 현금배당 cumsum
        try:
            inc_df['adj_DPS_cash_cumsum'] = inc_df['adj_DPS'].cumsum()
        except:
            inc_df['adj_DPS_cash_cumsum'] = np.nan

    return inc_df


# 무상증자
def mng_bonus_issue():
    inc_df = mng_dps()
    if len(inc_df.loc[inc_df['issue_reason'] == '무상증자']) != 0:
        bonus_base_dt = inc_df.shift(-1).query('issue_reason == "무상증자"').index[0]
        bonus_issue_dt = inc_df.shift(-1).query('issue_reason == "무상증자"')['listing_dt'].item()
        bonus_issue_rate = (inc_df.loc[inc_df.index == bonus_issue_dt]['listed_shares'].values /
                            inc_df.shift(1).loc[inc_df.index == bonus_issue_dt][
                                'listed_shares'].values).item()
        inc_df['inc_rate'] = np.nan
        inc_df['inc_rate'][bonus_base_dt] = bonus_issue_rate
        inc_df['inc_rate'] = inc_df['inc_rate'].ffill().fillna(1)

        ffill_df = inc_df.drop(
            columns=['issue_reason', 'adj_DPS_cash', 'dividend_rate_stock', 'par_value', 'adj_DPS', 'listing_dt'])
        ffill_df = ffill_df.ffill().fillna(0).astype(float)
        ffill_df['inc_pr'] = ''
        ffill_df['inc_pr'] = ffill_df['std_pr'] * ffill_df['inc_rate']
        ffill_df['adj_pr'] = ffill_df['inc_pr']
        ffill_df['adj_pr_cash'] = ''
        ffill_df['adj_pr_cash'] = ffill_df['inc_pr'] + ffill_df['adj_DPS_cash_cumsum']
    else:
        ffill_df = inc_df.drop(
            columns=['issue_reason', 'adj_DPS_cash', 'dividend_rate_stock', 'par_value', 'adj_DPS', 'listing_dt'])
        ffill_df = ffill_df.ffill().fillna(0).astype(float)
        if len(inc_df.loc[inc_df['issue_reason'] == '액면분할']) != 0:
            ffill_df['adj_pr_cash'] = ffill_df['split_adj_pr'] + ffill_df['adj_DPS_cash_cumsum']
        elif len(inc_df.loc[inc_df['issue_reason'] == '액면병합']) != 0:
            ffill_df['adj_pr_cash'] = ffill_df['rev_split_adj_pr'] + ffill_df['adj_DPS_cash_cumsum']
        else:
            ffill_df['adj_pr_cash'] = ffill_df['std_pr'] + ffill_df['adj_DPS_cash_cumsum']

    return ffill_df


def main(start_dt, end_dt, ticker, name_kr):
    # 무상증자 처리
    bon_df = mng_bonus_issue()

    return bon_df


if __name__ == '__main__':
    start_dt = '20210401'
    end_dt = '20220411'
    ticker = '006980'
    name_kr = '우성'

    # start_dt = '20210401'
    # end_dt = '20220408'
    # ticker = '025560'
    # name_kr = '미래산업'

    # start_dt = '20180401'
    # end_dt = '20220408'
    # ticker = '005930'
    # name_kr = '삼성전자'

    # start_dt = '20180105'
    # end_dt = '20220404'
    # ticker = '285130'
    # name_kr = 'SK케미칼'

    # start_dt = '20130717'
    # end_dt = '20220401'
    # ticker = '089600'
    # name_kr = '나스미디어'

    adj_pr_df = main(start_dt, end_dt, ticker, name_kr)
    adj_pr_df.to_csv('/Users/user/dataknows/woosung.csv')