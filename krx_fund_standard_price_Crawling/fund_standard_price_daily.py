import pandas as pd

#df = pd.read_csv('C:/Users/user/Desktop/일별_펀드기준가격/20000104.csv', encoding='cp949')

date_list = pd.date_range(start='20000104',end='20020628')
date_list = date_list.strftime('%Y%m%d')

set_source_lt = []
for date in date_list:
    try:
        df = pd.read_csv('C:/Users/user/Desktop/일별_펀드기준가격/{}.csv'.format(date), encoding='cp949')
        print(f'saved date. {date}')
    except:
        print(f'empty data. {date}')
        continue

    set_source_lt.append(df)

df = pd.concat(set_source_lt)

set_source_df = df.pivot(index='기준일자', columns='펀드코드', values='설정원본(백만원)')
standard_df = df.pivot(index='기준일자', columns='펀드코드', values='기준가격(원)_기준')
bill_df = df.pivot(index='기준일자', columns='펀드코드', values='기준가격(원)_과표')
all_fund_df = df.set_index('펀드코드')[['펀드명','펀드유형','설정일','판매회사']]

fund_reset_df = all_fund_df.reset_index()
fund_reset_df['펀드코드'].nunique() # => 20778
fund_reset_df['펀드코드'].value_counts() # => 최대 중복 개수: 738

copy_fund_df = fund_reset_df.copy()
copy_fund_df = copy_fund_df.sort_values('펀드코드')
dupl_fund_df = copy_fund_df.drop_duplicates(['펀드코드','설정일'], keep='last')

unique_fund_list = dupl_fund_df['펀드코드'].tolist()

for fund_code in unique_fund_list:
    if fund_code in copy_fund_df['펀드코드']:
        copy_fund_df['펀드명','설정일'] = dupl_fund_df['펀드명','설정일']


set_source_df.to_csv('C:/Users/user/Desktop/2000.01.04~2002.06.28펀드기준가격/설정원본(백만원).csv', encoding='utf-8-sig')
standard_df.to_csv('C:/Users/user/Desktop/2000.01.04~2002.06.28펀드기준가격/기준가격(원)_기준.csv', encoding='utf-8-sig')
bill_df.to_csv('C:/Users/user/Desktop/2000.01.04~2002.06.28펀드기준가격/기준가격(원)_과표.csv', encoding='utf-8-sig')
all_fund_df.to_csv('C:/Users/user/Desktop/2000.01.04~2002.06.28펀드기준가격/모든펀드.csv', encoding='utf-8-sig')