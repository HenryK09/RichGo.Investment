import pandas as pd
import requests
import json
from pandas import json_normalize
from scraper_rough.stock_kr.api.stock_daily_by_date import get_stock_daily_price

proxies = {
    'http': 'socks5://127.0.0.1:9050',
    'https': 'socks5://127.0.0.1:9050'
}


def get_stock_code():
    url = 'http://data.krx.co.kr/comm/bldAttendant/getJsonData.cmd'
    data = {
        'locale': 'ko_KR',
        'mktsel': 'ALL',
        'typeNo': '0',
        'bld': 'dbms/comm/finder/finder_stkisu'
    }
    req = requests.post(url, data=data,
                        # proxies=proxies
                        )
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


def get_stock_price(start_dt, end_dt, ticker):
    if start_dt is None:
        start_dt = '19000101'
    else:
        start_dt = pd.Timestamp(start_dt).strftime('%Y%m%d')

    if end_dt is None:
        end_dt = pd.Timestamp.now(tz='Asia/Seoul').strftime('%Y%m%d')
    else:
        end_dt = pd.Timestamp(end_dt).strftime('%Y%m%d')

    if ticker is None:
        print('Return prices of all tickers today')
        return get_stock_daily_price(pd.Timestamp.now(tz='Asia/Seoul').strftime('%Y%m%d'))
    else:
        ticker = ticker

    url = 'http://data.krx.co.kr/comm/bldAttendant/getJsonData.cmd'

    code_df = get_stock_code()
    full_cd = code_df.loc[ticker, 'full_cd']
    data = {
        'bld': 'dbms/MDC/STAT/standard/MDCSTAT01701',
        'locale': 'ko_KR',
        'isuCd': f'{full_cd}',
        'strtDd': f'{start_dt}',
        'endDd': f'{end_dt}',
        'share': '1',
        'money': '1',
        'csvxls_isNo': 'false'
    }
    req = requests.post(url, data=data,
                        # proxies=proxies
                        )
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
    stock_daily_df = stock_daily_df.set_index(
        pd.to_datetime(stock_daily_df['base_dt'].astype(str)).dt.strftime('%Y-%m-%d'))
    stock_daily_df = stock_daily_df.drop(columns=['base_dt', 'FLUC_TP_CD', 'CMPPREVDD_PRC', 'FLUC_RT'])
    stock_daily_df = stock_daily_df.astype(str).apply(lambda l: l.str.replace(',', '')).astype(int)

    return stock_daily_df


# stock_df = get_stock_price(start_dt='20170317', end_dt='20220331', ticker='005930')