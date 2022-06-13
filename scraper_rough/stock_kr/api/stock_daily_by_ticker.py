import pandas as pd
import requests
import json
from pandas import json_normalize
from scraper_rough.stock_kr.api.stock_daily_by_date import get_stock_daily_price


def get_stock_code():
    url = 'http://data.krx.co.kr/comm/bldAttendant/getJsonData.cmd'
    data = {
        'locale': 'ko_KR',
        'mktsel': 'ALL',
        'typeNo': '0',
        'bld': 'dbms/comm/finder/finder_stkisu'
    }
    req = requests.post(url, data=data)
    jsn = json.loads(req.text)
    code_df = pd.json_normalize(jsn, 'block1')
    columns = {
        'full_code': 'full_cd',
        'short_code': 'short_cd',
        'codeName': 'item_nm',
        'marketCode': 'mkt_cd',
        'marketEngName': 'mkt_nm',
    }
    code_df = code_df.rename(columns=columns)
    code_df = code_df.drop(columns=['marketName', 'ord1', 'ord2'])
    code_df = code_df.set_index('short_cd')
    return code_df


def get_stock_price(ticker, start_dt=None, end_dt=None):
    if start_dt is None:
        start_dt = '19950502'
    else:
        start_dt = pd.Timestamp(start_dt).strftime('%Y%m%d')

    if end_dt is None:
        end_dt = pd.Timestamp.now(tz='Asia/Seoul').strftime('%Y%m%d')
    else:
        end_dt = pd.Timestamp(end_dt).strftime('%Y%m%d')

    if ticker is None:
        print('Return prices of all tickers today')
        return get_stock_daily_price(pd.Timestamp.now(tz='Asia/Seoul').strftime('%Y%m%d'))

    url = 'http://data.krx.co.kr/comm/bldAttendant/getJsonData.cmd'

    code_df = get_stock_code()
    full_cd = code_df.loc[ticker, 'full_cd']
    data = {
        'bld': 'dbms/MDC/STAT/standard/MDCSTAT01701',
        'locale': 'ko_KR',
        'isuCd': full_cd,
        'strtDd': start_dt,
        'endDd': end_dt,
        'share': '1',
        'money': '1',
        'csvxls_isNo': 'false'
    }
    req = requests.post(url, data=data)
    jsn = json.loads(req.text)
    stock_daily_df = json_normalize(jsn, 'output')
    columns = {
        'TRD_DD': 'base_dt',
        'TDD_CLSPRC': 'std_pr',
        'TDD_OPNPRC': 'open_pr',
        'TDD_HGPRC': 'high_pr',
        'TDD_LWPRC': 'low_pr',
        'ACC_TRDVOL': 'trading_volume',
        'ACC_TRDVAL': 'trading_value',
        'MKTCAP': 'mkt_cap',
        'LIST_SHRS': 'listed_shares'
    }
    stock_daily_df = stock_daily_df.rename(columns=columns)
    stock_daily_df['base_dt'] = pd.to_datetime(stock_daily_df['base_dt'])
    stock_daily_df['ticker'] = ticker
    stock_daily_df['ticker'] = stock_daily_df['ticker'].astype(str)
    stock_daily_df = stock_daily_df.set_index(['ticker', 'base_dt'])
    stock_daily_df = stock_daily_df.drop(columns=['FLUC_TP_CD', 'CMPPREVDD_PRC', 'FLUC_RT'])
    stock_daily_df = stock_daily_df.replace(r',', '', regex=True).astype(int)

    return stock_daily_df
