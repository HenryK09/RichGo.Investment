import requests
import json
import pandas as pd
import re

my_headers = {
    'Referer': 'https://navercomp.wisereport.co.kr/v2/company/c1010001.aspx?cmp_cd=005930',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest'
}

res = requests.get(
    url = 'https://navercomp.wisereport.co.kr/v2/company/ajax/cF1001.aspx?cmp_cd=005930&fin_typ=0&freq_typ=A&encparam=aVYwYzNoeHRBVGEwci9aSnpaWWNMdz09&id=ZTRzQlVCd0',
    # url - encparam 뒤에 코드가 시간이 지나면 변형되어 에러 발생
        re.search("encparam: (.*)", res.text).group(1).strip()[1:-1]
),
    headers = my_headers
)

enc_param_url = "https://navercomp.wisereport.co.kr/v2/company/c1010001.aspx?cmp_cd=005930"

res = requests.get(enc_param_url, headers=my_headers)

"encparam" in res.text

re.search("encparam: .*", res.text).group(0)

re.search("encparam: (.*)", res.text).group(1).strip()

re.search("encparam: (.*)", res.text).group(1).strip()[1:-1]),

data_dict = json.loads(res.text)
data_dict.keys()

json.dumps(data_dict['chartData1'])

data_dict = res.json()

data_dict['chartData1'].keys()

data_dict['chartData1']['categories']

data_dict['chartData1']['title']

df = pd.DataFrame(data_dict['chartData1']['series'])