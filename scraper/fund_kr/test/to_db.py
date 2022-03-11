from scraper.fund_kr.api.update import to_product_daily
from scraper.fund_kr.api.update import to_product_info
from scraper.fund_kr.api.update import to_product_sales_company


def to_daily(ticker):
    to_price = to_product_daily(ticker)
    return to_price


def to_info(base_dt, ticker):
    to_info = to_product_info(base_dt, ticker)
    return to_info


def to_comp(salecomp_dt, salecomp_cd):
    to_comp = to_product_sales_company(salecomp_dt, salecomp_cd)
    return to_comp


if __name__ == '__main__':
    test_base_dt = '20220304'
    test_ticker = 'K55101BA9725'

    test_salecomp_dt = '20211231'
    test_salecomp_cd = 'A01048'

    # pymysql.install_as_MySQLdb()

    # to_daily(test_ticker)
    # to_info(test_base_dt, test_ticker)
    to_comp(test_salecomp_dt, test_salecomp_cd)
