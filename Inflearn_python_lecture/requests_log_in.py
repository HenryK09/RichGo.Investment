import requests

# requests로 로그인하기
# 로그인 한 상태인지 connection이 계속 유지되어야 함

# 성공사례
my_id_part = "fake_id"

data_dict = {
    'email' : '{}@.gmail.com'.format(my_id_part),
    'password' : 'opentutorials!'
}
data_dict


url = "https://opentutorials.org/auth/login_ajax"

res_s = requests.post(url, data=data_dict)
res.text

# 로그인 connection 확인하게 하는 쿠키, 세션
session = requests.Session() # 세션 정보 기억할 수 있는 환경
res_s = session.post(url, data=data_dict)
res_s.status_code # 200 나왔다고 안심 X

res_s.text # 확인하는 방법

session.get("https://opentutorials.org/")

session.close() # 로그아웃



# 실패사례 - 개인정보보호로 위 방법으로 쉽게 가져오는 경우 잘 없음
user_id = "qughus0934"
data = {
    "s_url": "%2F",
    "user_id": user_id,
    "password": "EAk46yLztUx",
}

c = requests.Session()

res_f = c.post("https://www.ppomppu.co.kr/  , data=data")

user_id in res.text

res_f = c.get("https://www.ppomppu.co.kr/")
user_id in res.text