import FundCrawler as fc
import pandas as pd
import requests


def saleComp_list():
    salecomp_df = fc.SaleCompList()
    salecomp_list = salecomp_df['saleCompCd'].tolist()

    return salecomp_list

salecomp_list = saleComp_list()

def saleComp_fund():
    url = 'https://dis.kofia.or.kr/proframeWeb/XMLSERVICES/'

    fund_basket = []
    for salecomp in salecomp_list:

        xml = f"""<?xml version="1.0" encoding="utf-8"?>
        <message>
          <proframeHeader>
            <pfmAppName>FS-DIS2</pfmAppName>
            <pfmSvcName>DISSalEpsRopSO</pfmSvcName>
            <pfmFnName>selectRtn</pfmFnName>
          </proframeHeader>
          <systemHeader></systemHeader>
            <COMDataDynmDTO>
            <standardDt>20211231</standardDt>
            <companyCd>{salecomp}</companyCd>
            <val3></val3>
        </COMDataDynmDTO>
        </message>"""

        headers = {
            'Accept': 'text/xml',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
            'Connection': 'keep-alive',
            'Content-Type': 'text/xml',
            'Cookie': '__smVisitorID=Qhfls34NRgD; userGb=01; JSESSIONID=XCXl8QxAa53rATwpxUhBMxHv33apdk33NxsdjfkCe4ajRULX7ZJaK8m1eQnwQoH6.ap1_servlet_kofiadisEngine; disTdMenu=%ED%8E%80%EB%93%9C%ED%8C%90%EB%A7%A4%ED%9A%8C%EC%82%AC%20%ED%8E%80%EB%93%9C%20%EC%88%98%EC%9D%B5%EB%A5%A0%20%EA%B3%B5%EC%8B%9C%3D%3D%2Fwebsquare%2Findex.jsp%3Fw2xPath%3D%2Fwq%2Ffundann%2FDISFundSalRtn.xml%26divisionId%3DMDIS01013004000000%26serviceId%3DSDIS01013004000%7C%7C%ED%8E%80%EB%93%9C%ED%8C%90%EB%A7%A4%ED%9A%8C%EC%82%AC%20%ED%8E%80%EB%93%9C%20%EA%B8%B0%EC%A4%80%EA%B0%80%EA%B2%A9%EB%93%B1%EB%9D%BD%EB%A5%A0%3D%3D%2Fwebsquare%2Findex.jsp%3Fw2xPath%3D%2Fwq%2Ffundann%2FDISFundSaleStdPrcRate.xml%26divisionId%3DMDIS01013007000000%26serviceId%3DSDIS01013007000%7C%7C%ED%8E%80%EB%93%9C%EA%B8%B0%EC%A4%80%EA%B0%80%EA%B2%A9%3D%3D%2Fwebsquare%2Findex.jsp%3Fw2xPath%3D%2Fwq%2Ffundann%2FDISFundStdPrice.xml%26divisionId%3DMDIS01004001000000%26serviceId%3DSDIS01004001000%23!%7C%7C%ED%8E%80%EB%93%9C%EA%B3%B5%EC%8B%9C%EA%B2%80%EC%83%89%3D%3D%2Fwebsquare%2Findex.jsp%3Fw2xPath%3D%2Fwq%2Ffundann%2FDISFundAnnSrch.xml%26divisionId%3DMDIS01001000000000%26serviceId%3DSDIS01001000000%7C%7C%EC%97%B0%EA%B8%88%EC%83%81%ED%92%88%EA%B3%B5%EC%8B%9C%3D%3D%2Fwebsquare%2Findex.jsp%3Fw2xPath%3D%2Fwq%2Fcmpann%2FDISPension.xml%26divisionId%3DMDIS01010001000000%26serviceId%3DSDIS01010001000%23!%7C%7C%ED%8C%90%EB%A7%A4%EC%82%AC%EB%B3%84%20%ED%8E%80%EB%93%9C%EB%B3%B4%EC%88%98%EB%B9%84%EC%9A%A9%3D%3D%2Fwebsquare%2Findex.jsp%3Fw2xPath%3D%2Fwq%2Ffundann%2FDISSalesCompFeeCMS.xml%26divisionId%3DMDIS01005002000000%26serviceId%3DSDIS01005002000%7C%7C%EA%B8%B0%EC%A4%80%EA%B0%80%EA%B2%A9%EB%93%B1%EB%9D%BD%EB%A5%A0%3D%3D%2Fwebsquare%2Findex.jsp%3Fw2xPath%3D%2Fwq%2Ffundann%2FDISFundStdPrcRate.xml%26divisionId%3DMDIS01004003000000%26serviceId%3DSDIS01004003000%7C%7C%EA%B8%B0%EC%A4%80%EA%B0%80%EA%B2%A9%EB%B3%80%EB%8F%99%EC%B6%94%EC%9D%B4%3D%3D%2Fwebsquare%2Findex.jsp%3Fw2xPath%3D%2Fwq%2Ffundann%2FDISFundStdPrcStut.xml%26divisionId%3DMDIS01004002000000%26serviceId%3DSDIS01004002000%7C%7C%ED%8A%B9%EC%A0%95%EC%9C%A0%ED%98%95%EC%84%A0%ED%83%9D%20%EC%A1%B0%ED%9A%8C%3D%3D%2Fwebsquare%2Findex.jsp%3Fw2xPath%3D%2Fwq%2Ffundann%2FDISFundByType.xml%26divisionId%3DMDIS01007003000000%26serviceId%3DSDIS01007003000%23!%7C%7C%ED%8C%90%EB%A7%A4%EB%B3%B4%EC%88%98%20%EB%B0%8F%20%EC%88%98%EC%88%98%EB%A3%8C%20%EB%B9%84%EA%B5%90%3D%3D%2Fwebsquare%2Findex.jsp%3Fw2xPath%3D%2Fwq%2Ffundann%2FDISCmprFeeCMS.xml%26divisionId%3DMDIS01005003000000%26serviceId%3DSDIS01005003000',
            'Host': 'dis.kofia.or.kr',
            'Origin': 'https://dis.kofia.or.kr',
            'Referer': 'https://dis.kofia.or.kr/websquare/index.jsp?w2xPath=/wq/fundann/DISFundSalRtn.xml&divisionId=MDIS01013004000000&serviceId=SDIS01013004000',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.80 Safari/537.36'
        }

        res = requests.post(url, data=xml, headers=headers).text

        salefund_df = pd.read_xml(res, xpath='.//COMDataDynmDTO')

        salefund_df = salefund_df[['standardCd', 'companyCd', 'val5']].copy()
        salefund_df = salefund_df.dropna()
        salefund_df = salefund_df.rename(columns={'val5': 'product_name'})
        salefund_df = salefund_df.set_index('companyCd')

        fund_basket.append(salefund_df)

        saleComp_fundCd = pd.concat(fund_basket)
        saleCd_df = pd.DataFrame(saleComp_fundCd)

        return saleCd_df

saleCd_df = saleComp_fund()

def to_csv():
    saleCd_df.to_csv('~/dataknows/RichGo.Investment/product_saleComp.csv', encoding='utf-8-sig')