import pandas as pd
import requests
from scraper.common.dbconn import DBConn
import os

FUND_DB = os.getenv('FUND_DB_URI')
CACHE_PATH = os.getenv('CACHE_PATH', '../..')


def get_family_fund(start_dt=None, end_dt=None):
    """
    상위 운용펀드의 코드로 하위 클래스 펀드들을 매핑한다.
    :param start_dt: 오늘 날짜로부터 6개월 전 날짜
    :param end_dt: 오늘 날짜
    :return: 공통의 펀드코드로 매핑된 데이터프레임
    """
    cache_file_path = f'{CACHE_PATH}/family_fund.csv'
    if os.path.isfile(cache_file_path):
        fund_family_df = pd.read_csv(cache_file_path, encoding='utf-8-sig')
    else:
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
            <uCdList></uCdList>
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

        res = requests.post(url, data=xml_str, headers=headers).text
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

    index_list = list(range(len(fund_family_df)))
    fund_family_df['is_child'] = fund_family_df['product_name'].str.contains('└▶')
    current_group_id = 0
    group_dict = {}
    for x, y in zip(index_list[:-1], index_list[1:]):
        x_sr = fund_family_df.iloc[x]
        y_sr = fund_family_df.iloc[y]

        if not x_sr['is_child'] and y_sr['is_child']:
            group_dict[current_group_id] = [x, y]
        elif x_sr['is_child'] and y_sr['is_child']:
            group_dict[current_group_id] += [y]
        elif x_sr['is_child'] and not y_sr['is_child']:
            current_group_id += 1

    family_fund = []
    for i in list(range(current_group_id)):
        one_family = fund_family_df.iloc[group_dict[i]]
        one_family['family_ticker'] = one_family.iloc[0]['ticker']
        # one_family['product_name'] = one_family['product_name'].str.replace('└▶', '')
        family_fund.append(one_family)
    family_fund_df = pd.concat(family_fund)

    family_fund_df = family_fund_df[['ticker', 'family_ticker']].copy()

    return family_fund_df


def update_family_fund():
    query = '''
        insert into fund_kofia.product_family (ticker, family_ticker)
        values (:ticker, :family_ticker)
        ON DUPLICATE KEY UPDATE ticker        = VALUES(ticker),
                                family_ticker = VALUES(family_ticker),
                                updated_at    = now();
        '''
    family_fund_df = get_family_fund()
    update_data_list = family_fund_df.to_dict(orient='records')
    with DBConn(FUND_DB).transaction():
        DBConn(FUND_DB).update(query, update_data_list)


if __name__ == '__main__':
    update_family_fund()