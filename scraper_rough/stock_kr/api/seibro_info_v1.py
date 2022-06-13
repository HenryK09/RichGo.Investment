import time
import pandas as pd
import requests
import re
import numpy as np


def get_adj_dps_info(from_dt=None, to_dt=None, name_kr=None):
    if to_dt is None:
        to_dt = pd.Timestamp.now(tz='Asia/Seoul').strftime('%Y%m%d')
    else:
        to_dt = pd.Timestamp(to_dt).strftime('%Y%m%d')

    if from_dt is None:
        from_dt = to_dt
    else:
        from_dt = pd.Timestamp(from_dt).strftime('%Y%m%d')

    if name_kr is None:
        name_kr = ''

    url = 'https://seibro.or.kr/websquare/engine/proworks/callServletService.jsp'
    header = {
        'Referer': 'https://seibro.or.kr/websquare/control.jsp?w2xPath=/IPORTAL/user/company/BIP_CNTS01041V.xml&menuNo=285'
    }
    ticker_select_data = """
    <reqParam action="divStatInfoListCnt" task="ksd.safe.bip.cnts.Company.process.EntrFnafInfoPTask">
    <RGT_STD_DT_FROM value="{from_date}"/>
    <RGT_STD_DT_TO value="{to_date}"/>
    </reqParam>""".format(from_date=from_dt, to_date=to_dt)

    r = requests.post(url, data=ticker_select_data, headers=header)

    text = re.search(r'(<.*\"\d+\"/>)', r.text).group(0)
    data_count = int(re.search(r'\"\d+\"', text).group(0)[1:-1])
    if data_count < 1:
        return None

    result_data = []
    for x in range(int(np.ceil(data_count / 15))):
        data = """
        <reqParam action="divStatInfoPList" task="ksd.safe.bip.cnts.Company.process.EntrFnafInfoPTask">
        <RGT_STD_DT_FROM value="{from_date}"/>
        <RGT_STD_DT_TO value="{to_date}"/>
        <ISSUCO_CUSTNO value=""/>
        <KOR_SECN_NM value="{name}"/>
        <SECN_KACD value=""/>
        <RGT_RSN_DTAIL_SORT_CD value=""/>
        <LIST_TPCD value=""/>
        <START_PAGE value="{start_page}"/>
        <END_PAGE value="{end_page}"/>
        <MENU_NO value="285"/>
        <CMM_BTN_ABBR_NM value="allview,allview,print,hwp,word,pdf,searchIcon,seach,xls,link,link,wide,wide,top,"/>
        <W2XPATH value="/IPORTAL/user/company/BIP_CNTS01041V.xml"/>
        </reqParam>""".format(from_date=from_dt,
                              to_date=to_dt,
                              name=name_kr,
                              start_page=x * 15 + 1,
                              end_page=x * 15 + 15).encode('utf-8')

        r = requests.post(url, data=data, headers=header)

        for a in re.findall(r'(<result>.*</result>)', r.text):
            temp_item_info = {}
            for b in re.findall(r'<\w+\svalue=.*/>', a.replace('/>', '/>\n')):
                items = b.split(' value=')
                temp_item_info[items[0][1:]] = items[1][1:-3]

            result_data.append(temp_item_info)

        time.sleep(1)

    df = pd.DataFrame(result_data).rename(columns={
        'RGT_STD_DT': 'base_dt',
        'TH1_PAY_TERM_BEGIN_DT': 'payment_dt',
        'DELI_DT': 'delivery_dt',
        'SHOTN_ISIN': 'ticker',
        'KOR_SECN_NM': 'name_kr',
        'LIST_TPNM': 'market',
        'RGT_RSN_DTAIL_SORT_NM': 'dividend_division',
        'SECN_DTAIL_KANM': 'stock_type',
        'CASH_ALOC_AMT': 'DPS',
        'DIFF_ALOC_AMT': 'DPS_diff',
        'CASH_ALOC_RATIO': 'adj_DPS_cash',
        'STK_ALOC_RATIO': 'dividend_rate_stock',
        'DIFF_ALOC_RATIO1': 'diff_dividend_rate_cash',
        'DIFF_ALOC_RATIO2': 'diff_dividend_rate_stock',
        'PVAL': 'par_value',
        'SETACC_MM': 'closing_month',
        'ISSUCO_CUSTNO': 'company_num'
    })
    df = df.drop(columns=['RGT_RACD', 'SETACC_MMDD', 'AG_ORG_TPNM'])
    df['base_dt'] = pd.to_datetime(df['base_dt'].astype(str)).dt.strftime('%Y-%m-%d')
    df['payment_dt'] = pd.to_datetime(df['payment_dt'].astype(str)).dt.strftime('%Y-%m-%d')
    df['delivery_dt'] = pd.to_datetime(df['delivery_dt'].astype(str)).dt.strftime('%Y-%m-%d')
    df['ticker'] = df['ticker'].astype(str)
    df = df.set_index(['ticker'])
    df['adj_DPS_cash'] = df['adj_DPS_cash'].astype(int)
    df['dividend_rate_stock'] = df['dividend_rate_stock'].astype(float) / 100
    df['par_value'] = df['par_value'].astype(int)

    # df = df[df['ticker'].notnull()]
    # df['product_name'] = df['product_name'].replace(r'amp;', '', regex=True)
    return df


