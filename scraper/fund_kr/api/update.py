from scraper.fund_kr.api.fund_daily_by_ticker import get_adj_pr
from scraper.fund_kr.api.fund_info import get_fund_info
from scraper.fund_kr.api.fund_sales_comp import get_sales_comp_fund
from pangres import upsert
from scraper.common import get_engine


def to_product_daily(ticker):
    engine = get_engine()
    adj_pr_df = get_adj_pr(ticker)
    upsert(con=engine,
           df=adj_pr_df,
           schema='fund_kofia',
           table_name='product_daily',
           if_row_exists='update'
           )


def to_product_info(base_dt, ticker):
    engine = get_engine()
    info_df = get_fund_info(base_dt, ticker)
    upsert(con=engine,
           df=info_df,
           schema='fund_kofia',
           table_name='product_info',
           if_row_exists='update'
           )


def to_product_sales_company(salecomp_dt, salecomp_cd):
    engine = get_engine()
    sales_comp_df = get_sales_comp_fund(salecomp_dt, salecomp_cd)
    upsert(con=engine,
           df=sales_comp_df,
           schema='fund_kofia',
           table_name='product_sales_company',
           if_row_exists='update'
           )
