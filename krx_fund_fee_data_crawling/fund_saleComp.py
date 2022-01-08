import requests
import pandas as pd

url = 'https://dis.kofia.or.kr/proframeWeb/XMLSERVICES/'

xml_str = """<?xml version="1.0" encoding="utf-8"?>
<message>
  <proframeHeader>
    <pfmAppName>FS-DIS2</pfmAppName>
    <pfmSvcName>DISMngCompInqSO</pfmSvcName>
    <pfmFnName>select</pfmFnName>
  </proframeHeader>
  <systemHeader></systemHeader>
    <DISMngCompInqListDTO>
    <option>S2</option>
    <standardDt></standardDt>
</DISMngCompInqListDTO>
</message>"""

headers = {
    'Accept': 'text/xml',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
    'Connection': 'keep-alive',
    'Content-Type': 'text/xml',
    'Cookie': '__smVisitorID=V4ubac3GJYX; JSESSIONID=7d75tg4uC8fd8nxPPiGamBhJedrGP6Lr9Q8OPn1GiWpTOKZap81tnXoUcoGnKFZy.ap2_servlet_kofiadisEngine; userGb=01; disTdMenu=%ED%8C%90%EB%A7%A4%EC%82%AC%EB%B3%84%20%ED%8E%80%EB%93%9C%EB%B3%B4%EC%88%98%EB%B9%84%EC%9A%A9%3D%3D%2Fwebsquare%2Findex.jsp%3Fw2xPath%3D%2Fwq%2Ffundann%2FDISSalesCompFeeCMS.xml%26divisionId%3DMDIS01005002000000%26serviceId%3DSDIS01005002000%7C%7C',
    'Host': 'dis.kofia.or.kr',
    'Origin': 'https://dis.kofia.or.kr',
    'Referer': 'https://dis.kofia.or.kr/websquare/index.jsp?w2xPath=/wq/fundann/DISSalesCompFeeCMS.xml&divisionId=MDIS01005002000000&serviceId=SDIS01005002000',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36'
}
test_str = '''
<list>
<manageCompCd />
<saleCompCd>A02024</saleCompCd>
<cIOrgTypCdList />
<koreanNm>KEB하나은행(구.하나은행)</koreanNm>
</list>
<list>
<manageCompCd />
<saleCompCd>A02014</saleCompCd>
<cIOrgTypCdList />
<koreanNm>NH농협은행</koreanNm>
</list>
<list>
<manageCompCd />
<saleCompCd>A02002</saleCompCd>
<cIOrgTypCdList />
<koreanNm>경남은행</koreanNm>
</list>
<list>
<manageCompCd />
<saleCompCd>A02003</saleCompCd>
<cIOrgTypCdList />
<koreanNm>광주은행</koreanNm>
</list>
<list>
<manageCompCd />
<saleCompCd>A02008</saleCompCd>
<cIOrgTypCdList />
<koreanNm>국민은행</koreanNm>
</list>
<list>
<manageCompCd />
<saleCompCd>A02019</saleCompCd>
<cIOrgTypCdList />
<koreanNm>기업은행</koreanNm>
</list>
<list>
<manageCompCd />
<saleCompCd>A02004</saleCompCd>
<cIOrgTypCdList />
<koreanNm>대구은행</koreanNm>
</list>
<list>
<manageCompCd />
<saleCompCd>A02005</saleCompCd>
<cIOrgTypCdList />
<koreanNm>부산은행</koreanNm>
</list>
<list>
<manageCompCd />
<saleCompCd>A02030</saleCompCd>
<cIOrgTypCdList />
<koreanNm>수협은행</koreanNm>
</list>
<list>
<manageCompCd />
<saleCompCd>A02011</saleCompCd>
<cIOrgTypCdList />
<koreanNm>스탠다드차타드은행</koreanNm>
</list>
<list>
<manageCompCd />
<saleCompCd>A02015</saleCompCd>
<cIOrgTypCdList />
<koreanNm>신한은행</koreanNm>
</list>
<list>
<manageCompCd />
<saleCompCd>A02016</saleCompCd>
<cIOrgTypCdList />
<koreanNm>우리은행</koreanNm>
</list>
<list>
<manageCompCd />
<saleCompCd>A02028</saleCompCd>
<cIOrgTypCdList />
<koreanNm>전북은행</koreanNm>
</list>
<list>
<manageCompCd />
<saleCompCd>A02029</saleCompCd>
<cIOrgTypCdList />
<koreanNm>제주은행</koreanNm>
</list>
<list>
<manageCompCd />
<saleCompCd>A02023</saleCompCd>
<cIOrgTypCdList />
<koreanNm>한국산업은행</koreanNm>
</list>
<list>
<manageCompCd />
<saleCompCd>A02021</saleCompCd>
<cIOrgTypCdList />
<koreanNm>한국씨티은행</koreanNm>
</list>
<list>
<manageCompCd />
<saleCompCd>A02027</saleCompCd>
<cIOrgTypCdList />
<koreanNm>홍콩상하이은행 서울지점</koreanNm>
</list>
<list>
<manageCompCd />
<saleCompCd>A03031</saleCompCd>
<cIOrgTypCdList />
<koreanNm>DB금융투자</koreanNm>
</list>
<list>
<manageCompCd />
<saleCompCd>A03058</saleCompCd>
<cIOrgTypCdList />
<koreanNm>DS투자증권</koreanNm>
</list>
<list>
<manageCompCd />
<saleCompCd>A03024</saleCompCd>
<cIOrgTypCdList />
<koreanNm>KB증권</koreanNm>
</list>
<list>
<manageCompCd />
<saleCompCd>A03016</saleCompCd>
<cIOrgTypCdList />
<koreanNm>NH투자증권</koreanNm>
</list>
<list>
<manageCompCd />
<saleCompCd>A03015</saleCompCd>
<cIOrgTypCdList />
<koreanNm>교보증권</koreanNm>
</list>
<list>
<manageCompCd />
<saleCompCd>A03011</saleCompCd>
<cIOrgTypCdList />
<koreanNm>대신증권</koreanNm>
</list>
<list>
<manageCompCd />
<saleCompCd>A03043</saleCompCd>
<cIOrgTypCdList />
<koreanNm>리딩투자증권</koreanNm>
</list>
<list>
<manageCompCd />
<saleCompCd>A03022</saleCompCd>
<cIOrgTypCdList />
<koreanNm>메리츠증권</koreanNm>
</list>
<list>
<manageCompCd />
<saleCompCd>A03006</saleCompCd>
<cIOrgTypCdList />
<koreanNm>미래에셋증권</koreanNm>
</list>
<list>
<manageCompCd />
<saleCompCd>A03037</saleCompCd>
<cIOrgTypCdList />
<koreanNm>부국증권</koreanNm>
</list>
<list>
<manageCompCd />
<saleCompCd>A03021</saleCompCd>
<cIOrgTypCdList />
<koreanNm>삼성증권</koreanNm>
</list>
<list>
<manageCompCd />
<saleCompCd>A03010</saleCompCd>
<cIOrgTypCdList />
<koreanNm>상상인증권</koreanNm>
</list>
<list>
<manageCompCd />
<saleCompCd>A03019</saleCompCd>
<cIOrgTypCdList />
<koreanNm>신영증권</koreanNm>
</list>
<list>
<manageCompCd />
<saleCompCd>A03004</saleCompCd>
<cIOrgTypCdList />
<koreanNm>신한금융투자</koreanNm>
</list>
<list>
<manageCompCd />
<saleCompCd>A03056</saleCompCd>
<cIOrgTypCdList />
<koreanNm>아이비케이투자증권</koreanNm>
</list>
<list>
<manageCompCd />
<saleCompCd>A03002</saleCompCd>
<cIOrgTypCdList />
<koreanNm>에스케이증권</koreanNm>
</list>
<list>
<manageCompCd />
<saleCompCd>A03003</saleCompCd>
<cIOrgTypCdList />
<koreanNm>유안타증권</koreanNm>
</list>
<list>
<manageCompCd />
<saleCompCd>A03001</saleCompCd>
<cIOrgTypCdList />
<koreanNm>유진투자증권</koreanNm>
</list>
<list>
<manageCompCd />
<saleCompCd>A03005</saleCompCd>
<cIOrgTypCdList />
<koreanNm>유화증권</koreanNm>
</list>
<list>
<manageCompCd />
<saleCompCd>A03045</saleCompCd>
<cIOrgTypCdList />
<koreanNm>이베스트투자증권</koreanNm>
</list>
<list>
<manageCompCd />
<saleCompCd>A03061</saleCompCd>
<cIOrgTypCdList />
<koreanNm>카카오페이증권</koreanNm>
</list>
<list>
<manageCompCd />
<saleCompCd>A03060</saleCompCd>
<cIOrgTypCdList />
<koreanNm>케이티비투자증권</koreanNm>
</list>
<list>
<manageCompCd />
<saleCompCd>A03057</saleCompCd>
<cIOrgTypCdList />
<koreanNm>케이프투자증권</koreanNm>
</list>
<list>
<manageCompCd />
<saleCompCd>A03050</saleCompCd>
<cIOrgTypCdList />
<koreanNm>코리아에셋투자증권</koreanNm>
</list>
<list>
<manageCompCd />
<saleCompCd>A03044</saleCompCd>
<cIOrgTypCdList />
<koreanNm>키움증권</koreanNm>
</list>
<list>
<manageCompCd />
<saleCompCd>A03041</saleCompCd>
<cIOrgTypCdList />
<koreanNm>하나금융투자</koreanNm>
</list>
<list>
<manageCompCd />
<saleCompCd>A03034</saleCompCd>
<cIOrgTypCdList />
<koreanNm>하이투자증권</koreanNm>
</list>
<list>
<manageCompCd />
<saleCompCd>A03040</saleCompCd>
<cIOrgTypCdList />
<koreanNm>한국투자증권</koreanNm>
</list>
<list>
<manageCompCd />
<saleCompCd>A03126</saleCompCd>
<cIOrgTypCdList />
<koreanNm>한국포스증권</koreanNm>
</list>
<list>
<manageCompCd />
<saleCompCd>A03018</saleCompCd>
<cIOrgTypCdList />
<koreanNm>한양증권</koreanNm>
</list>
<list>
<manageCompCd />
<saleCompCd>A03025</saleCompCd>
<cIOrgTypCdList />
<koreanNm>한화투자증권</koreanNm>
</list>
<list>
<manageCompCd />
<saleCompCd>A03029</saleCompCd>
<cIOrgTypCdList />
<koreanNm>현대차증권주식회사</koreanNm>
</list>
<list>
<manageCompCd />
<saleCompCd>A03052</saleCompCd>
<cIOrgTypCdList />
<koreanNm>흥국증권</koreanNm>
</list>
<list>
<manageCompCd />
<saleCompCd>A04024</saleCompCd>
<cIOrgTypCdList />
<koreanNm>KB손해보험(구. LIG손해보험)</koreanNm>
</list>
<list>
<manageCompCd />
<saleCompCd>A04013</saleCompCd>
<cIOrgTypCdList />
<koreanNm>KDB생명보험</koreanNm>
</list>
<list>
<manageCompCd />
<saleCompCd>A04001</saleCompCd>
<cIOrgTypCdList />
<koreanNm>교보생명보험</koreanNm>
</list>
<list>
<manageCompCd />
<saleCompCd>A04014</saleCompCd>
<cIOrgTypCdList />
<koreanNm>미래에셋생명보험</koreanNm>
</list>
<list>
<manageCompCd />
<saleCompCd>A04003</saleCompCd>
<cIOrgTypCdList />
<koreanNm>삼성생명보험</koreanNm>
</list>
<list>
<manageCompCd />
<saleCompCd>A04019</saleCompCd>
<cIOrgTypCdList />
<koreanNm>삼성화재보험</koreanNm>
</list>
<list>
<manageCompCd />
<saleCompCd>A04016</saleCompCd>
<cIOrgTypCdList />
<koreanNm>신한라이프생명보험(주)</koreanNm>
</list>
<list>
<manageCompCd />
<saleCompCd>A04002</saleCompCd>
<cIOrgTypCdList />
<koreanNm>한화생명보험</koreanNm>
</list>
<list>
<manageCompCd />
<saleCompCd>A04021</saleCompCd>
<cIOrgTypCdList />
<koreanNm>현대해상화재보험</koreanNm>
</list>
<list>
<manageCompCd />
<saleCompCd>A18030</saleCompCd>
<cIOrgTypCdList />
<koreanNm>가산농업협동조합</koreanNm>
</list>
<list>
<manageCompCd />
<saleCompCd>A18025</saleCompCd>
<cIOrgTypCdList />
<koreanNm>강동농업협동조합</koreanNm>
</list>
<list>
<manageCompCd />
<saleCompCd>A18034</saleCompCd>
<cIOrgTypCdList />
<koreanNm>강릉농업협동조합</koreanNm>
</list>
<list>
<manageCompCd />
<saleCompCd>A18026</saleCompCd>
<cIOrgTypCdList />
<koreanNm>경기 도드람양돈농업협동조합</koreanNm>
</list>
<list>
<manageCompCd />
<saleCompCd>A18007</saleCompCd>
<cIOrgTypCdList />
<koreanNm>관악농업협동조합</koreanNm>
</list>
<list>
<manageCompCd />
<saleCompCd>A18012</saleCompCd>
<cIOrgTypCdList />
<koreanNm>광주비아농업협동조합</koreanNm>
</list>
<list>
<manageCompCd />
<saleCompCd>A01015</saleCompCd>
<cIOrgTypCdList />
<koreanNm>교보악사자산운용</koreanNm>
</list>
<list>
<manageCompCd />
<saleCompCd>A01339</saleCompCd>
<cIOrgTypCdList />
<koreanNm>구도자산운용</koreanNm>
</list>
<list>
<manageCompCd />
<saleCompCd>A18031</saleCompCd>
<cIOrgTypCdList />
<koreanNm>김해축산업협동조합</koreanNm>
</list>
<list>
<manageCompCd />
<saleCompCd>A18008</saleCompCd>
<cIOrgTypCdList />
<koreanNm>남동농업협동조합</koreanNm>
</list>
<list>
<manageCompCd />
<saleCompCd>A18020</saleCompCd>
<cIOrgTypCdList />
<koreanNm>남서울농업협동조합</koreanNm>
</list>
<list>
<manageCompCd />
<saleCompCd>A18009</saleCompCd>
<cIOrgTypCdList />
<koreanNm>남인천농업협동조합</koreanNm>
</list>
<list>
<manageCompCd />
<saleCompCd>A01293</saleCompCd>
<cIOrgTypCdList />
<koreanNm>누림자산운용</koreanNm>
</list>
<list>
<manageCompCd />
<saleCompCd>A18002</saleCompCd>
<cIOrgTypCdList />
<koreanNm>대구축산업협동조합</koreanNm>
</list>
<list>
<manageCompCd />
<saleCompCd>A01011</saleCompCd>
<cIOrgTypCdList />
<koreanNm>대신자산운용</koreanNm>
</list>
<list>
<manageCompCd />
<saleCompCd>A18029</saleCompCd>
<cIOrgTypCdList />
<koreanNm>동창원농업협동조합</koreanNm>
</list>
<list>
<manageCompCd />
<saleCompCd>A01024</saleCompCd>
<cIOrgTypCdList />
<koreanNm>디비자산운용</koreanNm>
</list>
<list>
<manageCompCd />
<saleCompCd>A01187</saleCompCd>
<cIOrgTypCdList />
<koreanNm>르네상스자산운용</koreanNm>
</list>
<list>
<manageCompCd />
<saleCompCd>A01230</saleCompCd>
<cIOrgTypCdList />
<koreanNm>마스턴투자운용</koreanNm>
</list>
<list>
<manageCompCd />
<saleCompCd>A01050</saleCompCd>
<cIOrgTypCdList />
<koreanNm>마이다스에셋자산운용</koreanNm>
</list>
<list>
<manageCompCd />
<saleCompCd>A01065</saleCompCd>
<cIOrgTypCdList />
<koreanNm>맥쿼리자산운용</koreanNm>
</list>
<list>
<manageCompCd />
<saleCompCd>A01013</saleCompCd>
<cIOrgTypCdList />
<koreanNm>멀티에셋자산운용</koreanNm>
</list>
<list>
<manageCompCd />
<saleCompCd>A01069</saleCompCd>
<cIOrgTypCdList />
<koreanNm>메리츠자산운용</koreanNm>
</list>
<list>
<manageCompCd />
<saleCompCd>A01358</saleCompCd>
<cIOrgTypCdList />
<koreanNm>메자닌플러스자산운용</koreanNm>
</list>
<list>
<manageCompCd />
<saleCompCd>A01048</saleCompCd>
<cIOrgTypCdList />
<koreanNm>미래에셋자산운용</koreanNm>
</list>
<list>
<manageCompCd />
<saleCompCd>A18035</saleCompCd>
<cIOrgTypCdList />
<koreanNm>반월농업협동조합</koreanNm>
</list>
<list>
<manageCompCd />
<saleCompCd>A01049</saleCompCd>
<cIOrgTypCdList />
<koreanNm>베어링자산운용</koreanNm>
</list>
<list>
<manageCompCd />
<saleCompCd>A18013</saleCompCd>
<cIOrgTypCdList />
<koreanNm>부경양돈농업협동조합</koreanNm>
</list>
<list>
<manageCompCd />
<saleCompCd>A18022</saleCompCd>
<cIOrgTypCdList />
<koreanNm>부평농업협동조합</koreanNm>
</list>
<list>
<manageCompCd />
<saleCompCd>A18001</saleCompCd>
<cIOrgTypCdList />
<koreanNm>북서울농업협동조합</koreanNm>
</list>
<list>
<manageCompCd />
<saleCompCd>A01004</saleCompCd>
<cIOrgTypCdList />
<koreanNm>브이아이자산운용</koreanNm>
</list>
<list>
<manageCompCd />
<saleCompCd>A01075</saleCompCd>
<cIOrgTypCdList />
<koreanNm>비엔케이자산운용</koreanNm>
</list>
<list>
<manageCompCd />
<saleCompCd>A05004</saleCompCd>
<cIOrgTypCdList />
<koreanNm>비엔케이투자증권</koreanNm>
</list>
<list>
<manageCompCd />
<saleCompCd>A01157</saleCompCd>
<cIOrgTypCdList />
<koreanNm>비욘드자산운용</koreanNm>
</list>
<list>
<manageCompCd />
<saleCompCd>E04004</saleCompCd>
<cIOrgTypCdList />
<koreanNm>비지시캐피탈마켓외국환중개</koreanNm>
</list>
<list>
<manageCompCd />
<saleCompCd>A01115</saleCompCd>
<cIOrgTypCdList />
<koreanNm>삼성에스알에이자산운용</koreanNm>
</list>
<list>
<manageCompCd />
<saleCompCd>A01005</saleCompCd>
<cIOrgTypCdList />
<koreanNm>삼성자산운용</koreanNm>
</list>
<list>
<manageCompCd />
<saleCompCd>A18014</saleCompCd>
<cIOrgTypCdList />
<koreanNm>서대전농업협동조합</koreanNm>
</list>
<list>
<manageCompCd />
<saleCompCd>A18015</saleCompCd>
<cIOrgTypCdList />
<koreanNm>서부농업협동조합</koreanNm>
</list>
<list>
<manageCompCd />
<saleCompCd>A18016</saleCompCd>
<cIOrgTypCdList />
<koreanNm>서울경기양돈농업협동조합</koreanNm>
</list>
<list>
<manageCompCd />
<saleCompCd>A18010</saleCompCd>
<cIOrgTypCdList />
<koreanNm>송파농업협동조합</koreanNm>
</list>
<list>
<manageCompCd />
<saleCompCd>A18003</saleCompCd>
<cIOrgTypCdList />
<koreanNm>순천농업협동조합</koreanNm>
</list>
<list>
<manageCompCd />
<saleCompCd>A01017</saleCompCd>
<cIOrgTypCdList />
<koreanNm>신영자산운용</koreanNm>
</list>
<list>
<manageCompCd />
<saleCompCd>A01018</saleCompCd>
<cIOrgTypCdList />
<koreanNm>신한자산운용</koreanNm>
</list>
<list>
<manageCompCd />
<saleCompCd>A01163</saleCompCd>
<cIOrgTypCdList />
<koreanNm>씨스퀘어자산운용</koreanNm>
</list>
<list>
<manageCompCd />
<saleCompCd>A01061</saleCompCd>
<cIOrgTypCdList />
<koreanNm>알파자산운용</koreanNm>
</list>
<list>
<manageCompCd />
<saleCompCd>A01168</saleCompCd>
<cIOrgTypCdList />
<koreanNm>알펜루트자산운용</koreanNm>
</list>
<list>
<manageCompCd />
<saleCompCd>A18011</saleCompCd>
<cIOrgTypCdList />
<koreanNm>양주축산업협동조합</koreanNm>
</list>
<list>
<manageCompCd />
<saleCompCd>A01303</saleCompCd>
<cIOrgTypCdList />
<koreanNm>얼터너티브자산운용</koreanNm>
</list>
<list>
<manageCompCd />
<saleCompCd>A01067</saleCompCd>
<cIOrgTypCdList />
<koreanNm>에셋플러스자산운용</koreanNm>
</list>
<list>
<manageCompCd />
<saleCompCd>A01121</saleCompCd>
<cIOrgTypCdList />
<koreanNm>에이디에프자산운용</koreanNm>
</list>
<list>
<manageCompCd />
<saleCompCd>A01034</saleCompCd>
<cIOrgTypCdList />
<koreanNm>에이치디씨자산운용</koreanNm>
</list>
<list>
<manageCompCd />
<saleCompCd>A05003</saleCompCd>
<cIOrgTypCdList />
<koreanNm>엔에이치선물</koreanNm>
</list>
<list>
<manageCompCd />
<saleCompCd>A01040</saleCompCd>
<cIOrgTypCdList />
<koreanNm>엔에이치아문디자산운용</koreanNm>
</list>
<list>
<manageCompCd />
<saleCompCd>A18024</saleCompCd>
<cIOrgTypCdList />
<koreanNm>여수농업협동조합</koreanNm>
</list>
<list>
<manageCompCd />
<saleCompCd>A18032</saleCompCd>
<cIOrgTypCdList />
<koreanNm>여천농업협동조합</koreanNm>
</list>
<list>
<manageCompCd />
<saleCompCd>A18017</saleCompCd>
<cIOrgTypCdList />
<koreanNm>영등포농업협동조합</koreanNm>
</list>
<list>
<manageCompCd />
<saleCompCd>A01366</saleCompCd>
<cIOrgTypCdList />
<koreanNm>와이드크릭자산운용</koreanNm>
</list>
<list>
<manageCompCd />
<saleCompCd>A01007</saleCompCd>
<cIOrgTypCdList />
<koreanNm>우리자산운용</koreanNm>
</list>
<list>
<manageCompCd />
<saleCompCd>A06020</saleCompCd>
<cIOrgTypCdList />
<koreanNm>우리종합금융</koreanNm>
</list>
<list>
<manageCompCd />
<saleCompCd>D04001</saleCompCd>
<cIOrgTypCdList />
<koreanNm>우정사업본부</koreanNm>
</list>
<list>
<manageCompCd />
<saleCompCd>A01054</saleCompCd>
<cIOrgTypCdList />
<koreanNm>유리자산운용</koreanNm>
</list>
<list>
<manageCompCd />
<saleCompCd>A18023</saleCompCd>
<cIOrgTypCdList />
<koreanNm>유성농업협동조합</koreanNm>
</list>
<list>
<manageCompCd />
<saleCompCd>A01092</saleCompCd>
<cIOrgTypCdList />
<koreanNm>이지스자산운용</koreanNm>
</list>
<list>
<manageCompCd />
<saleCompCd>A01336</saleCompCd>
<cIOrgTypCdList />
<koreanNm>이현자산운용</koreanNm>
</list>
<list>
<manageCompCd />
<saleCompCd>A01142</saleCompCd>
<cIOrgTypCdList />
<koreanNm>인마크자산운용</koreanNm>
</list>
<list>
<manageCompCd />
<saleCompCd>A18036</saleCompCd>
<cIOrgTypCdList />
<koreanNm>인천원예농업협동조합</koreanNm>
</list>
<list>
<manageCompCd />
<saleCompCd>A01241</saleCompCd>
<cIOrgTypCdList />
<koreanNm>인트러스투자운용</koreanNm>
</list>
<list>
<manageCompCd />
<saleCompCd>A18021</saleCompCd>
<cIOrgTypCdList />
<koreanNm>일산농업협동조합</koreanNm>
</list>
<list>
<manageCompCd />
<saleCompCd>A18033</saleCompCd>
<cIOrgTypCdList />
<koreanNm>장유농업협동조합</koreanNm>
</list>
<list>
<manageCompCd />
<saleCompCd>A18028</saleCompCd>
<cIOrgTypCdList />
<koreanNm>정읍농업협동조합</koreanNm>
</list>
<list>
<manageCompCd />
<saleCompCd>A07008</saleCompCd>
<cIOrgTypCdList />
<koreanNm>제너시스투자자문</koreanNm>
</list>
<list>
<manageCompCd />
<saleCompCd>A18019</saleCompCd>
<cIOrgTypCdList />
<koreanNm>중앙농업협동조합</koreanNm>
</list>
<list>
<manageCompCd />
<saleCompCd>A01357</saleCompCd>
<cIOrgTypCdList />
<koreanNm>지베스코자산운용</koreanNm>
</list>
<list>
<manageCompCd />
<saleCompCd>A18037</saleCompCd>
<cIOrgTypCdList />
<koreanNm>진해농업협동조합</koreanNm>
</list>
<list>
<manageCompCd />
<saleCompCd>A18004</saleCompCd>
<cIOrgTypCdList />
<koreanNm>천안농업협동조합</koreanNm>
</list>
<list>
<manageCompCd />
<saleCompCd>A18018</saleCompCd>
<cIOrgTypCdList />
<koreanNm>청주농업협동조합</koreanNm>
</list>
<list>
<manageCompCd />
<saleCompCd>A18027</saleCompCd>
<cIOrgTypCdList />
<koreanNm>청주축산농업협동조합</koreanNm>
</list>
<list>
<manageCompCd />
<saleCompCd>A01041</saleCompCd>
<cIOrgTypCdList />
<koreanNm>칸서스자산운용</koreanNm>
</list>
<list>
<manageCompCd />
<saleCompCd>A01093</saleCompCd>
<cIOrgTypCdList />
<koreanNm>캡스톤자산운용</koreanNm>
</list>
<list>
<manageCompCd />
<saleCompCd>A01031</saleCompCd>
<cIOrgTypCdList />
<koreanNm>케이비자산운용</koreanNm>
</list>
<list>
<manageCompCd />
<saleCompCd>A01170</saleCompCd>
<cIOrgTypCdList />
<koreanNm>케이클라비스자산운용</koreanNm>
</list>
<list>
<manageCompCd />
<saleCompCd>A01053</saleCompCd>
<cIOrgTypCdList />
<koreanNm>케이티비자산운용</koreanNm>
</list>
<list>
<manageCompCd />
<saleCompCd>A01057</saleCompCd>
<cIOrgTypCdList />
<koreanNm>코레이트자산운용</koreanNm>
</list>
<list>
<manageCompCd />
<saleCompCd>A01120</saleCompCd>
<cIOrgTypCdList />
<koreanNm>쿼드자산운용</koreanNm>
</list>
<list>
<manageCompCd />
<saleCompCd>A01014</saleCompCd>
<cIOrgTypCdList />
<koreanNm>키움투자자산운용</koreanNm>
</list>
<list>
<manageCompCd />
<saleCompCd>A01158</saleCompCd>
<cIOrgTypCdList />
<koreanNm>타임폴리오자산운용</koreanNm>
</list>
<list>
<manageCompCd />
<saleCompCd>A01068</saleCompCd>
<cIOrgTypCdList />
<koreanNm>트러스톤자산운용</koreanNm>
</list>
<list>
<manageCompCd />
<saleCompCd>A01164</saleCompCd>
<cIOrgTypCdList />
<koreanNm>트리니티자산운용</koreanNm>
</list>
<list>
<manageCompCd />
<saleCompCd>A01188</saleCompCd>
<cIOrgTypCdList />
<koreanNm>파레토자산운용</koreanNm>
</list>
<list>
<manageCompCd />
<saleCompCd>A18005</saleCompCd>
<cIOrgTypCdList />
<koreanNm>파주연천축산업협동조합</koreanNm>
</list>
<list>
<manageCompCd />
<saleCompCd>A01183</saleCompCd>
<cIOrgTypCdList />
<koreanNm>퍼시픽자산운용</koreanNm>
</list>
<list>
<manageCompCd />
<saleCompCd>A01131</saleCompCd>
<cIOrgTypCdList />
<koreanNm>피데스자산운용</koreanNm>
</list>
<list>
<manageCompCd />
<saleCompCd>A01062</saleCompCd>
<cIOrgTypCdList />
<koreanNm>하나대체투자자산운용</koreanNm>
</list>
<list>
<manageCompCd />
<saleCompCd>A01002</saleCompCd>
<cIOrgTypCdList />
<koreanNm>하나유비에스자산운용</koreanNm>
</list>
<list>
<manageCompCd />
<saleCompCd>A01072</saleCompCd>
<cIOrgTypCdList />
<koreanNm>하이자산운용</koreanNm>
</list>
<list>
<manageCompCd />
<saleCompCd>A01127</saleCompCd>
<cIOrgTypCdList />
<koreanNm>한국교통자산운용</koreanNm>
</list>
<list>
<manageCompCd />
<saleCompCd>A01001</saleCompCd>
<cIOrgTypCdList />
<koreanNm>한국투자신탁운용</koreanNm>
</list>
<list>
<manageCompCd />
<saleCompCd>A01021</saleCompCd>
<cIOrgTypCdList />
<koreanNm>한화자산운용</koreanNm>
</list>
<list>
<manageCompCd />
<saleCompCd>A01290</saleCompCd>
<cIOrgTypCdList />
<koreanNm>헤리티지자산운용</koreanNm>
</list>
<list>
<manageCompCd />
<saleCompCd>A01082</saleCompCd>
<cIOrgTypCdList />
<koreanNm>현대자산운용</koreanNm>
</list>
<list>
<manageCompCd />
<saleCompCd>A01032</saleCompCd>
<cIOrgTypCdList />
<koreanNm>흥국자산운용</koreanNm>
</list>
'''

res = requests.post(url, data=xml_str,headers=headers).text

saleComp_df = pd.read_xml(res, xpath='.//list')

saleComp_df = saleComp_df[['saleCompCd','koreanNm']]
saleComp_df = saleComp_df.sort_values(by='saleCompCd', ascending=True)
saleComp_df = saleComp_df.rename(columns={'saleComCd':'판매회사_코드','koreanNM':'판매회사'})






