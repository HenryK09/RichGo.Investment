import requests
import pandas as pd
import time
import random

saleComp_df = pd.read_csv('C:/Users/user/PycharmProjects/fund_fee_Crawl/펀드판매회사.csv', encoding='cp949')

url = 'https://dis.kofia.or.kr/proframeWeb/XMLSERVICES/'

for code, comp_name in saleComp_df.set_index('saleCompCd')['koreanNm'].items():

    xml_str = f"""<?xml version="1.0" encoding="utf-8"?>
    <message>
      <proframeHeader>
        <pfmAppName>FS-DIS2</pfmAppName>
        <pfmSvcName>DISSalesCompFeeCmsSO</pfmSvcName>
        <pfmFnName>select</pfmFnName>
      </proframeHeader>
      <systemHeader></systemHeader>
        <DISCondFuncDTO>
        <tmpV11>{code}</tmpV11>
        <tmpV30>20211130</tmpV30>
        <tmpV12></tmpV12>
        <tmpV3></tmpV3>
        <tmpV5></tmpV5>
        <tmpV4></tmpV4>
    </DISCondFuncDTO>
    </message>"""

    headers = {
        'Accept': 'text/xml',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
        'Connection': 'keep-alive',
        'Content-Type': 'text/xml',
        'Cookie': '__smVisitorID=V4ubac3GJYX; userGb=01; disTdMenu=%ED%8C%90%EB%A7%A4%EC%82%AC%EB%B3%84%20%ED%8E%80%EB%93%9C%EB%B3%B4%EC%88%98%EB%B9%84%EC%9A%A9%3D%3D%2Fwebsquare%2Findex.jsp%3Fw2xPath%3D%2Fwq%2Ffundann%2FDISSalesCompFeeCMS.xml%26divisionId%3DMDIS01005002000000%26serviceId%3DSDIS01005002000%7C%7C',
        'Host': 'dis.kofia.or.kr',
        'Origin': 'https://dis.kofia.or.kr',
        'Referer': 'https://dis.kofia.or.kr/websquare/index.jsp?w2xPath=/wq/fundann/DISSalesCompFeeCMS.xml&divisionId=MDIS01005002000000&serviceId=SDIS01005002000',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36'
    }

    # 웹에서 xml 데이터 request
    res = requests.post(url, data=xml_str,headers=headers).text
    # xml 파일에서 특정 부분 읽어오기
    try:
        fundFee_df = pd.read_xml(res, xpath='.//selectMeta')
    except: # 판매회사에 판매중인 펀드가 없어 데이터가 비어 있을 경우 에러 발생
        print(f'empty data. {code}/{comp_name}')
        continue
    # 필요한 컬럼 범위 추출
    fundFee_df = fundFee_df.loc[:, 'tmpV1':'tmpV18']
    # column 이름 변경
    fundFee_df = fundFee_df.rename(
        columns={'tmpV1':'운용회사',
                 'tmpV2':'펀드명',
                 'tmpV3':'펀드유형',
                 'tmpV4':'설정일',
                 'tmpV5':'보수율(운용)',
                 'tmpV6':'보수율(판매)',
                 'tmpV7':'보수율(수탁)',
                 'tmpV8':'보수율(사무관리)',
                 'tmpV9':'보수율(합계(A))',
                 'tmpV10':'보수율(유사유형_평균보수율)',
                 'tmpV11':'기타비용(B)',
                 'tmpV12':'TER(A+B)',
                 'tmpV13':'판매수수료(C)_선취',
                 'tmpV14':'판매수수료(C)_후취',
                 'tmpV15':'매매_중개수수료율(D)',
                 'tmpV16':'기준일',
                 'tmpV17':'표준코드',
                 'tmpV18':'운용회사_코드'
                 }
    )

    fundFee_df.to_csv('C:/Users/user/PycharmProjects/fund_fee_Crawl/판매사별_펀드_보수비용/{}.csv'.format(comp_name), encoding='cp949')
    print(f'saved. {code}/{comp_name}')

    time.sleep(random.randint(1,3))