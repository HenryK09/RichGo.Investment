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

    headers = {'Accept': 'text/xml',
               'Accept-Encoding': 'gzip, deflate, br',
               'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
               'Connection': 'keep-alive',
               'Content-Type': 'text/xml',
               'Cookie': '__smVisitorID=V4ubac3GJYX; JSESSIONID=YLhK4UYsMKnT7V9aOZCS1AZNbae1BDsp0OaqaTGXnRA78syipb7m3Cu23BbV9zn4.ap1_servlet_kofiadisEngine; userGb=01; disTdMenu=%ED%8E%80%EB%93%9C%EA%B8%B0%EC%A4%80%EA%B0%80%EA%B2%A9%3D%3D%2Fwebsquare%2Findex.jsp%3Fw2xPath%3D%2Fwq%2Ffundann%2FDISFundStdPrice.xml%26divisionId%3DMDIS01004001000000%26serviceId%3DSDIS01004001000%7C%7C%EC%A3%BC%EC%9A%94%EC%A6%9D%EA%B0%90%ED%8E%80%EB%93%9C%3D%3D%2Fwebsquare%2Findex.jsp%3Fw2xPath%3D%2Fwq%2Ffundann%2FDISMainFlucFund.xml%26divisionId%3DMDIS01006002000000%26serviceId%3DSDIS01006002000%7C%7C%ED%8E%80%EB%93%9C%EB%B9%84%EA%B5%90%EA%B2%80%EC%83%89%3D%3D%2Fwebsquare%2Findex.jsp%3Fw2xPath%3D%2Fwq%2Fcmpann%2FDISFundCmpSrch.xml%26divisionId%3DMDIS01008000000000%26serviceId%3DSDIS01008000000%7C%7C%ED%8E%80%EB%93%9C%20%EC%88%98%EC%9D%B5%EB%B9%84%EC%9A%A9%20%EA%B3%84%EC%82%B0%EA%B8%B0%3D%3D%2Fwebsquare%2Findex.jsp%3Fw2xPath%3D%2Fwq%2Ffundcal%2FDISIdvFndSrch.xml%26divisionId%3DMDIS01014000000000%26serviceId%3DSDIS01014000000%7C%7C%ED%8E%80%EB%93%9C%ED%8C%90%EB%A7%A4%ED%9A%8C%EC%82%AC%20%ED%8E%80%EB%93%9C%20%EA%B8%B0%EC%A4%80%EA%B0%80%EA%B2%A9%EB%93%B1%EB%9D%BD%EB%A5%A0%3D%3D%2Fwebsquare%2Findex.jsp%3Fw2xPath%3D%2Fwq%2Ffundann%2FDISFundSaleStdPrcRate.xml%26divisionId%3DMDIS01013007000000%26serviceId%3DSDIS01013007000%7C%7C%EA%B8%B0%EC%A4%80%EA%B0%80%EA%B2%A9%EB%B3%80%EB%8F%99%EC%B6%94%EC%9D%B4%3D%3D%2Fwebsquare%2Findex.jsp%3Fw2xPath%3D%2Fwq%2Ffundann%2FDISFundStdPrcStut.xml%26divisionId%3DMDIS01004002000000%26serviceId%3DSDIS01004002000%7C%7C%EA%B8%B0%EC%A4%80%EA%B0%80%EA%B2%A9%EB%93%B1%EB%9D%BD%EB%A5%A0%3D%3D%2Fwebsquare%2Findex.jsp%3Fw2xPath%3D%2Fwq%2Ffundann%2FDISFundStdPrcRate.xml%26divisionId%3DMDIS01004003000000%26serviceId%3DSDIS01004003000%7C%7C%ED%8C%90%EB%A7%A4%EC%82%AC%EB%B3%84%20%ED%8E%80%EB%93%9C%EB%B3%B4%EC%88%98%EB%B9%84%EC%9A%A9%3D%3D%2Fwebsquare%2Findex.jsp%3Fw2xPath%3D%2Fwq%2Ffundann%2FDISSalesCompFeeCMS.xml%26divisionId%3DMDIS01005002000000%26serviceId%3DSDIS01005002000%7C%7C',
               'Host': 'dis.kofia.or.kr',
               'Origin': 'https://dis.kofia.or.kr',
               'Referer': 'https://dis.kofia.or.kr/websquare/index.jsp?w2xPath=/wq/fundann/DISFundStdPrice.xml&divisionId=MDIS01004001000000&serviceId=SDIS01004001000',
               'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36'
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
