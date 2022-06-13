import pandas as pd
from scraper.fund_kr.api.fund_daily_by_date import get_fund_daily
import requests
from scraper.common.dbconn import DBConn
import os

FUND_DB = os.getenv('FUND_DB_URI')

proxies = {
    'http': 'socks5://127.0.0.1:9050',
    'https': 'socks5://127.0.0.1:9050'
}


def get_dividend_added_price(last_trading_dt=None, yesterday=None):
    url = 'https://dis.kofia.or.kr/proframeWeb/XMLSERVICES/'
    xml = f"""<?xml version="1.0" encoding="utf-8"?>
    <message>
      <proframeHeader>
        <pfmAppName>FS-DIS2</pfmAppName>
        <pfmSvcName>DISFundRdmpSO</pfmSvcName>
        <pfmFnName>select</pfmFnName>
      </proframeHeader>
      <systemHeader></systemHeader>
        <DISCondFuncDTO>
        <tmpV30>20220408</tmpV30>
        <tmpV31>20220410</tmpV31>
        <tmpV12></tmpV12>
        <tmpV3></tmpV3>
        <tmpV5></tmpV5>
        <tmpV4></tmpV4>
        <tmpV7></tmpV7>
    </DISCondFuncDTO>
    </message>
    """
    headers = {
        'Host': 'dis.kofia.or.kr',
        'Origin': 'https://dis.kofia.or.kr',
        'Referer': 'https://dis.kofia.or.kr/websquare/index.jsp?w2xPath=/wq/fundann/DISFundRdmp.xml&divisionId=MDIS01004004000000&serviceId=SDIS01004004000'
    }

    res = requests.post(url, data=xml, headers=headers,
                        proxies=proxies
                        ).text

    df = pd.read_xml(res, xpath='.//selectMeta')

    df = df[['tmpV1', 'tmpV2', 'tmpV3', 'tmpV4', 'tmpV5', 'tmpV6', 'tmpV7', 'tmpV8', 'tmpV9', 'tmpV10', 'tmpV11']]
    df = df.rename(columns={
        'tmpV1': 'company',
        'tmpV2': 'product_name',
        'tmpV3': 'accounting_start',
        'tmpV4': 'accounting_end',
        'tmpV5': 'elapsed_days',
        'tmpV6': 'aum',
        'tmpV7': 'std_pr',
        'tmpV8': 'tax_std_pr',
        'tmpV9': 'distribution_rate',
        'tmpV10': 'division',
        'tmpV11': 'ticker'
    })
    df['accounting_start'] = pd.to_datetime(df['accounting_start'].astype(str))
    df['accounting_end'] = pd.to_datetime(df['accounting_end'].astype(str))
    df['std_pr'] = df['std_pr'].astype(float)
    df['tax_std_pr'] = df['tax_std_pr'].astype(float)
    df['aum'] = df['aum'].astype(int)
    df['distribution_rate'] = df['distribution_rate'].astype(float)

    dvd_df = df[['ticker', 'std_pr', 'accounting_end']].set_index('ticker')

    return dvd_df


def get_daily_price_kofia(last_trading_dt=None, today=None):
    if last_trading_dt is None:
        # last_trading_dt =
        pass
    else:
        last_trading_dt = last_trading_dt
    if today is None:
        today = pd.Timestamp.now(tz='Asia/Seoul').strftime('%Y%m%d')
    else:
        today = today

    # for verification
    # kofia_pr_ytdy2 = get_fund_daily('20220407')
    # kofia_pr_ytdy2 = pd.read_csv('/Users/user/dataknows/20220407.csv', encoding='utf-8-sig')
    # kofia_pr_ytdy2 = kofia_pr_ytdy2[['ticker', 'base_dt', 'nav']]
    # kofia_pr_ytdy2['base_dt'] = pd.to_datetime(kofia_pr_ytdy2['base_dt'].astype(str))

    # ytdy_kofia_pr = get_fund_daily('20220408')
    # tdy_kofia_pr = get_fund_daily('20220411')

    last_kofia_pr = get_fund_daily(last_trading_dt)
    tdy_kofia_pr = get_fund_daily(today)

    # last_kofia_pr = pd.read_csv('/Users/user/dataknows/20220408.csv', encoding='utf-8-sig')
    # tdy_kofia_pr = pd.read_csv('/Users/user/dataknows/20220411.csv', encoding='utf-8-sig')

    last_kofia_pr = last_kofia_pr[['ticker', 'base_dt', 'nav']]
    tdy_kofia_pr = tdy_kofia_pr[['ticker', 'base_dt', 'nav']]

    last_kofia_pr['base_dt'] = pd.to_datetime(last_kofia_pr['base_dt'].astype(str))
    tdy_kofia_pr['base_dt'] = pd.to_datetime(tdy_kofia_pr['base_dt'].astype(str))

    return last_kofia_pr, tdy_kofia_pr


def replace_price(dvd_df):
    last_kofia_pr, tdy_kofia_pr = get_daily_price_kofia()
    tdy_kofia_pr = tdy_kofia_pr.set_index('ticker')
    dvd_df = dvd_df.loc[dvd_df.index.isin(tdy_kofia_pr.index)].copy()
    tdy_kofia_pr.loc[dvd_df.index, 'adj_nav'] = dvd_df['std_pr']
    tdy_kofia_pr['adj_nav'] = tdy_kofia_pr['adj_nav'].fillna(tdy_kofia_pr['nav'])
    kofia_price_chg = pd.merge(last_kofia_pr, tdy_kofia_pr, left_on='ticker', right_on='ticker')
    kofia_price_chg['price_chg'] = kofia_price_chg['adj_nav'] / kofia_price_chg['nav_x']

    return kofia_price_chg


def get_daily_price_db():
    query = '''
        select ticker, max(base_dt) as base_dt, adj_pr
        from fund_kofia.product_daily
        where base_dt = max(base_dt)
    '''
    return DBConn(FUND_DB).fetch(query).df()


def main():
    dvd_df = get_dividend_added_price()
    kofia_pr_chg = replace_price(dvd_df)
    db_pr = get_daily_price_db()

    kofia_pr_chg = kofia_pr_chg[['ticker', 'price_chg', 'base_dt_y']]
    db_pr = db_pr.loc[pd.to_datetime(db_pr['base_dt']) == '2022-04-08']
    # db_pr = db_pr.loc[pd.to_datetime(db_pr['base_dt'])]
    db_pr['base_dt'] = pd.to_datetime(db_pr['base_dt'].astype(str))
    db_pr['adj_pr'] = db_pr['adj_pr'].astype(float)

    df = pd.merge(kofia_pr_chg, db_pr, left_on='ticker', right_on='ticker')
    df['new_adj_pr'] = df['adj_pr'] * df['price_chg']
    df = df[['ticker', 'new_adj_pr', 'base_dt_y']]
    df = df.rename(columns={'base_dt_y': 'base_dt',
                            'new_adj_pr': 'adj_pr'
                            })

    return df


def update_daily_price():
    query = '''
        INSERT INTO fund_kofia.product_daily_practice (ticker, base_dt, adj_pr)
        VALUES (:ticker, :base_dt, :adj_pr)
        ON DUPLICATE KEY UPDATE ticker = VALUES(ticker),
                                base_dt = VALUES(base_dt),
                                adj_pr = VALUES(adj_pr),
                                updated_at = now();
    '''
    df = main()
    update_price_list = df.dict(orient='records')
    with DBConn(FUND_DB).transaction():
        DBConn(FUND_DB).update(query, update_price_list)

if __name__ == '__main__':
    update_daily_price()
    kd = 234
