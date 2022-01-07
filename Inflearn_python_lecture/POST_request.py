import json
import pandas as pd
import requests

data_dict = {
    "dmSearch":{
        "tmpV40":"100000000",
        "tmpV41":"1",
        "tmpV30":"20210706",
        "tmpV31":"20220106",
        "tmpV37":"0",
        "tmpV5":"",
        "tmpV7":"1",
        "tmpV3":"",
        "tmpV11":"",
        "tmpV19":"Y",
        "OBJ_NM":"STATFND0100100030BO"
    }
}

data_dict_json = json.dumps(data_dict) # jsonlize (dict -> string)

headers = {
    'Content-Type': 'application/json; charset=UTF-8',
    'Host': 'freesis.kofia.or.kr',
    'Origin': 'http://freesis.kofia.or.kr',
    'Referer': 'http://freesis.kofia.or.kr/stat/FreeSIS.do?parentDivId=MSIS40100000000000&serviceId=STATFND0100100030',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest'
}

url = 'http://freesis.kofia.or.kr/meta/getMetaDataList.do'

res = requests.post(url, data=data_dict_json, headers=headers)
res.status_code

data_list = res.json()['ds1']
df = pd.DataFrame(data_list)

