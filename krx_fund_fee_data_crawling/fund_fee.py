import requests
import pandas as pd

url = 'https://dis.kofia.or.kr/proframeWeb/XMLSERVICES/'

xml_str = """<?xml version="1.0" encoding="utf-8"?>
<message>
  <proframeHeader>
    <pfmAppName>FS-DIS2</pfmAppName>
    <pfmSvcName>DISSalesCompFeeCmsSO</pfmSvcName>
    <pfmFnName>select</pfmFnName>
  </proframeHeader>
  <systemHeader></systemHeader>
    <DISCondFuncDTO>
    <tmpV11>A18005</tmpV11>
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

res = requests.post(url, data=xml_str,headers=headers).text

fundFee_df = pd.read_xml(res, xpath='.//selectMeta')

fundFee_df = fundFee_df.loc[:, 'tmpV1':'tmpV18']

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
             'tmpV17':'코드',
             'tmpV18':'운용회사_코드'
             }
)

#fundFee_df.to_csv('C:/Users/user/PycharmProjects/fund_fee_Crawl/판매사별_펀드_보수비용/파주연천축산업협동조합.csv', encoding='cp949')