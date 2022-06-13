import pandas as pd
import requests


def get_new_fund_list(start_dt=None, end_dt=None):
    url = 'https://dis.kofia.or.kr/proframeWeb/XMLSERVICES/'
    xml = f"""<?xml version="1.0" encoding="utf-8"?>
    <message>
      <proframeHeader>
        <pfmAppName>FS-DIS2</pfmAppName>
        <pfmSvcName>DISNewEstSO</pfmSvcName>
        <pfmFnName>select</pfmFnName>
      </proframeHeader>
      <systemHeader></systemHeader>
        <DISCondFuncDTO>
        <tmpV30>{start_dt}</tmpV30>
        <tmpV31>{end_dt}</tmpV31>
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
        'Referer': 'https://dis.kofia.or.kr/websquare/index.jsp?w2xPath=/wq/fundann/DISNewEst.xml&divisionId=MDIS01006001000000&serviceId=SDIS01006001000'
    }
    res = requests.post(url, data=xml, headers=headers).text
    df = pd.read_xml(res, xpath='.//selectMeta')
    df = df[['tmpV2', 'tmpV3', 'tmpV10']]
    df = df.rename(columns={
        'tmpV2': 'product_name',
        'tmpV3': 'listing_dt',
        'tmpV10': 'ticker'
    })
    new_tickers_list = df['ticker'].tolist()

    return new_tickers_list


if __name__ == '__main__':
    start_dt = '20220427'
    end_dt = '20220427'
    new_funds_list = get_new_fund_list(start_dt, end_dt)
