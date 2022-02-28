import pandas as pd
import requests
from datetime import datetime
import datetime as dt
import numpy as np
import os
from fund_kr.backup import (unreset_price)

PREFIX = 'cached_fund_price'
PREFIX_adj = 'fund_adj_pr'
CACHE_PATH = os.getenv('CACHE_PATH', '.')
today = datetime.today().strftime('%Y%m%d')


def get_fund_historical_price(ticker):
    """
    펀드코드별 역대 기준가격 가져오기
    -------------------------
    :param:
        ticker: 펀드코드
    :return: DataFrame
        펀드가격정보
    """
    cache_file_path = f'{CACHE_PATH}/{PREFIX}_{ticker}.csv'
    if os.path.isfile(cache_file_path):
        return pd.read_csv(cache_file_path)

    url = 'https://dis.kofia.or.kr/proframeWeb/XMLSERVICES/'

    xml = f"""<?xml version="1.0" encoding="utf-8"?>
    <message>
      <proframeHeader>
        <pfmAppName>FS-COM</pfmAppName>
        <pfmSvcName>COMFundPriceModSO</pfmSvcName>
        <pfmFnName>priceModSrch</pfmFnName>
      </proframeHeader>
      <systemHeader></systemHeader>
        <COMFundUnityInfoInputDTO>
        <standardCd>{ticker}</standardCd>
        <companyCd></companyCd>
        <vSrchTrmFrom>19850311</vSrchTrmFrom>
        <vSrchTrmTo>{today}</vSrchTrmTo>
        <vSrchStd>1</vSrchStd>
    </COMFundUnityInfoInputDTO>
    </message>"""

    headers = {
        'Accept': 'text/xml',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
        'Connection': 'keep-alive',
        'Content-Type': 'text/xml',
        'Cookie': '__smVisitorID=Qhfls34NRgD; userGb=01; JSESSIONID=NtxpBIhlNAlgag8DL7AbTnlOYOUagT6qK8xweQXjwNMdcVFSpYP11XHGWgXLREMo.ap2_servlet_kofiadisEngine; disTdMenu=%ED%8E%80%EB%93%9C%EA%B8%B0%EC%A4%80%EA%B0%80%EA%B2%A9%3D%3D%2Fwebsquare%2Findex.jsp%3Fw2xPath%3D%2Fwq%2Ffundann%2FDISFundStdPrice.xml%26divisionId%3DMDIS01004001000000%26serviceId%3DSDIS01004001000%7C%7C%EA%B8%B0%EC%A4%80%EA%B0%80%EA%B2%A9%EB%93%B1%EB%9D%BD%EB%A5%A0%3D%3D%2Fwebsquare%2Findex.jsp%3Fw2xPath%3D%2Fwq%2Ffundann%2FDISFundStdPrcRate.xml%26divisionId%3DMDIS01004003000000%26serviceId%3DSDIS01004003000%7C%7C',
        'Host': 'dis.kofia.or.kr',
        'Origin': 'https://dis.kofia.or.kr',
        'Referer': 'https://dis.kofia.or.kr/websquare/popup.html?w2xPath=/wq/com/popup/DISComFundSmryInfo.xml&companyCd=20000701&standardCd=KR5101300253&standardDt=20220204&grntGb=S&search=&check=1&isMain=undefined&companyGb=A&uFundNm=/v+sHMd4xfCuCMj8wt3WPNVpuqjC4NDB&popupID=undefined&w2xHome=/wq/fundann/&w2xDocumentRoot=',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.80 Safari/537.36'
    }

    res = requests.post(url, data=xml, headers=headers).text
    fund_price_df = pd.read_xml(res, xpath='.//priceModList')

    fund_price_df['code'] = ticker
    fund_price_df = fund_price_df[['code', 'standardDt', 'standardCot', 'standardassStdCot', 'uOriginalAmt']].copy()
    fund_price_df = fund_price_df.rename(columns={'standardassStdCot': 'tax_base_nav',
                                                  'uOriginalAmt': 'aum'})
    fund_price_df['standardDt'] = pd.to_datetime(fund_price_df['standardDt'], format='%Y%m%d')
    fund_price_df = fund_price_df.sort_values(['code', 'standardDt'], ascending=True)

    fund_price_df.to_csv(cache_file_path, encoding='utf-8-sig')

    return fund_price_df


