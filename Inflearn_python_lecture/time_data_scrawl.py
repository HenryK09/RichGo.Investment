import requests
import pandas as pd

# 네이버 금융에서 당일 데이터 가져오기

my_headers = {
    'referer': 'https://finance.naver.com/item/sise_time.naver?code=005930&thistime=20220107153111&page=1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'
}

df_list = []
for i in range(1,40):
    url = 'https://finance.naver.com/item/sise_time.naver?code=005930&thistime=20220107153111&page={}'.format(i) # {}안에 ()값이 들어감
    res = requests.get(url, headers=my_headers)
    df_list.append(
        pd.read_html(res.text)[0].dropna()
    )

df = pd.concat(df_list)
df.drop_duplicates()

df = df.iloc[::-1].reset_index(drop=True)
df.to_csv('005930_220107.csv')