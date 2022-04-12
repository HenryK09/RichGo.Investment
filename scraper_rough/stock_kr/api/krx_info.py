import pandas as pd
import requests
import json
import datetime

proxies = {
    'http': 'socks5://127.0.0.1:9050',
    'https': 'socks5://127.0.0.1:9050'
}


def get_basic_info():
    url = 'http://data.krx.co.kr/comm/bldAttendant/getJsonData.cmd'
    data = {
        'bld': 'dbms/MDC/STAT/standard/MDCSTAT01901',
        'locale': 'ko_KR',
        'mktId': 'ALL',
        'share': '1',
        'csvxls_isNo': 'false'
    }
    req = requests.post(url, data=data,
                        # proxies=proxies
                        )
    jsn = json.loads(req.text)
    info_df = pd.json_normalize(jsn, 'OutBlock_1')
    columns = {
        'ISU_CD': 'full_cd',
        'ISU_SRT_CD': 'ticker',
        'ISU_NM': 'item_name_kr',
        'ISU_ABBRV': 'name_kr',
        'ISU_ENG_NM': 'product_name_eng',
        'LIST_DD': 'listing_dt',
        'MKT_TP_NM': 'mkt_nm',
        'SECUGRP_NM': 'securities_class',
        'SECT_TP_NM': 'department',
        'KIND_STKCERT_TP_NM': 'stock_type',
        'PARVAL': 'par_value',
        'LIST_SHRS': 'listed_shares'
    }
    info_df = info_df.rename(columns=columns)
    info_df['listing_dt'] = pd.to_datetime(info_df['listing_dt']).dt.strftime('%Y-%m-%d')
    info_df = info_df.set_index('ticker')

    return info_df


# info_df = get_basic_info()


def get_weekly_dividend_info(base_dt):
    url = 'http://data.krx.co.kr/comm/bldAttendant/getJsonData.cmd'
    data = {
        'bld': 'dbms/MDC/STAT/standard/MDCSTAT03501',
        'locale': 'ko_KR',
        'searchType': '1',
        'mktId': 'ALL',
        'trdDd': f'{base_dt}',
        'csvxls_isNo': 'false'
    }
    req = requests.post(url, data=data,
                        # proxies=proxies
                        )
    jsn = json.loads(req.text)
    dividend_df = pd.json_normalize(jsn, 'output')
    columns = {
        'ISU_SRT_CD': 'ticker',
        'ISU_ABBRV': 'name_kr',
        'TDD_CLSPRC': 'std_pr',
        'CMPPREVDD_PRC': 'change',
        'FLUC_RT': 'pct_change',
        'FWD_EPS': 'fwd_EPS',
        'FWD_PER': 'fwd_PER',
        'DVD_YLD': 'dividend_yield'
    }
    dividend_df = dividend_df.rename(columns=columns)
    dividend_df['base_dt'] = base_dt
    dividend_df = dividend_df.set_index(pd.to_datetime(dividend_df['base_dt'].astype(str)).dt.strftime('%Y-%m-%d'))
    dividend_df = dividend_df.drop(columns=['ISU_ABBRV_STR', 'FLUC_TP_CD', 'base_dt'])
    dividend_df['from_dt'] = (pd.to_datetime(dividend_df.index) - datetime.timedelta(days=7)).strftime('%Y-%m-%d')
    return dividend_df


# dividend_df = get_weekly_dividend_info('20220325')

def get_dividend_info():
    url = 'http://data.krx.co.kr/comm/bldAttendant/getJsonData.cmd'
    data = {
        'bld': 'dbms/MDC/STAT/issue/MDCSTAT20901',
        'locale': 'ko_KR',
        'mktId': 'ALL',
        'tboxisuCd_finder_comnm0_1': '전체',
        'isuCd': 'ALL',
        'isuCd2': 'ALL',
        'basYy': '2021',
        'indTpCd': '1',
        'share': '1',
        'money': '1',
        'csvxls_isNo': 'true'
    }
    req = requests.post(url, data=data,
                        # proxies=proxies
                        )
    jsn = json.loads(req.text)
    dvd_df = pd.json_normalize(jsn, 'output')
    columns = {
        'ISU_CD': 'ticker',
        'ISU_NM': 'item_name_kr',
        'MKT_NM': 'mkt_nm',
        'BZ_YY': 'business_year',
        'ACNTCLS_MM': 'accounting_closing_month',
        'IDX_IND_NM': 'sector',
        'DIV_YD': 'dividend_yield',
        'PERSHR_DIV_CMSTK_SHRS': 'stock_dividend',
        'STK_DIV_BAS_DD': 'stock_dividend_base_dt',
        'PARVAL': 'par_value',
        'CMSTK_DPS': 'DPS',
        'MKTPRC_CMSTK_DIV_RT': 'dividend_yield_ratio',
        'DIV_INCLIN': 'dividend_payout_ratio',
        'LIST_SHRS': 'listed_shares',
        'DIV_TOTAMT': 'dividend_total_amount'
    }
    dvd_df = dvd_df.rename(columns=columns)
    dvd_df = dvd_df.drop(
        columns=['PRSNT_PRC', 'FLUC_TP_CD', 'CMPPRVDD_PRC', 'FLUC_RT', 'TDD_OPNPRC', 'TDD_HGPRC', 'TDD_LWPRC',
                 'ACC_TRDVOL', 'ACC_TRDVAL', 'MKTCAP', 'DIV_INCLIN_TP'])
    dvd_df['stock_dividend_base_dt'] = pd.to_datetime(dvd_df['stock_dividend_base_dt'].astype(str)).dt.strftime(
        '%Y-%m-%d')

    return dvd_df


