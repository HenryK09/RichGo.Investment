import pandas as pd
import numpy as np
import FundCrawler as fc

def price_crawl():
    fund_list = ['K55207BU0715',
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
                 'K55223BT1450']

    fund_data = []
    for i in fund_list:
        funds = fc.fund_crawling(i, 20170101, 20220208)
        funds['code'] = i
        fund_data.append(funds)

    df = pd.concat(fund_data)

    df['standardDt'] = pd.to_datetime(df['standardDt'], format='%Y%m%d')
    # df = df.set_index(df['standardDt'])
    price_df = df[['standardDt','standardCot','code']].copy()
    return price_df

def dvdnd_crawl():
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

    dvdnd_list = []
    for n in fund_name:
        try:
            dvdnd = fc.FundDividend(n, 20170101, 20220208)
            dvdnd_list.append(dvdnd)
        except:
            pass

    dvdnd_df = pd.concat(dvdnd_list)
    dvdnd_df.index = pd.to_datetime(dvdnd_df.index, format='%Y%m%d')

    dividend_df = dvdnd_df[['표준코드','분배율']].copy()
    return dividend_df

price_df = price_df.set_index(['standardDt','code'])
dividend_df = dividend_df.reset_index()
dividend_df = dividend_df.rename(columns={'회계기말':'standardDt',
                                          '표준코드':'code'})
dividend_df = dividend_df.set_index(['standardDt','code'])

fund_df = price_df.join(dividend_df)
fund_df['분배율'] = fund_df['분배율']/100
fund_df['분배율'] = fund_df['분배율'].shift(-1)

fund_df = fund_df.reset_index()
fund_df = fund_df.sort_values(by=['code','standardDt'], ascending=True)
fund_df = fund_df.replace(np.nan, 0)
fund_df['dvdnd_applied'] = fund_df['standardCot'] + (1000 * fund_df['분배율'])


fund_df['분배율'] = fund_df['분배율'].replace(0, np.nan)

# if fund_df['분배율'] == np.nan:
#      fund_df['daily_rtn'] = fund_df['dvdnd_applied'].pct_change()
# else:
#     fund_df['daily_rtn'] = fund_df['dvdnd_applied']/fund_df['standardCot']


fund_df.to_csv('~/dataknows/RichGo.Investment/adj_price/woori_fund.csv', encoding='utf-8-sig')


daily_adj_df = pd.read_csv('~/dataknows/RichGo.Investment/adj_price/woori_fund_adj.csv')
daily_adj_df['standardDt'] = pd.to_datetime(daily_adj_df['standardDt'])
# pivot_dap = daily_adj_df.pivot(index='standardDt', columns='code', )
# daily_adj_df.to_csv('~/dataknows/RichGo.Investment/adj_price/woori_fund_adj_v2.csv', encoding='utf-8-sig')

mon_adj_df = daily_adj_df[['standardDt', 'code', 'adj_price']].copy()
mon_adj_df = mon_adj_df.set_index(['standardDt'])
mon_adj_df = mon_adj_df.groupby(['code']).resample('M').last()
mon_adj_df = mon_adj_df.drop(columns='code').reset_index()
mon_adj_df = mon_adj_df.set_index('code')
mon_adj_df.to_csv('~/dataknows/RichGo.Investment/adj_price/woori_fund_mon.csv', encoding='utf-8-sig')

kfr_df = pd.read_csv('~/dataknows/RichGo.Investment/adj_price/kfr_Trading.csv')
kfr_df.columns = ['date','code','price']
kfr_df = kfr_df.pivot(index='date', columns='code', values='price')
kfr_df.to_csv('~/dataknows/RichGo.Investment/adj_price/kfr_df.csv')


kofia_df = daily_adj_df.pivot(index='standardDt', columns='code', values='adj_price')
kofia_df.to_csv('~/dataknows/RichGo.Investment/adj_price/kofia_df.csv')

# kfr_df = kfr_df.fillna(0)
# kofia_df = kofia_df.fillna(0)
# diff = kfr_df - kofia_df

# diff_df = pd.concat([kfr_df,kofia_df]).drop_duplicates(keep=True)
kfr_df.equals(kofia_df)
# kfr_df.compare(kofia_df, align_axis=0)
# kfr_df.reset_index(drop=True) == kofia_df.reset_index(drop=True)
diff_df = pd.concat([kfr_df, kofia_df])
diff_df = diff_df.reset_index(drop=True)

diff_gp = diff_df.groupby(list(diff_df.columns))

idx = [x[0] for x in diff_gp.groups.values() if len(x) == 1]

val_diff = diff_df.reindex(idx)




name_code_df = pd.DataFrame(fund_name, fund_list)
woori_df = mon_adj_df.join(name_code_df, how='outer')
woori_df = woori_df.rename(columns={0:'name'})
woori_df = woori_df.reset_index()
woori_df = woori_df.rename(columns={'index':'code'}).set_index(['name','code'])
woori_df = woori_df.reset_index()
woori_df = woori_df.pivot(index='standardDt', columns=['name','code'], values='adj_price')

woori_df.to_csv('~/dataknows/RichGo.Investment/adj_price/woori_fund.csv', encoding='utf-8-sig')