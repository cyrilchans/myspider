import requests
import time
import execjs

headers = {
    'User-Agent': 'yuanrenxue.project'
}

def get_js():
    with open('test.js', 'r', encoding='utf-8') as f:
        a = f.read()
    js = execjs.compile(a).call('get_t_value')
    print(js)
    return js

def get_url(keys):
    count = []
    for index in range(1, 6):
        url = 'http://match.yuanrenxue.com/api/match/1?' \
               f'page={index}&m={keys}%E4%B8%A8' \
               f''
        print(url)
        response = requests.get(url=url, headers=headers)
        print(response.json())
    #     text = response.json()['data']
    #
    #     for index in text:
    #         case = index['value']
    #         count.append(case)
    # get_date(count)

def get_date(text):
    avage = sum(text)/len(text)
    print(avage)


def run():
    keys = get_js()
    get_url(keys)

def main():
    run()


if __name__ == '__main__':
    main()
