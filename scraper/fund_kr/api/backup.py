import pandas as pd
import requests
import os
from scraper.fund_kr.api.fund_daily_by_date import get_fund_daily
import multitasking

PREFIX = 'cached_fund_daily'
CACHE_PATH = os.getenv('CACHE_PATH', '../..')


def get_fund_name_sr(base_dt):
    """
    기준일 당일 전체 펀드코드별 펀드명 데이터 가져오기
    --------------------------------------
    :param base_dt: 기준일
    :return: Series
        펀드코드를 인덱스로 하는 펀드명 시리즈
    """
    base_dt = pd.Timestamp(base_dt).strftime('%Y%m%d')
    cache_file_path = f'{CACHE_PATH}/{PREFIX}_{base_dt}.csv'
    if os.path.isfile(cache_file_path):
        daily_fund = pd.read_csv(cache_file_path, index_col=0)
        # 겹치는 ticker 가 없는지 확인
        has_not_duplicates = all(~daily_fund.set_index('ticker').index.duplicated(False))
        assert has_not_duplicates
        daily_fund = daily_fund.set_index('ticker')['name_kr']
        return daily_fund
    else:
        daily_fund = get_fund_daily(base_dt)
        has_not_duplicates = all(~daily_fund.set_index('ticker').index.duplicated(False))
        assert has_not_duplicates
        daily_fund = daily_fund.set_index('ticker')['name_kr']
        return daily_fund


def unreset_price(ticker):
    """
    분배가 발생한 회계기말 날짜 다음 거래일 기준가격 가져오기
    (1000으로 리셋되지 않은 기준가격 = 수정기준가격)
    --------------------------------------------
    :param:
        ticker: 펀드코드
    :return: DataFrame
        분배일 수정기준가
    """
    url = 'https://dis.kofia.or.kr/proframeWeb/XMLSERVICES/'

    xml = f"""<?xml version="1.0" encoding="utf-8"?>
    <message>
      <proframeHeader>
        <pfmAppName>FS-COM</pfmAppName>
        <pfmSvcName>COMFundSettleExSO</pfmSvcName>
        <pfmFnName>settleExSrch</pfmFnName>
      </proframeHeader>
      <systemHeader></systemHeader>
        <COMFundUnityInfoInputDTO>
        <standardCd>{ticker}</standardCd>
        <companyCd></companyCd>
    </COMFundUnityInfoInputDTO>
    </message>"""

    headers = {'Accept': 'text/xml',
               'Accept-Encoding': 'gzip, deflate, br',
               'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
               'Connection': 'keep-alive',
               'Content-Type': 'text/xml',
               'Cookie': '__smVisitorID=Qhfls34NRgD; userGb=01; JSESSIONID=HvdYnSqYwl8b9XB5jhWHVaCmPFVJJnaO8jmJFF8Lj0GvkOJQ7dTJqprnx8GzaGtu.ap2_servlet_engine3; disTdMenu=%EA%B2%B0%EC%82%B0%20%EB%B0%8F%20%EC%83%81%ED%99%98%3D%3D%2Fwebsquare%2Findex.jsp%3Fw2xPath%3D%2Fwq%2Ffundann%2FDISFundRdmp.xml%26divisionId%3DMDIS01004004000000%26serviceId%3DSDIS01004004000%7C%7C%ED%8E%80%EB%93%9C%EC%88%98%EC%9D%B5%EB%A5%A0%20%EB%B9%84%EA%B5%90%EA%B3%B5%EC%8B%9C%3D%3D%2Fwebsquare%2Findex.jsp%3Fw2xPath%3D%2Fwq%2Ffundann%2FDISFundROPCmpAnn.xml%26divisionId%3DMDIS01009001000000%26serviceId%3DSDIS01009001000%23!%7C%7C%ED%8E%80%EB%93%9C%ED%91%9C%EC%A4%80%EC%BD%94%EB%93%9C%EC%A1%B0%ED%9A%8C%3D%3D%2Fwebsquare%2Findex.jsp%3Fw2xPath%3D%2Fwq%2Fetcann%2FDISFundStandardCD.xml%26divisionId%3DMDIS04003000000000%26serviceId%3DSDIS04003000000%7C%7C%ED%8F%89%EA%B0%80%EA%B8%B0%EC%A4%80%EA%B3%B5%EC%8B%9C%3D%3D%2Fwebsquare%2Findex.jsp%3Fw2xPath%3D%2Fwq%2Fetcann%2FDISEstStdAnn.xml%26divisionId%3DMDIS04002000000000%26serviceId%3DSDIS04002000000%7C%7C%ED%8E%80%EB%93%9C%EB%B3%84%20%EC%BD%94%EB%93%9C%EC%A1%B0%ED%9A%8C%3D%3D%2Fwebsquare%2Findex.jsp%3Fw2xPath%3D%2Fwq%2Fetcann%2FDISFrnFundCdInq.xml%26divisionId%3DMDIS04001001000000%26serviceId%3DSDIS04001001000%7C%7C%EC%9E%90%EB%B3%B8%EC%8B%9C%EC%9E%A5%EB%B2%95%EC%A0%81%EC%9A%A9%ED%8E%80%EB%93%9C%3D%3D%2Fwebsquare%2Findex.jsp%3Fw2xPath%3D%2Fwq%2Ffundann%2FDISNewLawFund.xml%26divisionId%3DMDIS01006003000000%26serviceId%3DSDIS01006003000%7C%7C%EC%A3%BC%EC%8B%9D%ED%98%95%3D%3D%2Fwebsquare%2Findex.jsp%3Fw2xPath%3D%2Fwq%2Fdamoa%2FDISFundAnnFundUnit.xml%26divisionId%3DMDIS08002000000000%26serviceId%3DSDIS08002000000%7C%7CMMF%3D%3D%2Fwebsquare%2Findex.jsp%3Fw2xPath%3D%2Fwq%2Fdamoa%2FDISFundAnnFundUnit.xml%26divisionId%3DMDIS08005000000000%26serviceId%3DSDIS08005000000%7C%7C%ED%8E%80%EB%93%9C%EB%B3%84%20%EB%B3%B4%EC%88%98%EB%B9%84%EC%9A%A9%EB%B9%84%EA%B5%90%3D%3D%2Fwebsquare%2Findex.jsp%3Fw2xPath%3D%2Fwq%2Ffundann%2FDISFundFeeCMS.xml%26divisionId%3DMDIS01005001000000%26serviceId%3DSDIS01005001000%7C%7C%ED%8E%80%EB%93%9C%EA%B8%B0%EC%A4%80%EA%B0%80%EA%B2%A9%3D%3D%2Fwebsquare%2Findex.jsp%3Fw2xPath%3D%2Fwq%2Ffundann%2FDISFundStdPrice.xml%26divisionId%3DMDIS01004001000000%26serviceId%3DSDIS01004001000; JSESSIONID=oFWkL8CgaiDviiad3urt7Ap7NIXrhgM7i1Bt71FNsnva9rq07HHtBPwam9nk9kUF.ap1_servlet_kofiadisEngine',
               'Host': 'dis.kofia.or.kr',
               'Origin': 'https://dis.kofia.or.kr',
               'Referer': 'https://dis.kofia.or.kr/websquare/popup.html?w2xPath=/wq/com/popup/DISComFundSmryInfo.xml&companyCd=&standardCd=K55370BU1789&standardDt=&grntGb=S&search=&check=1&isMain=undefined&companyGb=A&uFundNm=/v8AQQBCu/itba34uFzCpMmdrYzSLMeQwuDQwQAoyPzC3QAtx6ysBMgR1hUAKciFuVjWFQBDAGUA%0ALQBQADI%3D&popupID=undefined&w2xHome=/wq/fundann/&w2xDocumentRoot=',
               'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.80 Safari/537.36'
               }

    res = requests.post(url, data=xml, headers=headers).text

    unreset_price_df = pd.read_xml(res, xpath='.//settleExList')

    unreset_price_df['code'] = ticker

    unreset_price_df = unreset_price_df[['code', 'trustAccend', 'standardCot']].copy()
    unreset_price_df = unreset_price_df.rename(columns={'trustAccend': 'trust_end_dt'})
    unreset_price_df['trust_end_dt'] = pd.to_datetime(unreset_price_df['trust_end_dt'], format='%Y%m%d')
    unreset_price_df = unreset_price_df.sort_values(['code', 'trust_end_dt'], ascending=True)

    return unreset_price_df


