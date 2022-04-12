import pandas as pd
import requests
import json
from pandas import json_normalize

proxies = {
    'http': 'socks5://127.0.0.1:9050',
    'https': 'socks5://127.0.0.1:9050'
}


def get_stock_daily_price(base_dt):
    url = 'http://data.krx.co.kr/comm/bldAttendant/getJsonData.cmd'
    data = {
        'bld': 'dbms/MDC/STAT/standard/MDCSTAT01501',
        'locale': 'ko_KR',
        'mktId': 'ALL',
        'trdDd': f'{base_dt}',
        'share': '1',
        'money': '1',
        'csvxls_isNo': 'false'
    }
    req = requests.post(url, data=data,
                        # proxies=proxies
                        )
    jsn = json.loads(req.text)
    stock_daily_df = json_normalize(jsn, 'OutBlock_1')
    columns = {
        'ISU_SRT_CD': 'ticker',
        'ISU_ABBRV': 'name_kr',
        'MKT_NM': 'mkt_nm',
        'SECT_TP_NM': 'department',
        'TDD_CLSPRC': 'std_pr',
        'TDD_OPNPRC': 'open_pr',
        'TDD_HGPRC': 'high_pr',
        'TDD_LWPRC': 'low_pr',
        'ACC_TRDVOL': 'trading_volume',
        'ACC_TRDVAL': 'trading_value',
        'MKTCAP': 'mkt_cap',
        'LIST_SHRS': 'listed_shares',
        'MKT_ID': 'mkt_cd'
    }
    stock_daily_df = stock_daily_df.rename(columns=columns)
    stock_daily_df['base_dt'] = base_dt
    stock_daily_df = stock_daily_df.set_index(
        pd.to_datetime(stock_daily_df['base_dt'].astype(str)).dt.strftime('%Y-%m-%d'))
    stock_daily_df = stock_daily_df.drop(columns=['base_dt', 'FLUC_TP_CD', 'CMPPREVDD_PRC', 'FLUC_RT'])
    stock_daily_df = stock_daily_df.astype(str).apply(lambda l: l.str.replace(',', '')).astype(int)

    return stock_daily_df


# stock_df = get_stock_daily_price(20220325)