df = get_adj_dps_info(from_dt='20210101', to_dt='20220413', name_kr='SK케미칼')
dd=0

def get_changed_shares_info(from_dt=None, to_dt=None, name_kr=None):
    if to_dt is None:
        to_dt = pd.Timestamp.now(tz='Asia/Seoul').strftime('%Y%m%d')
    else:
        to_dt = pd.Timestamp(to_dt).strftime('%Y%m%d')

    if from_dt is None:
        from_dt = to_dt
    else:
        from_dt = pd.Timestamp(from_dt).strftime('%Y%m%d')

    if name_kr is None:
        name_kr = ''

    company_num = get_adj_dps_info(from_dt=from_dt, to_dt=to_dt, name_kr=name_kr)['company_num'].values.any()

    url = 'https://seibro.or.kr/websquare/engine/proworks/callServletService.jsp'
    header = {
        'Referer': 'https://seibro.or.kr/websquare/control.jsp?w2xPath=/IPORTAL/user/company/BIP_CNTS01012V.xml&menuNo=282'}
    data = """
    <reqParam action="chgDetailsListCnt" task="ksd.safe.bip.cnts.Company.process.EntrFnafInfoPTask">
    <MENU_NO value="282"/>
    <CMM_BTN_ABBR_NM value="allview,allview,print,hwp,word,pdf,searchIcon,seach,xls,link,link,wide,wide,top,"/>
    <W2XPATH value="/IPORTAL/user/company/BIP_CNTS01012V.xml"/>
    <ISSUCO_CUSTNO value="{company}"/>
    <ISSU_DT_FROM value="{from_date}"/>
    <ISSU_DT_TO value="{to_date}"/>
    </reqParam>
    """.format(company=company_num,
               from_date=from_dt,
               to_date=to_dt,
               )

    r = requests.post(url, data=data, headers=header)

    text = re.search(r'(<.*\"\d+\"/>)', r.text).group(0)
    data_count = int(re.search(r'\"\d+\"', text).group(0)[1:-1])
    if data_count < 1:
        return None

    result_data = []
    for x in range(int(np.ceil(data_count / 30))):
        data = """
            <reqParam action="chgDetailsListEL1" task="ksd.safe.bip.cnts.Company.process.EntrFnafInfoPTask">
            <MENU_NO value="282"/>
            <CMM_BTN_ABBR_NM value="allview,allview,print,hwp,word,pdf,searchIcon,seach,xls,link,link,wide,wide,top,"/>
            <W2XPATH value="/IPORTAL/user/company/BIP_CNTS01012V.xml"/>
            <ISSUCO_CUSTNO value="{company}"/>
            <RGT_LINK_RACD value=""/>
            <SECN_KACD value="0101"/>
            <ISSU_DT_FROM value="{from_date}"/>
            <ISSU_DT_TO value="{to_date}"/>
            <STARTPAGE value="{start_page}"/>
            <ENDPAGE value="{end_page}"/>
            </reqParam>""".format(from_date=from_dt,
                                  to_date=to_dt,
                                  company=company_num,
                                  start_page=x * 15 + 1,
                                  end_page=x * 15 + 15).encode('utf-8')

        r = requests.post(url, data=data, headers=header)

        for a in re.findall(r'(<result>.*</result>)', r.text):
            temp_item_info = {}
            for b in re.findall(r'<\w+\svalue=.*/>', a.replace('/>', '/>\n')):
                items = b.split(' value=')
                temp_item_info[items[0][1:]] = items[1][1:-3]

            result_data.append(temp_item_info)

        time.sleep(1)

        df = pd.DataFrame(result_data).rename(columns={
            'ISSU_DT': 'issue_dt',
            'REP_SECN_NM': 'name_kr',
            'SECN_KACD_NM': 'stock_type',
            'SECN_ISSU_NTIMES': 'issue_count',
            'RGT_LINK_RACD_NM': 'issue_reason',
            'PVAL': 'par_value',
            'LIST_DT': 'listing_dt',
            'ISSU_QTY': 'issued_shares',
            'ISSU_FORM': 'issue_form',
            'ISSUPRC': 'issued_pr_share'
        })
        df = df.drop(columns=['SECN_KACD', 'RGT_LINK_RACD'])
        df['issue_dt'] = pd.to_datetime(df['issue_dt'].astype(str)).dt.strftime('%Y-%m-%d')
        df['listing_dt'] = pd.to_datetime(df['listing_dt'].astype(str)).dt.strftime('%Y-%m-%d')
        df = df.set_index(['name_kr'])

        return df


