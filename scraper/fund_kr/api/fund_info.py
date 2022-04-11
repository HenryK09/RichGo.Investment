import pandas as pd
import requests
from scraper.fund_kr.api.backup import (get_fund_name_sr)
from datetime import datetime
from scraper.fund_kr.api.fund_daily_by_date import (get_fund_daily)


# proxies = {
#     'http': 'socks5://127.0.0.1:9050',
#     'https': 'socks5://127.0.0.1:9050'
# }

def get_fund_info(base_dt, ticker):
    """
    펀드기본정보 스크래핑
    -----------------
    :param
        base_dt: 기준일
        ticker: 펀드코드
    :return: DataFrame
        펀드기본정보
    """
    url = 'https://dis.kofia.or.kr/proframeWeb/XMLSERVICES/'

    xml_str = f"""<?xml version="1.0" encoding="utf-8"?>
    <message>
      <proframeHeader>
        <pfmAppName>FS-COM</pfmAppName>
        <pfmSvcName>COMFundUnityBasInfoSO</pfmSvcName>
        <pfmFnName>fundBasInfoSrch</pfmFnName>
      </proframeHeader>
      <systemHeader></systemHeader>
        <COMFundUnityInfoInputDTO>
        <standardCd>{ticker}</standardCd>
        <standardDt>{base_dt}</standardDt>
    </COMFundUnityInfoInputDTO>
    </message>"""

    headers = {
        'Cookie': '__smVisitorID=V4ubac3GJYX; JSESSIONID=vo6s7LxPdf51od0G4nkg8um7V9MtfQGjzqR8a23XvADB1u1mpSrzQNHqnP4xVXFf.ap2_servlet_kofiadisEngine; userGb=01; disTdMenu=%EC%97%B0%EA%B8%88%EC%83%81%ED%92%88%EA%B3%B5%EC%8B%9C%3D%3D%2Fwebsquare%2Findex.jsp%3Fw2xPath%3D%2Fwq%2Fcmpann%2FDISPension.xml%26divisionId%3DMDIS01010001000000%26serviceId%3DSDIS01010001000%7C%7C%ED%8E%80%EB%93%9C%EB%B9%84%EA%B5%90%EA%B2%80%EC%83%89%3D%3D%2Fwebsquare%2Findex.jsp%3Fw2xPath%3D%2Fwq%2Fcmpann%2FDISFundCmpSrch.xml%26divisionId%3DMDIS01008000000000%26serviceId%3DSDIS01008000000%7C%7C%ED%8E%80%EB%93%9C%EA%B8%B0%EC%A4%80%EA%B0%80%EA%B2%A9%3D%3D%2Fwebsquare%2Findex.jsp%3Fw2xPath%3D%2Fwq%2Ffundann%2FDISFundStdPrice.xml%26divisionId%3DMDIS01004001000000%26serviceId%3DSDIS01004001000%7C%7C%EA%B2%B0%EC%82%B0%20%EB%B0%8F%20%EC%83%81%ED%99%98%3D%3D%2Fwebsquare%2Findex.jsp%3Fw2xPath%3D%2Fwq%2Ffundann%2FDISFundRdmp.xml%26divisionId%3DMDIS01004004000000%26serviceId%3DSDIS01004004000%7C%7C%EC%97%B0%EA%B8%88%EC%83%81%ED%92%88%EC%83%81%EC%84%B8%EC%88%98%EC%9D%B5%EB%A5%A0%3D%3D%2Fwebsquare%2Findex.jsp%3Fw2xPath%3D%2Fwq%2Fcmpann%2FDISPensionProfit.xml%26divisionId%3DMDIS01010003000000%26serviceId%3DSDIS01010003000%7C%7C%EC%98%A8%EB%9D%BC%EC%9D%B8%EC%A0%84%EC%9A%A9%ED%8E%80%EB%93%9C%3D%3D%2Fwebsquare%2Findex.jsp%3Fw2xPath%3D%2Fwq%2Ffundann%2FDISOnlineFund.xml%26divisionId%3DMDIS01007001000000%26serviceId%3DSDIS01007001000%7C%7C%EC%9E%A5%EA%B8%B0%EB%B9%84%EA%B3%BC%EC%84%B8%ED%8E%80%EB%93%9C%3D%3D%2Fwebsquare%2Findex.jsp%3Fw2xPath%3D%2Fwq%2Ffundann%2FDISTaxFreeFund.xml%26divisionId%3DMDIS01007002000000%26serviceId%3DSDIS01007002000%7C%7C%ED%8A%B9%EC%A0%95%EC%9C%A0%ED%98%95%EC%84%A0%ED%83%9D%20%EC%A1%B0%ED%9A%8C%3D%3D%2Fwebsquare%2Findex.jsp%3Fw2xPath%3D%2Fwq%2Ffundann%2FDISFundByType.xml%26divisionId%3DMDIS01007003000000%26serviceId%3DSDIS01007003000%7C%7C%EC%A3%BC%EC%9A%94%EC%A6%9D%EA%B0%90%ED%8E%80%EB%93%9C%3D%3D%2Fwebsquare%2Findex.jsp%3Fw2xPath%3D%2Fwq%2Ffundann%2FDISMainFlucFund.xml%26divisionId%3DMDIS01006002000000%26serviceId%3DSDIS01006002000%7C%7C%ED%8E%80%EB%93%9C%20%EC%88%98%EC%9D%B5%EB%B9%84%EC%9A%A9%20%EA%B3%84%EC%82%B0%EA%B8%B0%3D%3D%2Fwebsquare%2Findex.jsp%3Fw2xPath%3D%2Fwq%2Ffundcal%2FDISIdvFndSrch.xml%26divisionId%3DMDIS01014000000000%26serviceId%3DSDIS01014000000',
        'Host': 'dis.kofia.or.kr',
        'Origin': 'https://dis.kofia.or.kr',
        'Referer': 'https://dis.kofia.or.kr/websquare/popup.html?w2xPath=/wq/com/popup/DISComFundSmryInfo.xml&companyCd=A01015&standardCd=KR5207AH8742&standardDt=20220103&grntGb=S&search=&check=1&isMain=undefined&companyGb=A&uFundNm=/v+tULz0xUXArABUAG8AbQBvAHIAcgBvAHfHpa4wxrC3ycmdrYzSLMeQwuDQwQBLAC0AIAAxACjM%0ARK2MACkAQwBsAGEAcwBzAEMALQBQADI%3D&popupID=undefined&w2xHome=/wq/cmpann/&w2xDocumentRoot=',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36'
    }

    res = requests.post(url, data=xml_str, headers=headers,
                        # proxies=proxies
                        ).text
    fund_std_info_df = pd.read_xml(res, xpath='.//COMFundBasInfoOutDTO')

    # product_info DB에 넣을 항목들만 남기고 드롭 후 컬럼명 바꾸기
    fund_std_info_df = fund_std_info_df.drop(columns=['vAdditionalEstMtdNm',
                                                      'shortCd',
                                                      'vProfitTypeCdNm',
                                                      'establishmentCot',
                                                      'trustTrm',
                                                      'manageRewRate',
                                                      'saleRewRate',
                                                      'trustRewRate',
                                                      'generalOfctrtrewRate',
                                                      'rewSum',
                                                      'vGeneralOfctrtcompNm',
                                                      'vTrustCompNm',
                                                      'standardDt',
                                                      'uNoVal5',
                                                      'uNoVal6',
                                                      'uNoVal7',
                                                      'uNoVal8',
                                                      'uNoVal9',
                                                      'uNoVal10',
                                                      'vImg',
                                                      'subClassCd',
                                                      'val1',
                                                      'val2',
                                                      'val3',
                                                      'establishmentDt']
                                             )

    fund_std_info_df = fund_std_info_df.rename(
        columns={
            'vFundGbNm': 'category',
            'uFundTypNm': 'fund_type',
            # 'vAdditionalEstMtdNm':'추가/단위구분',
            # 'establishmentDt': 'listing_dt',
            'classCd': 'class_cd',
            # 'shortCd':'단축코드',
            'trustAccTrm': 'trust_accounting_term',
            'vInvestRgnGbNm': 'invest_region',
            'vSaleRgnGbNm': 'sales_region',
            # 'vProfitTypeCdNm':'운용실적공시분류',
            'vTraitDivNm': 'trait_division',
            'vPriPubGBNm': 'private_public',
            # 'establishmentCot':'최초설정기준가격',
            # 'trustTrm':'신탁기간',
            # 'manageRewRate':'운용보수',
            # 'saleRewRate':'판매보수',
            # 'trustRewRate':'수탁보수',
            # 'generalOfctrtrewRate':'일반사무관리보수',
            # 'rewSum':'보수합계',
            # 'ter':'총비용비율(TER)',
            'frontendCmsRate': 'frontend_commission_rt',
            'backendCmsRate': 'backend_commission_rt',
            'vManageCompNm': 'mng_comp',
            # 'vGeneralOfctrtcompNm':'일반사무관리회사',
            # 'vTrustCompNm':'수탁회사',
            # 'standardDt':'기준일',
            'companyCd': 'comp_cd',
            # 'uNoVal5':'혼합채권형_유형평균보수_비율_운용보수',
            # 'uNoVal6':'혼합채권형_유형평균보수_비율_판매보수',
            # 'uNoVal7':'혼합채권형_유형평균보수_비율_수탁보수',
            # 'uNoVal8':'혼합채권형_유형평균보수_비율_일반사무관리보수',
            # 'uNoVal9':'혼합채권형_유형평균보수_비율_보수합계',
            # 'uNoVal10':'혼합채권형_유형평균보수_비율_총비용비율(TER)',
            'val4': 'status'
        }
    )

    fund_info_df = fund_std_info_df.copy()

    name_list = get_fund_name_sr(base_dt)
    fund_info_df['product_name'] = name_list.loc[ticker]

    fund_info_df['ticker'] = ticker
    fund_info_df = fund_info_df.set_index('ticker')

    daily_fund_df = get_fund_daily(base_dt)
    daily_fund_df['listing_dt'] = pd.to_datetime(daily_fund_df['listing_dt'], format='%Y%m%d').dt.strftime('%Y-%m-%d')
    daily_fund_sr = daily_fund_df.set_index('ticker')['listing_dt']
    fund_info_df = fund_info_df.join(daily_fund_sr)

    # fund_info_df['delisting_dt'] = []
    fund_info_df['updated_at'] = datetime.today().strftime('%Y-%m-%d')

    return fund_info_df
