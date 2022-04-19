import pandas as pd
import requests
from scraper.common.dbconn import DBConn
import os
import concurrent.futures as futures

FUND_DB = os.getenv('FUND_DB_URI')

proxies = {
    'http': 'socks5://127.0.0.1:9050',
    'https': 'socks5://127.0.0.1:9050'
}


def fetch_mng_fund():
    """
    DB에서 하위 클래스가 존재하는 운용펀드명 리스트를 가져온다.
    :return: 상위 운용펀드 이름 리스트
    """
    query = f"""
    select product_name 
    from fund_kofia.product_info 
    where private_public = '공모' and trait_division like '%FUND%'
    """
    mng_fund_df = DBConn(FUND_DB).fetch(query).df()
    mng_fund_list = mng_fund_df['product_name'].to_list()
    return mng_fund_list


def fetch_leftout_mng_fund():
    """
    ip 차단 문제로 중간에 끊긴 지점부터 다시 받기 위한 나머지 운용펀드명 리스트
    :return: DB에 적재되지 않은 나머지 상위 운용펀드 이름 리스트
    """
    query = f"""
    select product_name
    from fund_kofia.product_info 
    where private_public = '공모' and trait_division like '%FUND%'
    and product_name not in (select distinct family_ticker from fund_kofia.product_family)
    """
    mng_fund_df = DBConn(FUND_DB).fetch(query).df()
    mng_fund_list = mng_fund_df['product_name'].to_list()
    return mng_fund_list


def get_family_fund(name_kr, start_dt=None, end_dt=None):
    """
    상위 운용펀드의 코드로 하위 클래스 펀드들을 매핑한다.
    :param name_kr: 상위 운용펀드 명칭
    :param start_dt: 오늘 날짜로부터 6개월 전 날짜
    :param end_dt: 오늘 날짜
    :return: 공통의 펀드코드로 매핑된 데이터프레임
    """

    if end_dt is None:
        end_dt = pd.Timestamp.now(tz='Asia/Seoul')
    else:
        end_dt = pd.Timestamp(end_dt).strftime('%Y%m%d')
    if start_dt is None:
        start_dt = end_dt - pd.DateOffset(months=6)
    else:
        start_dt = pd.Timestamp(start_dt).strftime('%Y%m%d')

    end_dt = end_dt.strftime('%Y%m%d')
    start_dt = start_dt.strftime('%Y%m%d')

    url = 'https://dis.kofia.or.kr/proframeWeb/XMLSERVICES/'

    xml_str = f"""<?xml version="1.0" encoding="utf-8"?>
    <message>
      <proframeHeader>
        <pfmAppName>FS-DIS2</pfmAppName>
        <pfmSvcName>DISFundFTimeAnnSO</pfmSvcName>
        <pfmFnName>selectAnn</pfmFnName>
      </proframeHeader>
      <systemHeader></systemHeader>
        <DISFTimeAnnInsDTO>
        <uGb>1</uGb>
        <vStrtDt>{start_dt}</vStrtDt>
        <vEndDt>{end_dt}</vEndDt>
        <uCdList>{name_kr}</uCdList>
        <gbOption>N</gbOption>
        <uRptList>'2RF12'</uRptList>
        <tsCd>'2RF12'</tsCd>
        <uRptAllYN>0</uRptAllYN>
        <companyCd></companyCd>
    </DISFTimeAnnInsDTO>
    </message>""".encode('utf-8-sig')

    headers = {
        'Host': 'dis.kofia.or.kr',
        'Origin': 'https://dis.kofia.or.',
        'Referer': 'https://dis.kofia.or.kr/websquare/index.jsp?w2xPath=/wq/fundann/DISFundAnnSrch.xml&divisionId=MDIS01001000000000&serviceId=SDIS01001000000'
    }

    res = requests.post(url, data=xml_str, headers=headers,
                        proxies=proxies
                        ).text
    fund_family_df = pd.read_xml(res, xpath='.//list')

    fund_family_df = fund_family_df[['standardDt', 'uFundNm', 'standardCd']]
    fund_family_df = fund_family_df.rename(
        columns={
            'standardDt': 'base_dt',
            'uFundNm': 'product_name',
            'standardCd': 'ticker'
        }
    )
    try:
        fund_family_df = fund_family_df[['product_name', 'ticker']].drop_duplicates(keep='last')
    except:
        pass
    fund_family_df['family_ticker'] = fund_family_df['ticker'].iloc[0]
    fund_family_df['product_name'] = fund_family_df['product_name'].str.replace('└▶', '')
    family_fund_df = fund_family_df[['ticker', 'family_ticker', 'product_name']].copy()

    return family_fund_df


def update_one_family_fund(update_data_list):
    query = '''
                insert into fund_kofia.product_family (ticker, family_ticker)
                values (:ticker, :family_ticker)
                ON DUPLICATE KEY UPDATE
                    ticker = VALUES(ticker),
                    family_ticker = VALUES(family_ticker),
                    updated_at = now();
            '''
    DBConn(FUND_DB).update(query, update_data_list)


def family_fund_worker(name, i, mng_fund_list):
    family_fund_df = get_family_fund(name)
    update_data_list = family_fund_df.to_dict(orient='records')
    with DBConn(FUND_DB).transaction():
        update_one_family_fund(update_data_list)
    print(f'{len(mng_fund_list)}/{i} - {name}')


def run_multi_process(worker, mng_fund_list, *args):
    finished = []
    print(f'total: {len(mng_fund_list)}')
    try:
        futures_list = []
        with futures.ProcessPoolExecutor(max_workers=1) as executor:
            for i, name in enumerate(mng_fund_list):
                future = executor.submit(worker, name, i, mng_fund_list, *args)
                futures_list.append(future)
        result = futures.wait(futures_list)
        for future in result.done:
            finished.append(future.result())

    except Exception as e:
        print(f'{len(mng_fund_list)}/{i} - {name} - ERROR')
        raise e

    finally:
        print(f'len: {len(finished)}')


def update_family_fund():
    mng_fund_list = fetch_mng_fund()
    # mng_fund_list = fetch_leftout_mng_fund()
    run_multi_process(family_fund_worker, mng_fund_list)


if __name__ == '__main__':
    update_family_fund()
