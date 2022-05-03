import pandas as pd
import requests
from scraper.fund_kr.api.backup import (get_fund_name_sr)
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
        'Host': 'dis.kofia.or.kr',
        'Origin': 'https://dis.kofia.or.kr',
        'Referer': 'https://dis.kofia.or.kr/websquare/popup.html?w2xPath=/wq/com/popup/DISComFundSmryInfo.xml&companyCd=A01015&standardCd=KR5207AH8742&standardDt=20220103&grntGb=S&search=&check=1&isMain=undefined&companyGb=A&uFundNm=/v+tULz0xUXArABUAG8AbQBvAHIAcgBvAHfHpa4wxrC3ycmdrYzSLMeQwuDQwQBLAC0AIAAxACjM%0ARK2MACkAQwBsAGEAcwBzAEMALQBQADI%3D&popupID=undefined&w2xHome=/wq/cmpann/&w2xDocumentRoot=',
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

    return fund_info_df


def code_info_added(fund_info_df):
    df = fund_info_df
    # class type (5차 분류) 6번째 코드
    df['class_type'] = df['class_cd'].str.slice(5, 6)
    df['class_type'] = df['class_type'].replace('A', '클래스P')
    df['class_type'] = df['class_type'].replace('B', '클래스W')
    df['class_type'] = df['class_type'].replace('C', '클래스J')
    df['class_type'] = df['class_type'].replace('D', '클래스S')
    df['class_type'] = df['class_type'].replace('E', '클래스S-P')
    df['class_type'] = df['class_type'].replace('F', '클래스S-T')
    df['class_type'] = df['class_type'].replace('G', '클린클래스')
    df['class_type'] = df['class_type'].replace('Y', '그 외 클래스')
    df['class_type'] = df['class_type'].replace('Z', '일반')
    df['class_type'] = df['class_type'].replace('1', '운용')
    df['class_type'] = df['class_type'].replace('2', '클래스A')
    df['class_type'] = df['class_type'].replace('3', '클래스B')
    df['class_type'] = df['class_type'].replace('4', '클래스C')
    df['class_type'] = df['class_type'].replace('5', '클래스D')
    df['class_type'] = df['class_type'].replace('6', '클래스E')
    df['class_type'] = df['class_type'].replace('7', '클래스F')
    df['class_type'] = df['class_type'].replace('8', '클래스H')
    df['class_type'] = df['class_type'].replace('9', '클래스I')
    # redemption charge (8차 분류) 9번째 코드
    df['redemption_charge'] = df['class_cd'].str.slice(9, 10)
    df['redemption_charge'] = df['redemption_charge'].replace('0', '환매수수료없음')
    df['redemption_charge'] = df['redemption_charge'].replace('1', '1개월 미만')
    df['redemption_charge'] = df['redemption_charge'].replace('6', '1년 미만')
    df['redemption_charge'] = df['redemption_charge'].replace('4', '6개월 미만')
    df['redemption_charge'] = df['redemption_charge'].replace('2', '2개월 미만')
    df['redemption_charge'] = df['redemption_charge'].replace('9', '2년 이상')
    df['redemption_charge'] = df['redemption_charge'].replace('3', '3개월 미만')
    df['redemption_charge'] = df['redemption_charge'].replace('5', '9개월 미만')
    df['redemption_charge'] = df['redemption_charge'].replace('8', '2년 미만')
    df['redemption_charge'] = df['redemption_charge'].replace('7', '1년6개월 미만')
    df['redemption_charge'] = df['redemption_charge'].replace('A', '환매불가')
    # characteristics (9차 분류) 10, 11번째 코드
    df['characteristics'] = df['class_cd'].str.slice(10, 12)
    df['characteristics'] = df['characteristics'].replace('01', '일반형')
    df['characteristics'] = df['characteristics'].replace('02', '개인연금형')
    df['characteristics'] = df['characteristics'].replace('03', '세금우대형')
    df['characteristics'] = df['characteristics'].replace('04', '근로자장기저축형')
    df['characteristics'] = df['characteristics'].replace('05', '재형저축')
    df['characteristics'] = df['characteristics'].replace('06', '가계장기저축형')
    df['characteristics'] = df['characteristics'].replace('07', '일반적립형')
    df['characteristics'] = df['characteristics'].replace('08', '보장형')
    df['characteristics'] = df['characteristics'].replace('09', '원금보장형')
    df['characteristics'] = df['characteristics'].replace('10', '근로자우대')
    df['characteristics'] = df['characteristics'].replace('11', '목표달성형')
    df['characteristics'] = df['characteristics'].replace('12', '전환형')
    df['characteristics'] = df['characteristics'].replace('13', '공사채-주식연계형')
    df['characteristics'] = df['characteristics'].replace('14', '특정업종선택형')
    df['characteristics'] = df['characteristics'].replace('15', 'INDEX형')
    df['characteristics'] = df['characteristics'].replace('16', '특정회사투자형(자사주상품)')
    df['characteristics'] = df['characteristics'].replace('17', '대형주형')
    df['characteristics'] = df['characteristics'].replace('18', '중소형주형')
    df['characteristics'] = df['characteristics'].replace('19', '공사채형 중 전환사채편입형')
    df['characteristics'] = df['characteristics'].replace('20', '전환사채형')
    df['characteristics'] = df['characteristics'].replace('21', 'System운용형')
    df['characteristics'] = df['characteristics'].replace('22', 'VentureCapital')
    df['characteristics'] = df['characteristics'].replace('23', '장외주식형')
    df['characteristics'] = df['characteristics'].replace('25', '공모주혼합형')
    df['characteristics'] = df['characteristics'].replace('26', 'Umbrella형')
    df['characteristics'] = df['characteristics'].replace('27', '하이일드')
    df['characteristics'] = df['characteristics'].replace('28', 'CBO(후순위채)')
    df['characteristics'] = df['characteristics'].replace('29', '분리과세')
    df['characteristics'] = df['characteristics'].replace('30', 'Wrap Account')
    df['characteristics'] = df['characteristics'].replace('34', '연기금')
    df['characteristics'] = df['characteristics'].replace('36', '연금저축')
    df['characteristics'] = df['characteristics'].replace('37', '차익거래형')
    df['characteristics'] = df['characteristics'].replace('38', 'M&A')
    df['characteristics'] = df['characteristics'].replace('41', '기금풀(주간)')
    df['characteristics'] = df['characteristics'].replace('42', '기금풀(개별)')
    df['characteristics'] = df['characteristics'].replace('43', '공모주채권형')
    df['characteristics'] = df['characteristics'].replace('44', 'ETF(상장지수펀드)')
    df['characteristics'] = df['characteristics'].replace('45', '장기주택마련(비과세장기주택마련저축)')
    df['characteristics'] = df['characteristics'].replace('46', '원금보존추구형')
    df['characteristics'] = df['characteristics'].replace('47', 'ELS투자펀드')
    df['characteristics'] = df['characteristics'].replace('48', '카드채')
    df['characteristics'] = df['characteristics'].replace('49', '국공채')
    df['characteristics'] = df['characteristics'].replace('55', '엔터테인먼트')
    df['characteristics'] = df['characteristics'].replace('60', '퇴직연금')
    df['characteristics'] = df['characteristics'].replace('61', 'SRI펀드')
    df['characteristics'] = df['characteristics'].replace('65', '장기주식형대상펀드')
    df['characteristics'] = df['characteristics'].replace('66', '채권시장안정펀드(주간)')
    df['characteristics'] = df['characteristics'].replace('67', '채권시장안정펀드(개별)')
    df['characteristics'] = df['characteristics'].replace('68', '일반상품(농산물)')
    df['characteristics'] = df['characteristics'].replace('69', '일반상품(금속등)')
    df['characteristics'] = df['characteristics'].replace('70', '녹색인증대상투자')
    df['characteristics'] = df['characteristics'].replace('71', '월지급식펀드')
    df['characteristics'] = df['characteristics'].replace('72', '일반 사모펀드')
    df['characteristics'] = df['characteristics'].replace('73', '소득공제장기펀드')
    df['characteristics'] = df['characteristics'].replace('74', '정부.공공기금풀(주간)')
    df['characteristics'] = df['characteristics'].replace('75', '정부.공공기금풀(개별)')
    df['characteristics'] = df['characteristics'].replace('76', '민간기금풀(주간)')
    df['characteristics'] = df['characteristics'].replace('77', '민간기금풀(개별)')
    df['characteristics'] = df['characteristics'].replace('78', '기타기금풀(주간)')
    df['characteristics'] = df['characteristics'].replace('79', '기타기금풀(개별)')
    df['characteristics'] = df['characteristics'].replace('80', '성과보수')
    df['characteristics'] = df['characteristics'].replace('81', '자산배분')
    df['characteristics'] = df['characteristics'].replace('82', '사모투자재간접(공모)')
    df['characteristics'] = df['characteristics'].replace('83', '부동산.특별자산투자재간접(공모)')
    df['characteristics'] = df['characteristics'].replace('84', '경영참여 목적 일반사모펀드')
    # locations (10차 분류) 12, 13번째 코드
    df['locations'] = df['class_cd'].str.slice(12, 14)
    df['locations'] = df['locations'].replace('01', '대한민국')
    df['locations'] = df['locations'].replace('02', '글로벌')
    df['locations'] = df['locations'].replace('03', '아시아')
    df['locations'] = df['locations'].replace('04', '아시아(X-Japan)')
    df['locations'] = df['locations'].replace('05', '동남아시아')
    df['locations'] = df['locations'].replace('06', '친디아')
    df['locations'] = df['locations'].replace('07', '러시아')
    df['locations'] = df['locations'].replace('08', '서유럽')
    df['locations'] = df['locations'].replace('09', '동유럽')
    df['locations'] = df['locations'].replace('10', '북미')
    df['locations'] = df['locations'].replace('11', '중남미')
    df['locations'] = df['locations'].replace('12', '브릭스')
    df['locations'] = df['locations'].replace('13', '중동')
    df['locations'] = df['locations'].replace('14', '아프리카')
    df['locations'] = df['locations'].replace('15', '호주(뉴질랜드)')
    df['locations'] = df['locations'].replace('16', '일본')
    df['locations'] = df['locations'].replace('17', '중국(홍콩)')
    df['locations'] = df['locations'].replace('18', '인도')
    df['locations'] = df['locations'].replace('19', '베트남')
    df['locations'] = df['locations'].replace('20', '말레이시아')
    df['locations'] = df['locations'].replace('21', '북유럽')
    df['locations'] = df['locations'].replace('22', '글로벌(선진국)')
    df['locations'] = df['locations'].replace('23', '글로벌(신흥국가)')
    df['locations'] = df['locations'].replace('24', '유럽')
    df['locations'] = df['locations'].replace('25', '대중국(중국,홍콩,대만)')
    df['locations'] = df['locations'].replace('26', '아시아퍼시픽')
    df['locations'] = df['locations'].replace('27', '아시아퍼시픽(X-Japan)')
    df['locations'] = df['locations'].replace('28', 'EMEA')
    # risk level (14차 분류) 20번째 코드
    df['risk_level'] = df['class_cd'].str.slice(19, 20)
    df['risk_level'] = df['risk_level'].replace('A', '1')
    df['risk_level'] = df['risk_level'].replace('B', '2')
    df['risk_level'] = df['risk_level'].replace('C', '3')
    df['risk_level'] = df['risk_level'].replace('D', '4')
    df['risk_level'] = df['risk_level'].replace('E', '5')
    df['risk_level'] = df['risk_level'].replace('F', '6')
    # is_hedged 20번째 코드
    df['is_hedged'] = df['class_cd'].str.slice(19, 20)
    df['is_hedged'] = df['is_hedged'].replace('1', 'UH')
    df['is_hedged'] = df['is_hedged'].replace('2', 'UH')
    df['is_hedged'] = df['is_hedged'].replace('3', 'UH')
    df['is_hedged'] = df['is_hedged'].replace('4', 'UH')
    df['is_hedged'] = df['is_hedged'].replace('5', 'UH')
    df['is_hedged'] = df['is_hedged'].replace('6', 'UH')
    df['is_hedged'] = df['is_hedged'].replace('A', 'H')
    df['is_hedged'] = df['is_hedged'].replace('B', 'H')
    df['is_hedged'] = df['is_hedged'].replace('C', 'H')
    df['is_hedged'] = df['is_hedged'].replace('D', 'H')
    df['is_hedged'] = df['is_hedged'].replace('E', 'H')
    df['is_hedged'] = df['is_hedged'].replace('F', 'H')

    return df

if __name__ == '__main__':
    BASEDATE = '20220502'
    TICKER = 'K55101B55361'
    # df = get_fund_info(BASEDATE, TICKER)
    df = pd.read_csv('/Users/user/dataknows/test.csv', encoding='utf-8-sig')
    added_df = code_info_added(df)
    dd=0