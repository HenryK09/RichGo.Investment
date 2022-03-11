import matplotlib.pyplot as plt
from matplotlib import rc
from scraper.fund_kr.api.backup import get_fund_name_sr
from scraper.fund_kr.plot.adj_price_compare import show_graphs

rc('font', family='AppleGothic')
plt.rcParams['axes.unicode_minus'] = False

code_list = ['K55207BU0715',
             # 'K55370BU1789',
             # 'K55235BW6898',
             # 'K55307D05118',
             # 'K55213BX5796',
             # 'K55105BV3695',
             # 'K55229BU7300',
             # 'K55101BT7462',
             # 'K55301BV2426',
             # 'K55232BU5747',
             # 'K55370BU1987',
             # 'K55235BO4158',
             # 'K55235BY9403',
             # 'K55102BT6570',
             # 'K55213DA8043',
             # 'K55105D00562',
             # 'K55234CJ0997',
             # 'K55105D17574',
             # 'K55107D40440',
             # 'K55210BU2435',
             # 'K55105BT9928',
             # 'K55301BU6253',
             # 'K55207CP6031',
             'K55101BT7397',
             'K55223BT1450'
             ]

fund_name = ['교보악사파워인덱스증권자투자신탁1호(주식)ClassC-Pe',
             # 'AB미국그로스증권투자신탁(주식-재간접형)종류형Ce-P2',
             # '피델리티글로벌테크놀로지증권자투자신탁(주식-재간접형)종류CP-e',
             # '유리필라델피아반도체인덱스증권자투자신탁H[주식]_Class C-P1e',
             # '한화중국본토증권 자투자신탁 H(주식) 종류C-RPe(퇴직연금)',
             # '삼성누버거버먼차이나증권자투자신탁H[주식-재간접형]_Cpe(퇴직연금)',
             # '이스트스프링차이나드래곤AShare증권자투자신탁(H)[주식]클래스C-P(퇴직연금)E',
             # '한국투자연금베트남그로스증권자투자신탁(주식)(C-Re)',
             # '미래에셋연금인디아업종대표증권자투자신탁1호(주식)종류C-P2e',
             # 'NH-Amundi 국채10년 인덱스 증권자투자신탁[채권]Class C-P2e(퇴직연금)',
             # 'AB글로벌고수익증권투자신탁(채권-재간접형)종류형Ce-P2',
             # '피델리티아시아하이일드증권자투자신탁CP(채권-재간접형)',
             # '피델리티이머징마켓증권자투자신탁CP-e(채권-재간접형)',
             # '하나UBS글로벌리츠부동산투자신탁[재간접형]ClassC-P2E',
             # '한화K리츠플러스부동산 자투자신탁(H)(리츠-재간접형) C-RPe(퇴직연금)',
             # '삼성누버거버먼미국리츠부동산자투자신탁H[REITs-재간접형]_C-Pe',
             # 'IBK 플레인바닐라 EMP 증권투자신탁[혼합-재간접형] 종류C-Re',
             # '삼성글로벌다이나믹자산배분증권자투자신탁H[주식혼합-재간접형]_Cpe(퇴직연금)',
             # '우리다같이TDF2040증권투자신탁(혼합-재간접형)ClassC-Pe',
             # '신한마음편한TDF2040증권투자신탁[주식혼합-재간접형](종류C-re)',
             # '삼성 한국형 TDF 2040 증권투자신탁H[주식혼합-재간접형]_Cpe(퇴직연금)',
             # '미래에셋전략배분TDF2040년혼합자산자투자신탁 종류C-P2e',
             # '교보악사 평생든든TDF 2040증권투자신탁(혼합-재간접형) Class C-Re(퇴직연금)',
             '한국투자TDF알아서2040증권투자신탁(주식혼합-재간접형)(C-Re)',
             'KB 온국민 TDF 2040 증권 투자신탁(주식혼합-재간접형) C-퇴직e']

if __name__ == '__main__':
    test_ticker = 'K55101BT7397'
    test_base_dt = '20220310'

    code_name_sr = get_fund_name_sr(test_base_dt)
    show_graphs(test_ticker, test_base_dt)
