import pandas as pd
import requests
import os

PREFIX = 'cached_fund_daily'
CACHE_PATH = os.getenv('CACHE_PATH', '../..')

# proxies = {
#     'http': 'socks5://127.0.0.1:9050',
#     'https': 'socks5://127.0.0.1:9050'
# }


def get_fund_daily(base_dt):
    """
    펀드 일단위 데이터 수집
    --------------------
    :param:
        base_dt : 기준일
    :return: Dataframe
        펀드 일 데이터
    """
    base_dt = pd.Timestamp(base_dt).strftime('%Y%m%d')
    cache_file_path = f'{CACHE_PATH}/{PREFIX}_{base_dt}.csv'
    if os.path.isfile(cache_file_path):
        return pd.read_csv(cache_file_path)

    url = 'https://dis.kofia.or.kr/proframeWeb/XMLSERVICES/'

    xml_str = f"""<?xml version="1.0" encoding="utf-8"?>
    <message>
      <proframeHeader>
        <pfmAppName>FS-DIS2</pfmAppName>
        <pfmSvcName>DISFundStdPriceSO</pfmSvcName>
        <pfmFnName>select</pfmFnName>
      </proframeHeader>
      <systemHeader></systemHeader>
        <DISCondFuncDTO>
        <tmpV30>{base_dt}</tmpV30>
        <tmpV3></tmpV3>
        <tmpV4></tmpV4>
        <tmpV7></tmpV7>
        <tmpV5></tmpV5>
        <tmpV11></tmpV11>
        <tmpV12></tmpV12>
        <tmpV50></tmpV50>
        <tmpV51></tmpV51>
    </DISCondFuncDTO>
    </message>"""

    headers = {'Host': 'dis.kofia.or.kr',
               'Origin': 'https://dis.kofia.or.kr',
               'Referer': 'https://dis.kofia.or.kr/websquare/index.jsp?w2xPath=/wq/fundann/DISFundStdPrice.xml&divisionId=MDIS01004001000000&serviceId=SDIS01004001000',
               }

    res = requests.post(url, data=xml_str, headers=headers,
                        # proxies=proxies
                        ).text
    fund_daily_df = pd.read_xml(res, xpath='.//selectMeta')

    fund_daily_df = data_cleansing(fund_daily_df)

    fund_daily_df.to_csv(cache_file_path, encoding='utf-8-sig')

    return fund_daily_df


def data_cleansing(fund_daily_df):
    """
    fund daily data cleansing
    ---------------------------------------
    :param:
        fund_daily_df : 수집한 fund daily 정보
    :return: DataFrame
        정제된 fund daily 정보
    """
    fund_daily_df = fund_daily_df.loc[:, 'tmpV2':'tmpV14'].copy()

    result_df = fund_daily_df.rename(
        columns={'tmpV14': 'base_dt',
                 'tmpV13': 'sale_comp_code',
                 'tmpV12': 'ticker',
                 'tmpV2': 'name_kr',
                 'tmpV4': 'listing_dt',
                 'tmpV5': 'aum',
                 'tmpV6': 'nav',
                 'tmpV7': 'tax_base_nav'}
    )[['base_dt', 'sale_comp_code', 'ticker', 'name_kr', 'listing_dt',
       'aum', 'nav', 'tax_base_nav']]

    return result_df
