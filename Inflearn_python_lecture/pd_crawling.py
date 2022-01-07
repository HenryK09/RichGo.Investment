import requests
import pandas as pd

my_headers = {
    'referer': 'https://finance.naver.com/item/sise_day.naver?code=005930&page=1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'
}
page_number = 1

url = 'https://finance.naver.com/item/sise_day.naver?code=005930&page={}'.format(page_number) # {}안에 ()값이 들어감
res = requests.get(url=url, headers=my_headers) # url 링크 가져오기

df = pd.read_html(res.text)[0] # 반드시 tb이 존재해야 함 -> list로 반환
df = df.dropna()


df['날짜'] = pd.to_datetime(df['날짜'])
df['날짜'].dtype

df[df['날짜'] >= '2022.01.03']