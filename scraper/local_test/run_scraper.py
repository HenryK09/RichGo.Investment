import pandas as pd
from scraper.fund_kr.api.fund_daily_by_ticker import get_adj_pr as get_one_fund_adj_pr
from scraper.fund_kr.api.fund_info import get_fund_info
from scraper.fund_kr.api.fund_info import code_info_added
from scraper.common.dbconn import DBConn
import concurrent.futures as futures
import numpy as np
import os
from scraper.fund_kr.api.backup import get_fund_name_sr

FUND_DB = os.getenv('FUND_DB_URI')


def update_fund_names():
    fund_names_sr = get_fund_name_sr(pd.Timestamp.now().strftime('%Y%m%d'))
    data_list = fund_names_sr.to_frame('product_name').reset_index().to_dict(orient='records')

    query = '''
        insert into fund_kofia.product_info (ticker, product_name)
        values (:ticker, :product_name)
        ON DUPLICATE KEY UPDATE
            product_name = VALUES(product_name),
            updated_at = now();
    '''

    with DBConn(FUND_DB).transaction():
        DBConn(FUND_DB).update(query, data_list)


def update_one_fund_daily(data_list):
    query = '''
        insert into fund_kofia.product_daily (ticker, base_dt, nav, tax_base_nav, aum, adj_pr)
        values (:ticker, :base_dt, :nav, :tax_base_nav, :aum, :adj_pr)
        ON DUPLICATE KEY UPDATE
            nav = VALUES(nav),
            tax_base_nav = VALUES(tax_base_nav),
            aum = VALUES(aum),
            adj_pr = VALUES(adj_pr),
            updated_at = now();
    '''

    DBConn(FUND_DB).update(query, data_list)


def update_one_fund_info(data_list):
    query = '''
        insert into fund_kofia.product_info (ticker, product_name, category, fund_type, 
                                             listing_dt, class_cd, trust_accounting_term, 
                                             invest_region, sales_region, trait_division, private_public, 
                                             ter, frontend_commission_rt, backend_commission_rt, mng_comp, 
                                             comp_cd, status, class_type, redemption_charge, characteristics, 
                                             locations, risk_level, is_hedged)
        values (:ticker, :product_name, :category, :fund_type, :listing_dt, :class_cd, 
                :trust_accounting_term, :invest_region, :sales_region, :trait_division, :private_public, :ter, 
                :frontend_commission_rt, :backend_commission_rt, :mng_comp, :comp_cd, :status, :class_type, 
                :redemption_charge, :characteristics, :locations, :risk_level, :is_hedged)
        ON DUPLICATE KEY UPDATE
            product_name = VALUES(product_name),
            category = VALUES(category),
            fund_type = VALUES(fund_type),
            listing_dt = VALUES(listing_dt),
            class_cd = VALUES(class_cd),
            trust_accounting_term = VALUES(trust_accounting_term),
            invest_region = VALUES(invest_region),
            sales_region = VALUES(sales_region),
            trait_division = VALUES(trait_division),
            private_public = VALUES(private_public),
            ter = VALUES(ter),
            frontend_commission_rt = VALUES(frontend_commission_rt),
            backend_commission_rt = VALUES(backend_commission_rt),
            mng_comp = VALUES(mng_comp),
            comp_cd = VALUES(comp_cd),
            status = VALUES(status),
            class_type = VALUES(class_type),
            redemption_charge = VALUES(redemption_charge),
            characteristics = VALUES(characteristics),
            locations = VALUES(locations),
            risk_level = VALUES(risk_level),
            is_hedged = VALUES(is_hedged),
            updated_at = now();
    '''

    DBConn(FUND_DB).update(query, data_list)


def fund_daily_worker(ticker, num):
    try:
        df = get_one_fund_adj_pr(ticker)
        df = df.replace([np.inf, -np.inf], np.nan)
        df = df.astype(object).where(df.notna(), None)
        data_list = df.reset_index().to_dict(orient='records')
        with DBConn(FUND_DB).transaction():
            update_one_fund_daily(data_list)
    except Exception as e:
        print(f'{ticker}({num}) - ERROR')
        raise e

    print(f'{ticker}({num})')
    return ticker


def fund_info_worker(ticker, num, base_dt):
    fund_info_df = get_fund_info(base_dt, ticker)
    df = code_info_added(fund_info_df)
    df = df.astype(object).where(df.notna(), None)
    data_list = df.reset_index().to_dict(orient='records')
    with DBConn(FUND_DB).transaction():
        update_one_fund_info(data_list)

    print(f'{ticker}({num})')
    return ticker


def get_empty_daily_tickers():
    # where 절에 내용이 있어야 쿼리가 빠름
    query = '''
        select ticker
        from fund_kofia.product_info
        where ticker not in (select distinct ticker from fund_kofia.product_daily)
    '''
    return DBConn(FUND_DB).fetch(query).list()


def get_all_tickers():
    query = '''
        select distinct ticker
        from fund_kofia.product_info
    '''
    return DBConn(FUND_DB).fetch(query).list()


def run_multi_process(worker, tickers, *args):
    finished = []
    print(f'total: {len(tickers)}')
    try:
        futures_list = []
        with futures.ProcessPoolExecutor() as executor:
            for i, ticker in enumerate(tickers):
                future = executor.submit(worker, ticker, i, *args)
                futures_list.append(future)

        result = futures.wait(futures_list)
        for future in result.done:
            finished.append(future.result())

    except Exception as e:
        raise e

    finally:
        print(f'len: {len(finished)}')


def update_fund_daily():
    tickers = get_empty_daily_tickers()
    run_multi_process(fund_daily_worker, tickers)


def update_fund_info(base_dt):
    tickers = get_all_tickers()
    run_multi_process(fund_info_worker, tickers, base_dt)


if __name__ == '__main__':
    BASE_DATE = '20220311'
    # update_fund_names(BASE_DATE)
    update_fund_daily()
    # update_fund_info(BASE_DATE)