def sales_comp_list():
    """
    펀드 판매회사별 펀드코드와 펀드명 데이터 가져오기
    --------------------------------------
    :return: DataFrame
        펀드코드, 펀드명
    """
    url = 'https://dis.kofia.or.kr/proframeWeb/XMLSERVICES/'

    xml_str = """<?xml version="1.0" encoding="utf-8"?>
    <message>
      <proframeHeader>
        <pfmAppName>FS-DIS2</pfmAppName>
        <pfmSvcName>DISMngCompInqSO</pfmSvcName>
        <pfmFnName>select</pfmFnName>
      </proframeHeader>
      <systemHeader></systemHeader>
        <DISMngCompInqListDTO>
        <option>S2</option>
        <standardDt></standardDt>
    </DISMngCompInqListDTO>
    </message>"""

    headers = {
        'Accept': 'text/xml',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
        'Connection': 'keep-alive',
        'Content-Type': 'text/xml',
        'Cookie': '__smVisitorID=V4ubac3GJYX; JSESSIONID=7d75tg4uC8fd8nxPPiGamBhJedrGP6Lr9Q8OPn1GiWpTOKZap81tnXoUcoGnKFZy.ap2_servlet_kofiadisEngine; userGb=01; disTdMenu=%ED%8C%90%EB%A7%A4%EC%82%AC%EB%B3%84%20%ED%8E%80%EB%93%9C%EB%B3%B4%EC%88%98%EB%B9%84%EC%9A%A9%3D%3D%2Fwebsquare%2Findex.jsp%3Fw2xPath%3D%2Fwq%2Ffundann%2FDISSalesCompFeeCMS.xml%26divisionId%3DMDIS01005002000000%26serviceId%3DSDIS01005002000%7C%7C',
        'Host': 'dis.kofia.or.kr',
        'Origin': 'https://dis.kofia.or.kr',
        'Referer': 'https://dis.kofia.or.kr/websquare/index.jsp?w2xPath=/wq/fundann/DISSalesCompFeeCMS.xml&divisionId=MDIS01005002000000&serviceId=SDIS01005002000',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36'
    }

    res = requests.post(url, data=xml_str, headers=headers).text

    sale_comp_df = pd.read_xml(res, xpath='.//list')

    sale_comp_df = sale_comp_df[['saleCompCd', 'koreanNm']]
    sale_comp_df = sale_comp_df.sort_values(by='saleCompCd', ascending=True)
    sale_comp_df = sale_comp_df.rename(columns={'saleComCd': '판매회사_코드', 'koreanNM': '판매회사'})

    sale_comp_list = sale_comp_df['saleCompCd'].tolist()

    return sale_comp_list


