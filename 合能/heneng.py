import requests
import hashlib
import json
import re
import time
from pymongo import MongoClient

'''解析js'''
def parse():
    headers = {
      'Content-Type': 'application/json;charset=UTF-8',
      'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'
    }

    url = 'http://vendor.heneng.cn:16791/api/gwc'
    for index in range(1, 4):
        i = str(int(time.time()*1000))
        c = '{"action":"P_SUP_Bid_GetNotice","p1":"","p2":"",' \
            f'"p3":{index},"p4":20,"p5":"","p6":"-1","p7":""}}'
        strs = c + str(i) + "HNSUP.2018._.123"
        m = hashlib.md5()
        b = strs.encode('utf-8')
        m.update(b)
        a = m.hexdigest()
        data = {'ak': a,
                'i': str(i),
                'payload': c}

        response = requests.post(url=url, headers=headers, data=json.dumps(data))
        text = json.loads(response.text)
        parse_page(text['data'])


'''提取内容'''
def parse_page(text):
    for index in text:
        item = {}
        item['name'] = '合能集团'
        item['source_url'] = f'http://vendor.heneng.cn:16790/bid_notice/{index["noticeid"]}-{index["purchasematterid"]}'
        item['purchase_thing'] = index['condition']
        item['pub_name'] = ''.join(re.findall(r'\d+-\d+-\d{2}', index['publishdate']))
        item['deadline'] = ''.join(re.findall(r'\d+-\d+-\d{2}', index['signenddate']))
        item['project_name'] = index['noticetitle']
        print(item)
        save_mongo(item)


'''保存在Mongodb,并做增量处理'''
def save_mongo(item):
    conn = MongoClient(host='localhost', port=27017)['database']['collection']
    count = conn.find({'source_url': item['source_url']}).count()
    if count == 0:
        conn.insert(item)
    else:
        print('已存在')


def run():
    parse()


if __name__ == '__main__':
    run()



