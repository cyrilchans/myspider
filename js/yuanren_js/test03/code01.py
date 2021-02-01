import requests
import re
from collections import Counter
lists = []

def plan_spider():
    headers = {
        'Host': 'match.yuanrenxue.com',
        'Connection': 'keep-alive',
        'Accept': 'application/json,text/javascript,*/*;q=0.01',
        'User-Agent': 'Mozilla/5.0(WindowsNT10.0;Win64;x64)AppleWebKit/537.36(KHTML,likeGecko)Chrome/86.0.4240.198Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
        'Referer': 'http//match.yuanrenxue.com/match/3',
        'Accept-Encoding': 'gzip,deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
    }
    url = 'http://match.yuanrenxue.com/logo'
    return url, headers

def get_session_id():
    url, headers = plan_spider()
    session = requests.session()
    session.headers = headers
    id = ''.join(re.findall(r'sessionid=(.{32})', str(session.post(url=url).cookies)))
    return id, headers

def start_spider(url, id, headers):
    headers1 = {'Cookie': f'sessionid={id}', 'User-Agent': 'yuanrenxue.project'}
    headers.update(headers1)
    session = requests.session()
    session.headers = headers
    texts = session.get(url)
    deal_date(texts.json())

def deal_date(date):
    text = date['data']
    for index in text:
        lists.append(index['value'])

def count_num():
    # 使用collection.Counter统计
    count = Counter(lists)
    nums = count.most_common()
    print(nums)
    # #使用max计算次数最多
    # print(max(lists, key=lists.count))

def run():
    for index in range(1, 6):
        id, headers = get_session_id()
        url = f'http://match.yuanrenxue.com/api/match/3?page={index}'
        start_spider(url, id, headers)
    count_num()

if __name__ == '__main__':
    run()
