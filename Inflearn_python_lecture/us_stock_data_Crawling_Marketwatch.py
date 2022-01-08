import requests
import pandas as pd

# 미국 주식 재무제표 데이터 크롤링

res = requests.get('https://www.marketwatch.com/investing/stock/aapl/financials/cash-flow/quarter')

df_list = pd.read_html(res.text)

df = df_list[4]

# 미국 주식 일별 시세 크롤링
from urllib.parse import unquote

url = "https://www.marketwatch.com/investing/stock/aapl/downloaddatapartial?partial=true&index=0&countryCode=&iso=&startDate=12%2F08%2F2021%2000%3A00%3A00&endDate=01%2F07%2F2022%2023%3A59%3A59&frequency=P1D&downloadPartial=true&csvDownload=false&newDates=false"

# decoding
url = unquote(url)  # 'https://www.marketwatch.com/investing/stock/aapl/downloaddatapartial?partial=true&index=0&countryCode=&iso=&startDate=12/08/2021 00:00:00&endDate=01/07/2022 23:59:59&frequency=P1D&downloadPartial=true&csvDownload=false&newDates=false'

for i in range(5):
    url = 'https://www.marketwatch.com/investing/stock/aapl/downloaddatapartial?partial=true&index={}&countryCode=&iso=&startDate=12/08/2021 00:00:00&endDate=01/07/2022 23:59:59&frequency=P1D&downloadPartial=true&csvDownload=false&newDates=false'.format(i)
    pd.read_html(requests.get(url).text)

# 마지막 페이지부터는 계속 똑같은 데이터 받는지(네이버금융) 체크 -> False

# 여러 종목의 가격데이터 받아와서 합치기
start_date = "09/06/2021"
end_date = "01/06/2022"

my_tickers = ['aapl','msft']

import time

price_df_list = []
url_format = 'https://www.marketwatch.com/investing/stock/aapl/downloaddatapartial?partial=true&index={}&countryCode=&iso=&startDate=12/08/2021 00:00:00&endDate=01/07/2022 23:59:59&frequency=P1D&downloadPartial=true&csvDownload=false&newDates=false'
for ticker in my_tickers:
    temp_df_list = []
    i = 0
    while True:
        url = url_format.format(
            ticker=ticker,
            index=i,
            start_date=start_date,
            end_date=end_date,
        )
        try:
            df = pd.read_html(requests.get(url).text)[0]
            df['Date Date'].apply(lambda x: x[len(x) // 2:].strip())
            # 길이가 중간 기준 10으로 같음. len(x)=값의 길이 나누기 2 => x[len(x) // 2:] 중간 인덱스 지점부터 우측 날짜 데이터만 string으로 인덱싱싱
            df = df.rename(columns={"Date Date": "Date"})
            df = df.set_index("Date")
            df.index = pd.to_datetime(df.index) # string -> datetime
            temp_df_list.append(df) # 만들어놓은 리스트에 넣기
        except ValueError:
            # 주어진 기간의 데이터가 다 나왔음에도 index를 계속 증가시키면 No table found Error가 발생함
            # 이 때 loop을 중단시킨다.
            # 중단 전, 모았던 데이터를 하나로 합친다.
            price_df = pd.concat(temp_df_list)
            price_df_list.append(price_df)
            break

        # 예외가 발생하지 않은 경우
        i = i + 1 # 인덱스 1 증가
        time.sleep(0.5)

df = pd.concat(price_df_list, keys=my_tickers)

df = df.reset_index() # 각 row가 하나의 column이 됨

df.dtypes # column별 데이터 종류

close_df = df.pivot(columns="level_0", index="Date", values="Close")

# map, apply, applymap에 대해 구글링에서 반드시 공부하기를 권장!
close_df = close_df.applymap(lambda x: float(x[1:])) # 달러 표시 날려버리기

close_df.plot(figsize=(10,5))


