import pandas as pd
import numpy as np
import requests


url = 'https://dis.kofia.or.kr/proframeWeb/XMLSERVICES/'

fund_group = []
for page in range(1, 6720):
    xml = f"""<?xml version="1.0" encoding="utf-8"?>
    <message>
      <proframeHeader>
        <pfmAppName>FS-DIS2</pfmAppName>
        <pfmSvcName>DISIntSrchSO</pfmSvcName>
        <pfmFnName>selectFndList</pfmFnName>
      </proframeHeader>
      <systemHeader></systemHeader>
        <DISFndIntSrchDTO>
        <uRefundRsnGbNm></uRefundRsnGbNm>
        <managementGb></managementGb>
        <fundNm></fundNm>
        <pageCnt>{page}</pageCnt>
    </DISFndIntSrchDTO>
    </message>"""

    headers = {
        'Accept': 'text/xml',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.9',
        'Connection': 'keep-alive',
        'Content-Type': 'text/xml',
        'Cookie': '__smVisitorID=Qhfls34NRgD; userGb=01; disTdMenu=%ED%8E%80%EB%93%9C%EA%B8%B0%EC%A4%80%EA%B0%80%EA%B2%A9%3D%3D%2Fwebsquare%2Findex.jsp%3Fw2xPath%3D%2Fwq%2Ffundann%2FDISFundStdPrice.xml%26divisionId%3DMDIS01004001000000%26serviceId%3DSDIS01004001000%7C%7C%ED%8E%80%EB%93%9C%EA%B3%B5%EC%8B%9C%EA%B2%80%EC%83%89%3D%3D%2Fwebsquare%2Findex.jsp%3Fw2xPath%3D%2Fwq%2Ffundann%2FDISFundAnnSrch.xml%26divisionId%3DMDIS01001000000000%26serviceId%3DSDIS01001000000%7C%7C%ED%8E%80%EB%93%9C%ED%8C%90%EB%A7%A4%ED%9A%8C%EC%82%AC%20%ED%8E%80%EB%93%9C%20%EC%88%98%EC%9D%B5%EB%A5%A0%20%EA%B3%B5%EC%8B%9C%3D%3D%2Fwebsquare%2Findex.jsp%3Fw2xPath%3D%2Fwq%2Ffundann%2FDISFundSalRtn.xml%26divisionId%3DMDIS01013004000000%26serviceId%3DSDIS01013004000%7C%7C%ED%8E%80%EB%93%9C%ED%8C%90%EB%A7%A4%ED%9A%8C%EC%82%AC%20%ED%8E%80%EB%93%9C%20%EA%B8%B0%EC%A4%80%EA%B0%80%EA%B2%A9%EB%93%B1%EB%9D%BD%EB%A5%A0%3D%3D%2Fwebsquare%2Findex.jsp%3Fw2xPath%3D%2Fwq%2Ffundann%2FDISFundSaleStdPrcRate.xml%26divisionId%3DMDIS01013007000000%26serviceId%3DSDIS01013007000%7C%7C%EC%97%B0%EA%B8%88%EC%83%81%ED%92%88%EA%B3%B5%EC%8B%9C%3D%3D%2Fwebsquare%2Findex.jsp%3Fw2xPath%3D%2Fwq%2Fcmpann%2FDISPension.xml%26divisionId%3DMDIS01010001000000%26serviceId%3DSDIS01010001000%23!%7C%7C%ED%8C%90%EB%A7%A4%EC%82%AC%EB%B3%84%20%ED%8E%80%EB%93%9C%EB%B3%B4%EC%88%98%EB%B9%84%EC%9A%A9%3D%3D%2Fwebsquare%2Findex.jsp%3Fw2xPath%3D%2Fwq%2Ffundann%2FDISSalesCompFeeCMS.xml%26divisionId%3DMDIS01005002000000%26serviceId%3DSDIS01005002000%7C%7C%EA%B8%B0%EC%A4%80%EA%B0%80%EA%B2%A9%EB%93%B1%EB%9D%BD%EB%A5%A0%3D%3D%2Fwebsquare%2Findex.jsp%3Fw2xPath%3D%2Fwq%2Ffundann%2FDISFundStdPrcRate.xml%26divisionId%3DMDIS01004003000000%26serviceId%3DSDIS01004003000%7C%7C%EA%B8%B0%EC%A4%80%EA%B0%80%EA%B2%A9%EB%B3%80%EB%8F%99%EC%B6%94%EC%9D%B4%3D%3D%2Fwebsquare%2Findex.jsp%3Fw2xPath%3D%2Fwq%2Ffundann%2FDISFundStdPrcStut.xml%26divisionId%3DMDIS01004002000000%26serviceId%3DSDIS01004002000%7C%7C%ED%8A%B9%EC%A0%95%EC%9C%A0%ED%98%95%EC%84%A0%ED%83%9D%20%EC%A1%B0%ED%9A%8C%3D%3D%2Fwebsquare%2Findex.jsp%3Fw2xPath%3D%2Fwq%2Ffundann%2FDISFundByType.xml%26divisionId%3DMDIS01007003000000%26serviceId%3DSDIS01007003000%23!%7C%7C%ED%8C%90%EB%A7%A4%EB%B3%B4%EC%88%98%20%EB%B0%8F%20%EC%88%98%EC%88%98%EB%A3%8C%20%EB%B9%84%EA%B5%90%3D%3D%2Fwebsquare%2Findex.jsp%3Fw2xPath%3D%2Fwq%2Ffundann%2FDISCmprFeeCMS.xml%26divisionId%3DMDIS01005003000000%26serviceId%3DSDIS01005003000; JSESSIONID=EiwVItt1RXBaPkwwsKgg4ZoxoTaXoJfbegN4VAGy1AbWDaDb7wpHxTnKfE6dzODY.ap2_servlet_kofiadisEngine',
        'Host': 'dis.kofia.or.kr',
        'Origin': 'https://dis.kofia.or.kr',
        'Referer': 'https://dis.kofia.or.kr/websquare/webSquare.jsp?w2xPath=/wq/fundMgr/DISFundMgrFundWebSrch.xml',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.80 Safari/537.36}'
    }

    res = requests.post(url, data=xml, headers=headers).text

    totalCd = pd.read_xml(res, xpath='.//list')

    fund_group.append(totalCd)
    attachedCd = pd.concat(fund_group)
    totalCd_df = pd.DataFrame(attachedCd)
    if page == 2:
        break
kkk=0