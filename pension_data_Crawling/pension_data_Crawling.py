import pandas as pd
import requests
import time


url = 'https://dis.kofia.or.kr/proframeWeb/XMLSERVICES/'

date_list = pd.date_range(start='2003-01-01', end='2022-01-18').strftime('%Y%m%d')

for date in date_list:
    xml_str = f"""<?xml version="1.0" encoding="utf-8"?>
    <message>
      <proframeHeader>
        <pfmAppName>FS-DIS2</pfmAppName>
        <pfmSvcName>DISPensionSO</pfmSvcName>
        <pfmFnName>select</pfmFnName>
      </proframeHeader>
      <systemHeader></systemHeader>
        <DISCondFuncDTO>
        <tmpV30>{date}</tmpV30>
        <tmpV4></tmpV4>
        <tmpV16></tmpV16>
        <tmpV11></tmpV11>
        <tmpV12></tmpV12>
        <tmpV5></tmpV5>
        <tmpV7>1</tmpV7>
        <tmpV3></tmpV3>
        <tmpV40>1000000</tmpV40>
    </DISCondFuncDTO>
    </message>"""

    headers = {
        'Cookie': '__smVisitorID=V4ubac3GJYX; userGb=01; JSESSIONID=J417EdajNtB5M2DY2ZwanQvRsaKF58OOy5by8ioDufFDPOzVpecHKZVaXYTVJ4OB.ap2_servlet_kofiadisEngine; disTdMenu=%EC%97%B0%EA%B8%88%EC%83%81%ED%92%88%EA%B3%B5%EC%8B%9C%3D%3D%2Fwebsquare%2Findex.jsp%3Fw2xPath%3D%2Fwq%2Fcmpann%2FDISPension.xml%26divisionId%3DMDIS01010001000000%26serviceId%3DSDIS01010001000%7C%7C%EC%97%B0%EA%B8%88%EC%83%81%ED%92%88%EC%83%81%EC%84%B8%EC%88%98%EC%9D%B5%EB%A5%A0%3D%3D%2Fwebsquare%2Findex.jsp%3Fw2xPath%3D%2Fwq%2Fcmpann%2FDISPensionProfit.xml%26divisionId%3DMDIS01010003000000%26serviceId%3DSDIS01010003000%7C%7C%EC%98%A8%EB%9D%BC%EC%9D%B8%EC%A0%84%EC%9A%A9%ED%8E%80%EB%93%9C%3D%3D%2Fwebsquare%2Findex.jsp%3Fw2xPath%3D%2Fwq%2Ffundann%2FDISOnlineFund.xml%26divisionId%3DMDIS01007001000000%26serviceId%3DSDIS01007001000%7C%7C%EC%9E%A5%EA%B8%B0%EB%B9%84%EA%B3%BC%EC%84%B8%ED%8E%80%EB%93%9C%3D%3D%2Fwebsquare%2Findex.jsp%3Fw2xPath%3D%2Fwq%2Ffundann%2FDISTaxFreeFund.xml%26divisionId%3DMDIS01007002000000%26serviceId%3DSDIS01007002000%7C%7C%ED%8A%B9%EC%A0%95%EC%9C%A0%ED%98%95%EC%84%A0%ED%83%9D%20%EC%A1%B0%ED%9A%8C%3D%3D%2Fwebsquare%2Findex.jsp%3Fw2xPath%3D%2Fwq%2Ffundann%2FDISFundByType.xml%26divisionId%3DMDIS01007003000000%26serviceId%3DSDIS01007003000%7C%7C%EA%B2%B0%EC%82%B0%20%EB%B0%8F%20%EC%83%81%ED%99%98%3D%3D%2Fwebsquare%2Findex.jsp%3Fw2xPath%3D%2Fwq%2Ffundann%2FDISFundRdmp.xml%26divisionId%3DMDIS01004004000000%26serviceId%3DSDIS01004004000%7C%7C%ED%8E%80%EB%93%9C%EA%B8%B0%EC%A4%80%EA%B0%80%EA%B2%A9%3D%3D%2Fwebsquare%2Findex.jsp%3Fw2xPath%3D%2Fwq%2Ffundann%2FDISFundStdPrice.xml%26divisionId%3DMDIS01004001000000%26serviceId%3DSDIS01004001000%23!%7C%7C%EC%A3%BC%EC%9A%94%EC%A6%9D%EA%B0%90%ED%8E%80%EB%93%9C%3D%3D%2Fwebsquare%2Findex.jsp%3Fw2xPath%3D%2Fwq%2Ffundann%2FDISMainFlucFund.xml%26divisionId%3DMDIS01006002000000%26serviceId%3DSDIS01006002000%7C%7C%ED%8E%80%EB%93%9C%EB%B9%84%EA%B5%90%EA%B2%80%EC%83%89%3D%3D%2Fwebsquare%2Findex.jsp%3Fw2xPath%3D%2Fwq%2Fcmpann%2FDISFundCmpSrch.xml%26divisionId%3DMDIS01008000000000%26serviceId%3DSDIS01008000000%7C%7C%ED%8E%80%EB%93%9C%20%EC%88%98%EC%9D%B5%EB%B9%84%EC%9A%A9%20%EA%B3%84%EC%82%B0%EA%B8%B0%3D%3D%2Fwebsquare%2Findex.jsp%3Fw2xPath%3D%2Fwq%2Ffundcal%2FDISIdvFndSrch.xml%26divisionId%3DMDIS01014000000000%26serviceId%3DSDIS01014000000',
        'Host': 'dis.kofia.or.kr',
        'Origin': 'https://dis.kofia.or.kr',
        'Referer': 'https://dis.kofia.or.kr/websquare/index.jsp?w2xPath=/wq/cmpann/DISPension.xml&divisionId=MDIS01010001000000&serviceId=SDIS01010001000',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36'
    }

    res = requests.post(url, data=xml_str, headers=headers).text

    try:
        pension_df = pd.read_xml(res, xpath='.//selectMeta')
        print(f'data available. {date}')
    except:
        print(f'empty data. {date}')
        continue

    pension_df = pension_df.loc[:, 'tmpV1':'tmpV20']

    pension_df = pension_df.rename(
        columns={'tmpV1':'회사',
                 'tmpV2':'펀드유형',
                 'tmpV3':'상품종류',
                 'tmpV4':'펀드명',
                 'tmpV5':'설정일',
                 'tmpV6':'기준가격(원)',
                 'tmpV7':'설정원본(백만원)',
                 'tmpV8':'순자산(백만원)',
                 'tmpV9':'수익률(%)_Y1',
                 'tmpV10':'수익률(%)_Y2',
                 'tmpV11':'수익률(%)_Y3',
                 'tmpV18':'펀드코드',
                 'tmpV19':'기준일',
                 'tmpV20':'판매사코드'
                }
        )

    pension_df = pension_df.drop(columns=['tmpV12','tmpV13','tmpV14','tmpV15','tmpV16','tmpV17'])

    pension_df.to_csv(f'C:/Users/user/PycharmProjects/pension_data/연금상품데이터/{date}.csv', encoding='utf-8-sig')

    time.sleep(random.randint(3,5))