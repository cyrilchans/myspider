import requests as req
import hashlib as hash
import random
import time

'''
    最后测试2020.11.15
    简单中文翻英文
'''



url = "http://fanyi.youdao.com/translate_o?smartresult=dict&smartresult=rule/"

def get_md5(string):
    string = string.encode('utf8')
    md5 = hash.md5(string).hexdigest()
    return md5

def yd(string):
    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
                      "AppleWebKit/537.36 (KHTML, like Gecko)"
                      "Chrome/80.0.3987.116 Safari/537.36",
        "Referer": "http://fanyi.youdao.com/",
        "Cookie": 'OUTFOX_SEARCH_USER_ID_NCOO=1586645183.0409322; OUTFOX_SEARCH_USER_ID="-732657987@10.169.0.102"; JSESSIONID=aaa8dN2TMu7y9cbwKPvxx; ___rl__test__cookies=1605611408897',

    }
    '''根据js格式改写，模拟随机生成方式'''
    ts = str(int(time.time() * 1000))
    salt = ts + str(random.randint(0, 9))
    sign = get_md5("fanyideskweb" + string + salt + "]BjuETDhU)zqSxf-=B#7m")
    version = "5.0 (Windows NT 10.0; Win64; x64) " \
              "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.116 Safari/537.36"
    bv = get_md5(version)

    datas = {
        "i": string,
        "from": "AUTO",
        "to": "AUTO",
        "smartresult": "dict",
        "client": "fanyideskweb",
        "salt": salt,
        "sign": sign,
        "ts": ts,
        "bv": bv,
        "doctype": "json",
        "version": "2.1",
        "keyfrom": "fanyi.web",
        "action": "FY_BY_CLICKBUTTION",
    }
    r = req.post(url=url, headers=header, data=datas)
    text = r.json()
    print(text['translateResult'][0][0]['tgt'])


def main():
    while 1:
        string = input("请输入你要翻译的单词：\n")
        yd(string)


if __name__ == '__main__':
    main()