def get_adj_pr(ticker):
    """
    수정기준가 생성하여 기준가격 정보에 조인
    ------------------------------
    :param:
        ticker: 펀드코드
    :return: DataFrame
        수정기준가격 컬럼이 포함된 가격 정보
    """
    unreset_df = unreset_price(ticker)
    price_df = get_fund_historical_price(ticker)

    one_pr = price_df[price_df['code'] == ticker].copy()
    one_adj = unreset_df[unreset_df['code'] == ticker].copy()

    one_sr = one_pr.set_index('standardDt')['standardCot']
    one_sr.index = pd.to_datetime(one_sr.index)

    one_adj['trust_end_dt'] = pd.to_datetime(one_adj['trust_end_dt'])
    """
    회계기말일에 분배가 발생하고, 다음 거래일에 가격이 조정된다.
    수정기준가로 대체할 거래일자를 맞추기 위해서 get_loc 함수를 사용한다.
    거래일 날짜 일치여부를 확인하기 위해서 그 전에 하루를 뒤로 민다.
    """
    one_adj['trust_end_dt'] = one_adj['trust_end_dt'] + dt.timedelta(days=1)
    """
    get_loc 으로 기준가 데이터 거래일과 일치하는 날짜가 있으면 해당 날짜로 설정 
    일치하는 날짜가 없으면 다시 뒤에 있는 날짜와 일치 여부 확인
    """
    one_adj.index = one_sr.index[one_sr.index.get_indexer(one_adj['trust_end_dt'], method='bfill')]

    # end_date = one_adj['trust_end_dt'].tolist()

    # dvdnd_dt = []
    # for d in end_date:
    #     # dvdnd_dt.append(one_sr.index[one_sr.index.get_loc(f'{d}', method='bfill')])
    #     # dvdnd_dt.append(one_sr.index[pd.to_datetime(one_sr.index).get_indexer([d], method='bfill')])
    #     # dvdnd_dt.append(one_sr.index.get_indexer([d], method='bfill'))
    #     dvdnd_dt.append(one_sr.index[one_sr.index.get_indexer([d], method='bfill')][0])

    # one_adj.index = dvdnd_dt

    one_df = one_adj.drop(columns=['code', 'trust_end_dt']).rename(columns={'standardCot': 'dvdnd_pr'})

    one_pr = one_pr.set_index('standardDt')
    one_pr.index = pd.to_datetime(one_pr.index)
    one_pr = one_pr.join(one_df, how='outer', lsuffix='_org', rsuffix='_adj')


    one_pr['dv_price'] = np.where(one_pr['dvdnd_pr'].notna(), one_pr.dvdnd_pr, one_pr.standardCot)
    one_pr['dly_rtn_notna'] = np.where(one_pr['dvdnd_pr'].notna(), one_pr.dv_price.pct_change(),
                                       one_pr.dv_price / (one_pr.standardCot.shift(1)))
    one_pr['dly_rtn_isna'] = np.where(one_pr['dvdnd_pr'].isna(), one_pr.dv_price.pct_change(),
                                      one_pr.dv_price / (one_pr.standardCot.shift(1)))

    dividend_dates = one_pr['dvdnd_pr'].dropna().index
    one_pr.loc[dividend_dates, 'dly_rtn_notna'] = one_pr.loc[dividend_dates, 'dly_rtn_isna']

    one_pr['adj_pr'] = one_pr['dly_rtn_notna']
    one_pr.loc[one_pr.index[0], 'adj_pr'] = one_pr.loc[one_pr.index[0], 'dv_price']
    one_pr['adj_pr'] = one_pr['adj_pr'].cumprod()

    one_pr = one_pr.drop(columns='dly_rtn_isna').rename(columns={'dly_rtn_notna': 'dly_rtn'})

    daily_df = one_pr.copy()
    daily_df = daily_df.rename(columns={
        'code': 'ticker',
        'index': 'base_dt',
        'standardCot': 'nav',
        'standardassStdCot': 'tax_base_nav',
        'uOriginalAmt': 'aum'
    }
    )
    daily_df = daily_df.drop(columns=['Unnamed: 0', 'dvdnd_pr', 'dv_price', 'dly_rtn'])

    # daily_df.to_csv(f'{CACHE_PATH}/{PREFIX_adj}_{ticker}.csv')

    return daily_df