def get_changed_shares_info2(ticker, from_dt=None, to_dt=None):
    if to_dt is None:
        to_dt = pd.Timestamp.now(tz='Asia/Seoul').strftime('%Y%m%d')
    else:
        to_dt = pd.Timestamp(to_dt).strftime('%Y%m%d')

    if from_dt is None:
        from_dt = '19000101'
    else:
        from_dt = pd.Timestamp(from_dt).strftime('%Y%m%d')

    company_num = int(ticker[:-1])
    url = 'https://seibro.or.kr/websquare/engine/proworks/callServletService.jsp'
    header = {
        'Referer': 'https://seibro.or.kr/websquare/control.jsp?w2xPath=/IPORTAL/user/company/BIP_CNTS01012V.xml&menuNo=282'
    }

    data = f'''
    <reqParam action="chgDetailsListCheckEL1" task="ksd.safe.bip.cnts.Company.process.EntrFnafInfoPTask">
      <MENU_NO value="282"/>
      <CMM_BTN_ABBR_NM value="allview,allview,print,hwp,word,pdf,searchIcon,seach,xls,link,link,wide,wide,top,"/>
      <W2XPATH value="/IPORTAL/user/company/BIP_CNTS01012V.xml"/>
      <ISSUCO_CUSTNO value="{company_num}"/>
      <RGT_LINK_RACD value=""/>
      <SECN_KACD value="0101"/>
      <ISSU_DT_FROM value="{from_dt}"/>
      <ISSU_DT_TO value="{to_dt}"/>
      <STARTPAGE value="1"/>
      <ENDPAGE value="10000"/>
    </reqParam>
    '''.encode('utf-8')

    r = requests.post(url, data=data, headers=header)

    issue_list = []
    for a in re.findall(r'(<result>.*</result>)', r.text):
        temp_item_info = {}
        for b in re.findall(r'<\w+\svalue=.*/>', a.replace('/>', '/>\n')):
            items = b.split(' value=')
            temp_item_info[items[0][1:]] = items[1][1:-3]
        issue_list.append(temp_item_info)

    df = pd.DataFrame(issue_list).rename(columns={
        'ISSU_DT': 'issue_dt',
        'REP_SECN_NM': 'name_kr',
        'SECN_KACD_NM': 'stock_type',
        'SECN_ISSU_NTIMES': 'issue_count',
        'RGT_LINK_RACD_NM': 'issue_reason',
        'PVAL': 'par_value',
        'LIST_DT': 'listing_dt',
        'ISSU_QTY': 'issued_shares',
        'ISSU_FORM': 'issue_form',
        'ISSUPRC': 'issued_pr_share'
    })
    df = df.drop(columns=['SECN_KACD', 'RGT_LINK_RACD'])
    df['issue_dt'] = pd.to_datetime(df['issue_dt'])
    df['listing_dt'] = pd.to_datetime(df['listing_dt'])
    df = df.set_index(['name_kr'])

    return df
