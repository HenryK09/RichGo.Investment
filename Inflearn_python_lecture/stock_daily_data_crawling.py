import requests
import bs4
import time
import random
import pandas as pd
from datetime import datetime


my_headers = {
    'referer': 'https://finance.naver.com/item/sise_day.naver?code=005930&page=1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'
}


# 모든 page에 대해서 가져오기
total_data_list = []
page_number = 1
prev_date_time_set = set()
while True:
    url = 'https://finance.naver.com/item/sise_day.naver?code=005930&page={}'.format(page_number) # {}안에 ()값이 들어감
    res = requests.get(url=url, headers=my_headers) # url 링크 가져오기

    soup = bs4.BeautifulSoup(res.text,'lxml')
    tr_elements = soup.select("table.type2 > tr[onmouseover='mouseOver(this)']")

    current_date_time_set = set() # 날짜 데이터를 모두 set에 넣음 -> hash값으로 변해서 집합들 간 비교가 쉬워짐
    # for문 돌면서 초기화되는 거 막기 위해 리스트 생성
    temp_total_data_list = [] # 여기에 놓는 이유: 페이지 구분 없이 모든 row를 하나의 페이지에 놓기 위함
    for e in tr_elements: # 하나의 테이블 행에서
        td_elements = e.select("td")
        data_list = [] # 하나의 row에 있는 td들을 하나의 변수로 관리하기 -> list
        for i, td_e in enumerate(td_elements): # td_e를 가져온 뒤
            data = td_e.text.strip()
            if data == "":
                break # td element에 대해서 for문 도는 거 멈춤

            if i != 0:
                data_list.append(
                    int(data.replace(",", ""))
                )
            else:
                # i = 0(날짜데이터)를 넣는다.
                data = datetime.strptime(data, "%Y.%m.%d")
                current_date_time_set.add(data) # td_e를 돌면서 text 가져오기
                data_list.append(data) # strip(): row 밑에있는 데이터를 하나로 모아서 출력할 때, 양 사이드에 있는 빈칸 등을 깔끔하게 처리

        if len(data_list) > 0: # 데이터가 비어있지 않다면
            temp_total_data_list.append(data_list)
        else:
            break

    if prev_date_time_set == current_date_time_set:
        print("끝났다", page_number)
        break # 모든 tr element 하나씩 도는 거 중단
    else:
        for data in temp_total_data_list:
            total_data_list.append(data)
        prev_date_time_set = current_date_time_set

#    last_date_time = datetime.strptime(df.iloc[:-1]['날짜'], "%Y.%m.%d")
#    if last_date_time in current_date_time_set:
#        break

    time.sleep(random.randint(1,3))
    page_number += 1
    if page_number == 3:
        break


df = pd.DataFrame(total_data_list, columns=['날짜','종가','전일비','시가','고가','저가','거래량'])
df.set_index('날짜')
df = df.iloc[::-1].reset_index(drop=True)



new_total_data_list = []
for data in total_data_list:
    if data[0] > last_date_time: # 크다는 것 = 더 최신 데이터
        new_total_data_list.append(data)

new_df = pd.DataFrame(new_total_data_list, columns=df.columns)

df = pd.concat([df, new_df])

df.to_csv("samsung.csv") # pd.read_csv('samsung.csv', index_col=0)