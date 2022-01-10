import requests
import pandas as pd
from datetime import datetime
import time
import random

#saleComp = pd.read_csv('C:/Users/s/PycharmProjects/fund_standard_price_Crawling/saleComp.csv', encoding='cp949')
date_list = pd.date_range(start='2000-01-01', end='2022-01-10')
date_list = date_list.strftime('%Y%m%d')

url = 'https://dis.kofia.or.kr/proframeWeb/XMLSERVICES/'

for date in date_list:
    xml_str = f"""<?xml version="1.0" encoding="utf-8"?>
    <message>
      <proframeHeader>
        <pfmAppName>FS-DIS2</pfmAppName>
        <pfmSvcName>DISFundStdPriceSO</pfmSvcName>
        <pfmFnName>select</pfmFnName>
      </proframeHeader>
      <systemHeader></systemHeader>
        <DISCondFuncDTO>
        <tmpV30>{date}</tmpV30>
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

    headers = {
        'Accept': 'text/xml',
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

    res = requests.post(url, data=xml_str, headers=headers).text

    try:
        fund_std_price_df = pd.read_xml(res, xpath='.//selectMeta')
    except:
        print(f'empty data. {date}')
        continue

    fund_std_price_df = fund_std_price_df.loc[:, 'tmpV2':'tmpV14']

    fund_std_price_df = fund_std_price_df.rename(
           columns={'tmpV14':'기준일자',
                    'tmpV13':'판매회사',
                    'tmpV12':'펀드코드',
                    'tmpV2':'펀드명',
                    'tmpV4':'설정일',
                    'tmpV5':'설정원본(백만원)',
                    'tmpV6':'기준가격(원)_기준',
                    'tmpV7':'기준가격(원)_과표',
                    'tmpV3':'펀드유형',
                    'tmpV8':'자산구성(백만원)_주식',
                    'tmpV9':'자산구성(백만원)_채권',
                    'tmpV10':'자산구성(백만원)_유동',
                    'tmpV11':'투자운용인력'}
    )


    fund_std_price_df.to_csv('C:/Users/s/PycharmProjects/fund_standard_price_Crawling/일별_펀드기준가격/{}.csv'.format(date), encoding='cp949')
    print(f'saved. {date}')

    time.sleep(random.randint(1,3))
