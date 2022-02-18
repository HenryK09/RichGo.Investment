import pandas as pd
import numpy as np
import datetime as dt
import FundCrawler as fc
import matplotlib.pyplot as plt
from matplotlib import rc
rc('font', family='AppleGothic')
plt.rcParams['axes.unicode_minus'] = False


code_list = ['K55207BU0715',
             'K55370BU1789',
             'K55235BW6898',
             'K55307D05118',
             'K55213BX5796',
             'K55105BV3695',
             'K55229BU7300',
             'K55101BT7462',
             'K55301BV2426',
             'K55232BU5747',
             'K55370BU1987',
             'K55235BO4158',
             'K55235BY9403',
             'K55102BT6570',
             'K55213DA8043',
             'K55105D00562',
             'K55234CJ0997',
             'K55105D17574',
             'K55107D40440',
             'K55210BU2435',
             'K55105BT9928',
             'K55301BU6253',
             'K55207CP6031',
             'K55101BT7397',
             'K55223BT1450'
             ]

fund_name = ['교보악사파워인덱스증권자투자신탁1호(주식)ClassC-Pe',
             'AB미국그로스증권투자신탁(주식-재간접형)종류형Ce-P2',
             '피델리티글로벌테크놀로지증권자투자신탁(주식-재간접형)종류CP-e',
             '유리필라델피아반도체인덱스증권자투자신탁H[주식]_Class C-P1e',
             '한화중국본토증권 자투자신탁 H(주식) 종류C-RPe(퇴직연금)',
             '삼성누버거버먼차이나증권자투자신탁H[주식-재간접형]_Cpe(퇴직연금)',
             '이스트스프링차이나드래곤AShare증권자투자신탁(H)[주식]클래스C-P(퇴직연금)E',
             '한국투자연금베트남그로스증권자투자신탁(주식)(C-Re)',
             '미래에셋연금인디아업종대표증권자투자신탁1호(주식)종류C-P2e',
             'NH-Amundi 국채10년 인덱스 증권자투자신탁[채권]Class C-P2e(퇴직연금)',
             'AB글로벌고수익증권투자신탁(채권-재간접형)종류형Ce-P2',
             '피델리티아시아하이일드증권자투자신탁CP(채권-재간접형)',
             '피델리티이머징마켓증권자투자신탁CP-e(채권-재간접형)',
             '하나UBS글로벌리츠부동산투자신탁[재간접형]ClassC-P2E',
             '한화K리츠플러스부동산 자투자신탁(H)(리츠-재간접형) C-RPe(퇴직연금)',
             '삼성누버거버먼미국리츠부동산자투자신탁H[REITs-재간접형]_C-Pe',
             'IBK 플레인바닐라 EMP 증권투자신탁[혼합-재간접형] 종류C-Re',
             '삼성글로벌다이나믹자산배분증권자투자신탁H[주식혼합-재간접형]_Cpe(퇴직연금)',
             '우리다같이TDF2040증권투자신탁(혼합-재간접형)ClassC-Pe',
             '신한마음편한TDF2040증권투자신탁[주식혼합-재간접형](종류C-re)',
             '삼성 한국형 TDF 2040 증권투자신탁H[주식혼합-재간접형]_Cpe(퇴직연금)',
             '미래에셋전략배분TDF2040년혼합자산자투자신탁 종류C-P2e',
             '교보악사 평생든든TDF 2040증권투자신탁(혼합-재간접형) Class C-Re(퇴직연금)',
             '한국투자TDF알아서2040증권투자신탁(주식혼합-재간접형)(C-Re)',
             'KB 온국민 TDF 2040 증권 투자신탁(주식혼합-재간접형) C-퇴직e']

def crawling():

    adj_pr_list = []
    for c in code_list:
        adj_pr = fc.AdjStdPrice(c)
        adj_pr['code'] = c
        adj_pr_list.append(adj_pr)
    adj_pr_df = pd.concat(adj_pr_list)

    fund_data = []
    for c in code_list:
        funds = fc.fund_crawling(c, 20170101, 20220212)
        funds['code'] = c
        fund_data.append(funds)
    price_df = pd.concat(fund_data)

    return adj_pr_df, price_df

# adj_pr_df, price_df = crawling()

def read_data():
    adj_pr_df = pd.read_csv('adj_pr.csv')
    price_df = pd.read_csv('fund_pr.csv')
    kfr_df = pd.read_csv('kfr_Trading.csv')

    return adj_pr_df, price_df, kfr_df

adj_pr_df, price_df, kfr_df = read_data()


def pre_setting():

    adj_pr_df, price_df, kfr_df = read_data()

    adj_pr_df = adj_pr_df[['code', 'trustAccend', 'standardCot']].copy()
    adj_pr_df['trustAccend'] = pd.to_datetime(adj_pr_df['trustAccend'], format='%Y%m%d')
    adj_pr_df = adj_pr_df.sort_values(['code', 'trustAccend'], ascending=True)

    price_df = price_df[['code', 'standardDt', 'standardCot']].copy()
    price_df['standardDt'] = pd.to_datetime(price_df['standardDt'], format='%Y%m%d')
    price_df = price_df.sort_values(['code', 'standardDt'], ascending=True)

    return adj_pr_df, price_df

