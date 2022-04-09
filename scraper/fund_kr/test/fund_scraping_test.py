from scraper.fund_kr.api.fund_daily_by_date import get_fund_daily
from scraper.fund_kr.api.fund_daily_by_ticker import get_adj_pr
from scraper.fund_kr.api.fund_info import get_fund_info
from scraper.fund_kr.api.backup import get_fund_name_sr
from scraper.fund_kr.api.fund_sales_comp import get_sales_comp_fund
import time


# 기준일 하루치 전체 펀드 기준가격 정보 가져오기
def get_fund_daily_test(base_dt):
    fund_daily_df = get_fund_daily(base_dt)
    return fund_daily_df


# 펀그코드별 역대 수정기준가격 정보가 포함된 가격정보 가져오기
def get_fund_adj_pr_test(ticker):
    fund_adj_pr_df = get_adj_pr(ticker)
    return fund_adj_pr_df


# 펀드코드별 펀드기본정보 가져오기
def get_fund_info_test(base_dt, ticker):
    fund_info_df = get_fund_info(base_dt, ticker)
    return fund_info_df


# 펀드판매회사별 펀드코드와 펀드명 정보 가져오기
def get_fund_sales_comp_test(base_dt, salecomp):
    sales_comp_list = get_sales_comp_fund(base_dt, salecomp)
    return sales_comp_list


# 기준일 전체 펀드코드와 펀드명 정보 가져오기
def get_fund_code_name_test(base_dt):
    code_name = get_fund_name_sr(base_dt)
    return code_name


if __name__ == '__main__':
    test_base_dt = '20220315'
    test_ticker = 'K55364B65638'
    test_salecomp_dt = '20211231'
    test_salecomp_cd = 'A01040'

    start = time.time()

    # print(get_fund_daily_test(test_base_dt))
    print(get_fund_adj_pr_test(test_ticker))
    # print(get_fund_info_test(test_base_dt, test_ticker).T)
    # print(get_fund_sales_comp_test(test_salecomp_dt, test_salecomp_cd))

    # print(get_fund_code_name_test(test_base_dt))

    end = time.time()
    print(end - start)
