import pandas as pd
import requests
from datetime import datetime
import datetime as dt
import numpy as np
from rf_scraper.site.fund_kr.api.common import apply_proxies


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

    headers = {'Host': 'dis.kofia.or.kr',
               'Origin': 'https://dis.kofia.or.kr',
               'Referer': 'https://dis.kofia.or.kr/websquare/popup.html?w2xPath=/wq/com/popup/DISComFundSmryInfo.xml&companyCd=&standardCd=K55370BU1789&standardDt=&grntGb=S&search=&check=1&isMain=undefined&companyGb=A&uFundNm=/v8AQQBCu/itba34uFzCpMmdrYzSLMeQwuDQwQAoyPzC3QAtx6ysBMgR1hUAKciFuVjWFQBDAGUA%0ALQBQADI%3D&popupID=undefined&w2xHome=/wq/fundann/&w2xDocumentRoot=',
               }

    res = requests.post(url, data=xml, headers=headers).text

    unreset_price_df = pd.read_xml(res, xpath='.//settleExList')

    unreset_price_df['ticker'] = ticker

    unreset_price_df = unreset_price_df[['ticker', 'trustAccend', 'standardCot']].copy()
    unreset_price_df = unreset_price_df.rename(columns={'trustAccend': 'trust_end_dt',
                                                        'standardCot': 'dvd_pr'})
    unreset_price_df = unreset_price_df[(unreset_price_df['dvd_pr'] > 0.0001) | (unreset_price_df['dvd_pr'] < -0.0001)]
    unreset_price_df['trust_end_dt'] = pd.to_datetime(unreset_price_df['trust_end_dt'], format='%Y%m%d')
    unreset_price_df = unreset_price_df.sort_values(['ticker', 'trust_end_dt'], ascending=True)

    return unreset_price_df


def get_fund_historical_price(ticker):
    """
    펀드코드별 역대 기준가격 가져오기
    -------------------------
    :param:
        ticker: 펀드코드
    :return: DataFrame
        펀드가격정보
    """
    today = datetime.today().strftime('%Y%m%d')

    url = 'https://dis.kofia.or.kr/proframeWeb/XMLSERVICES/'

    xml = f"""<?xml version="1.0" encoding="utf-8"?>
        <message>
          <proframeHeader>
            <pfmAppName>FS-DIS2</pfmAppName>
            <pfmSvcName>DISFundStdPrcStutSO</pfmSvcName>
            <pfmFnName>select</pfmFnName>
          </proframeHeader>
          <systemHeader></systemHeader>
            <DISCondFuncDTO>
            <tmpV30>19000101</tmpV30>
            <tmpV31>20220426</tmpV31>
            <tmpV10>0</tmpV10>
            <tmpV12>{ticker}</tmpV12>
        </DISCondFuncDTO>
        </message>"""

    headers = {'Host': 'dis.kofia.or.kr',
               'Origin': 'https://dis.kofia.or.kr',
               'Referer': 'https://dis.kofia.or.kr/websquare/popup.html',
               }

    kwargs = apply_proxies()
    res = requests.post(url, data=xml, headers=headers, **kwargs).text
    fund_price_df = pd.read_xml(res, xpath='.//selectMeta')

    fund_price_df['ticker'] = ticker
    fund_price_df = fund_price_df[['ticker', 'tmpV1', 'tmpV2', 'tmpV4', 'tmpV5']].copy()
    fund_price_df = fund_price_df.rename(columns={'tmpV1': 'base_dt',
                                                  'tmpV2': 'nav',
                                                  'tmpV4': 'tax_base_nav',
                                                  'tmpV5': 'aum',
                                                  })
    fund_price_df['base_dt'] = pd.to_datetime(fund_price_df['base_dt'], format='%Y%m%d')
    fund_price_df = fund_price_df.sort_values(['ticker', 'base_dt'], ascending=True)

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
    price_df = get_fund_historical_price(ticker)

    unreset_df = unreset_price(ticker)

    if unreset_df.empty:
        # 결산이 없으면 그대로 수정주가 그냥 복사
        price_df['adj_pr'] = price_df['nav']
        price_df = price_df.set_index(['base_dt', 'ticker'])
        return price_df
    
    one_pr = price_df[price_df['ticker'] == ticker].copy()
    one_adj = unreset_df[unreset_df['ticker'] == ticker].copy()

    one_sr = one_pr.set_index('base_dt')['nav']
    one_sr.index = pd.to_datetime(one_sr.index)

    one_adj['trust_end_dt'] = pd.to_datetime(one_adj['trust_end_dt'])
    """
    회계기말일에 분배가 발생하고, 다음 거래일에 가격이 조정된다.
    수정기준가로 대체할 거래일자를 맞추기 위해서 get_indexer 함수를 사용한다.
    거래일 날짜 일치 여부를 확인 하기 위해서 그 전에 하루를 뒤로 민다.
    """
    one_adj['trust_end_dt'] = one_adj['trust_end_dt'] + dt.timedelta(days=1)
    """
    get_loc 으로 기준가 데이터 거래일과 일치 하는 날짜가 있으면 해당 날짜로 설정 
    일치 하는 날짜가 없으면 다시 뒤에 있는 거래일과 일치 여부 확인 하여 일치 하면 기준가로 채워 넣기
    """
    one_adj.index = one_sr.index[one_sr.index.get_indexer(one_adj['trust_end_dt'], method='bfill')]

    one_df = one_adj.drop(columns=['ticker', 'trust_end_dt'])

    one_pr = one_pr.set_index('base_dt')
    one_pr.index = pd.to_datetime(one_pr.index)
    one_pr = one_pr.join(one_df, how='outer', lsuffix='_org', rsuffix='_adj')

    one_pr['dv_price'] = np.where(one_pr['dvd_pr'].notna(), one_pr.dvd_pr, one_pr['nav'])
    one_pr['dly_rtn_notna'] = np.where(one_pr['dvd_pr'].notna(), one_pr['dv_price'].pct_change(),
                                       one_pr['dv_price'] / (one_pr['nav'].shift(1)))
    one_pr['dly_rtn_isna'] = np.where(one_pr['dvd_pr'].isna(), one_pr['dv_price'].pct_change(),
                                      one_pr['dv_price'] / (one_pr['nav'].shift(1)))

    dvd_dates = one_pr['dvd_pr'].dropna().index
    one_pr.loc[dvd_dates, 'dly_rtn_notna'] = one_pr.loc[dvd_dates, 'dly_rtn_isna']

    one_pr['adj_pr'] = one_pr['dly_rtn_notna']
    one_pr.loc[one_pr.index[0], 'adj_pr'] = one_pr.loc[one_pr.index[0], 'dv_price']
    one_pr['adj_pr'] = one_pr['adj_pr'].cumprod().round(decimals=12)

    one_pr = one_pr.drop(columns='dly_rtn_isna').rename(columns={'dly_rtn_notna': 'dly_rtn'})

    daily_df = one_pr.copy()
    daily_df = daily_df.drop(columns=['dvd_pr', 'dv_price', 'dly_rtn'])

    daily_df = daily_df.reset_index()
    daily_df = daily_df.rename(columns={'index': 'base_dt'})
    daily_df['base_dt'] = pd.to_datetime(daily_df['base_dt'])
    daily_df['base_dt'] = daily_df['base_dt'].dt.strftime('%Y-%m-%d')
    daily_df = daily_df.set_index(['base_dt', 'ticker'])

    return daily_df