# dvd_df = get_dividend_info()


def get_ipo_info(start, end):
    url = 'http://data.krx.co.kr/comm/bldAttendant/getJsonData.cmd'
    data = {
        'bld': 'dbms/MDC/STAT/issue/MDCSTAT20001',
        'locale': 'ko_KR',
        'mktId': 'ALL',
        'tboxisurCd_finder_comnm0_0': '전체',
        'isurCd': 'ALL',
        'isurCd2': 'ALL',
        'listClssCd': 'ALL',
        'secugrpTp': 'ALL',
        'cntrIsoCd': 'ALL',
        'strtDd': f'{start}',
        'endDd': f'{end}',
        'share': '1',
        'csvxls_isNo': 'true'
    }
    req = requests.post(url, data=data,
                        # proxies=proxies
                        )
    jsn = json.loads(req.text)
    ipo_df = pd.json_normalize(jsn, 'output')
    columns = {
        'ISU_CD': 'ticker',
        'ISU_NM': 'item_name_kr',
        'MKT_NM': 'mkt_nm',
        'SECUGRP_NM': 'securities_class',
        'KIND_STKCERT_TP_NM': 'stock_type',
        'LIST_DD': 'listing_dt',
        'DELIST_DD': 'delisting_dt',
        'LIST_CLSS_NM': 'listed_class_nm',
        'LEADCOM_MBR_NM': 'ipo_lead_company',
        'PARVAL': 'par_value',
        'PUBOFR_PRC': 'public_offer_pr',
        'PUBOFR_SHRS': 'public_offer_shares',
        'FIRST_LIST_SHRS': 'first_listed_shares',
        'LIST_SHRS': 'listed_shares',
        'IND_ABBRV': 'sector',
        'CNTR_ISO_NM': 'country',
    }
    ipo_df = ipo_df.rename(columns=columns)
    ipo_df = ipo_df.drop(columns=['PAR_TP_CD', 'FLUC_TP_CD', 'TDD_CLSPRC',
                                  'CMPPRVDD_PRC', 'FLUC_RT', 'TDD_OPNPRC',
                                  'TDD_HGPRC', 'TDD_LWPRC', 'ACC_TRDVOL',
                                  'ACC_TRDVAL', 'MKTCAP'])
    ipo_df['listing_dt'] = pd.to_datetime(ipo_df['listing_dt'].astype(str)).dt.strftime('%Y-%m-%d')
    ipo_df['delisting_dt'] = pd.to_datetime(ipo_df['delisting_dt'].astype(str)).dt.strftime('%Y-%m-%d')

    return ipo_df


# ipo_df = get_ipo_info(start='20211228', end='20220328')


def get_delisting_info(start, end):
    url = 'http://data.krx.co.kr/comm/bldAttendant/getJsonData.cmd'
    data = {
        'bld': 'dbms/MDC/STAT/issue/MDCSTAT23801',
        'locale': 'ko_KR',
        'mktId': 'ALL',
        'tboxisuCd_finder_listdelisu0_3': '전체',
        'isuCd': 'ALL',
        'isuCd2': 'ALL',
        'strtDd': f'{start}',
        'endDd': f'{end}',
        'share': '1',
        'csvxls_isNo': 'true'
    }
    req = requests.post(url, data=data,
                        # proxies=proxies
                        )
    jsn = json.loads(req.text)
    del_df = pd.json_normalize(jsn, 'output')
    columns = {
        'ISU_CD': 'ticker',
        'ISU_NM': 'item_name_kr',
        'MKT_NM': 'mkt_nm',
        'SECUGRP_NM': 'securities_group_nm',
        'KIND_STKCERT_TP_NM': 'stock_type',
        'LIST_DD': 'listing_dt',
        'DELIST_DD': 'delisting_dt',
        'DELIST_RSN_DSC': 'delisting_reason',
        'ARRANTRD_MKTACT_ENFORCE_DD': 'enforcement_dt',
        'ARRANTRD_END_DD': 'trading_end_dt',
        'IDX_IND_NM': 'sector',
        'PARVAL': 'par_value',
        'LIST_SHRS': 'listed_shares',
        'TO_ISU_SRT_CD': 'transfer_ticker',
        'TO_ISU_ABBRV': 'transfer_name_kr'
    }
    del_df = del_df.rename(columns=columns)
    del_df = del_df.set_index('ticker')

    del_df['listing_dt'] = pd.to_datetime(del_df['listing_dt'].astype(str)).dt.strftime('%Y-%m-%d')
    del_df['delisting_dt'] = pd.to_datetime(del_df['delisting_dt'].astype(str)).dt.strftime('%Y-%m-%d')
    del_df['enforcement_dt'] = pd.to_datetime(del_df['enforcement_dt'].astype(str)).dt.strftime('%Y-%m-%d')
    del_df['trading_end_dt'] = pd.to_datetime(del_df['trading_end_dt'].astype(str)).dt.strftime('%Y-%m-%d')

    return del_df


# del_df = get_delisting_info(start='20200318', end='20220328')


k = 0