adj_pr_df, price_df = pre_setting()

def AdjustedPrice(code):
    one_pr = price_df[price_df['code'] == code].copy()
    one_adj = adj_pr_df[adj_pr_df['code'] == code].copy()

    one_sr = one_pr.set_index('standardDt')['standardCot']

    one_adj['trustAccend'] = pd.to_datetime(one_adj['trustAccend'])
    one_adj['trustAccend'] = one_adj['trustAccend'] + dt.timedelta(days=1)
    end_date = one_adj['trustAccend'].tolist()

    dvdnd_dt = []
    for d in end_date:
        dvdnd_dt.append(one_sr.index[one_sr.index.get_loc(f'{d}', method='bfill')])

    one_adj.index = dvdnd_dt

    one_df = one_adj.drop(columns=['code', 'trustAccend']).rename(columns={'standardCot': 'dvdnd_pr'})

    one_pr = one_pr.set_index('standardDt')
    one_pr = one_pr.join(one_df, how='outer')

    kfr_df.columns = ['date', 'code', 'price']
    kfr_one = kfr_df[kfr_df['code'] == code]
    kfr_one['date'] = pd.to_datetime(kfr_one['date'], format='%Y-%m-%d')
    kfr_one = kfr_one.set_index('date')

    one_pr['kfr_pr'] = kfr_one['price']
    one_pr['dv_price'] = np.where(one_pr['dvdnd_pr'].notna(), one_pr.dvdnd_pr, one_pr.standardCot)
    one_pr['dly_rtn_notna'] = np.where(one_pr['dvdnd_pr'].notna(), one_pr.dv_price.pct_change(),
                                       one_pr.dv_price / (one_pr.standardCot.shift(1)))
    one_pr['dly_rtn_isna'] = np.where(one_pr['dvdnd_pr'].isna(), one_pr.dv_price.pct_change(),
                                      one_pr.dv_price / (one_pr.standardCot.shift(1)))

    dividend_dates = one_pr['dvdnd_pr'].dropna().index
    one_pr['dly_rtn_notna'][dividend_dates] = one_pr['dly_rtn_isna'][dividend_dates]

    one_pr['adj_pr'] = one_pr['dly_rtn_notna']
    one_pr['adj_pr'].iloc[0] = one_pr['dv_price'].iloc[0]
    one_pr['adj_pr'] = one_pr['adj_pr'].cumprod()

    one_pr = one_pr.drop(columns='dly_rtn_isna').rename(columns={'dly_rtn_notna': 'dly_rtn'})

    # fig, axes = plt.subplots()
    # axes.plot(one_pr['adj_pr'], '-b', label='KOFIA_Adjusted_Price')
    # axes.plot(one_pr['kfr_pr'], '-r', label='KFR_Adjusted_NAV')
    # axes.axis('equal')
    # plt.title(n)
    # # axes.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
    # # axes.xaxis.set_major_locator(mdates.YearLocator())
    # plt.xticks(rotation=45)
    # axes.legend()
    #
    # # plt.savefig(f'{n}.png')
    # plt.show()

    return one_pr


for f, n in zip(code_list, fund_name):
    fig, axes = plt.subplots()
    axes.plot(AdjustedPrice(f)['adj_pr'], '-b', label='KOFIA_Adjusted_Price')
    axes.plot(AdjustedPrice(f)['kfr_pr'], '-r', label='KFR_Adjusted_NAV')
    axes.axis('equal')
    plt.xticks(rotation=45)
    axes.legend()
    plt.title(n)
    plt.savefig(f'{n}.png')
    plt.show()


data_list = []

for f in code_list:
    data_list.append(AdjustedPrice(f)['adj_pr'].rename(f))

df = pd.concat(data_list, axis=1)
month_df = df.resample('M').last()
kkk = 0

# month_df.to_csv('~/dataknows/RichGo.Investment/adj_price/woori_irp_fund_monthly_adjusted_price.csv')


def plot_rtn():
    for n in fund_name:
        fig, axes = plt.subplots()
        axes.plot(one_pr['adj_pr'], '-b', label='KOFIA_Adjusted_Price')
        axes.plot(one_pr['kfr_pr'], '-r', label='KFR_Adjusted_NAV')
        axes.axis('equal')
        plt.title(n)
        # axes.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
        # axes.xaxis.set_major_locator(mdates.YearLocator())
        plt.xticks(rotation=45)
        axes.legend()

        plt.savefig(f'{n}.png')
        plt.show()

plot_rtn()

# one_pr.to_csv('~/dataknows/RichGo.Investment/adj_price/one_pr_v2.csv')

