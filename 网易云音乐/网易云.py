'''
    最后测试于2020.11.21
    只限于搜索和免费
'''

import random
import requests
from Crypto.Cipher import AES
from binascii import hexlify
import json
import base64
import re
'''解决https报错'''
import urllib3
urllib3.disable_warnings()


class WangYiYun:

    def __init__(self):
        self.headers = {
            'Accept': '*/*',
            'Accept-Encoding': 'gzip,deflate,sdch',
            'Accept-Language': 'zh-CN,zh;q=0.8,gl;q=0.6,zh-TW;q=0.4',
            'Connection': 'keep-alive',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Host': 'music.163.com',
            'Referer': 'http://music.163.com/search/',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
        }
        self.key = '0CoJUm6Qyw8W8jud'
        self.iv = b'0102030405060708'
    # 随机值

    def get_random(self):
        str = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
        random_str = ''
        for i in range(16):
            index = random.randint(0, len(str) - 1)
            random_str += str[index]
        return random_str

    def aes_encrypt(self, text, key):
        pad = 16 - len(text) % 16
        text = text + chr(2) * pad
        encryptor = AES.new(key.encode(), AES.MODE_CBC, self.iv)
        encryptor_str = encryptor.encrypt(text.encode())
        result_str = base64.b64encode(encryptor_str).decode()
        return result_str

    def get_params(self, text, random_str):
        first_aes = self.aes_encrypt(text, key=self.key)
        second_aes = self.aes_encrypt(first_aes, random_str)
        return second_aes

    def get_encSeckey(self, text):
        pub_key = '010001'
        modulus = '00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7'
        text = text[::-1]
        result = pow(int(hexlify(text.encode()), 16), int(pub_key, 16), int(modulus, 16))
        return format(result, 'x').zfill(131)

    def get_url(self, url, params, encSeckey):
        response = requests.post(url=url,
                                 headers=self.headers,
                                 data={'params': params, 'encSecKey':encSeckey},
                                 verify=False)
        text = response.json()
        if 'v1?csrf_token=' not in url:
            self.parse_text(text)
        else:
            self.download_text(text)

    def parse_text(self,text):
        html = text['result']['songs']
        for index in html:
            item = {}
            item['歌名'] = index['name']
            item['ID'] = str(index['id'])
            item['歌链接'] = 'https://music.163.com/#/song?id='+ str(index['id'])
            text = str(index['ar'])
            item['演唱者'] = ''.join(re.findall(r"'name': '(.*?)'", text))
            print(item)

    def download_text(self, text):
        html = str(text['data'])
        url = ''.join(re.findall(r"'url': '(.*?)'", html))
        name = input('请输入保存名字')
        with open(f'{name}.m4a', 'wb') as f:
            try:
                response = requests.get(url, timeout=10)
            except requests.exceptions.ConnectTimeout:
                response = requests.get(url, timeout=10)
            f.write(response.content)

    def search(self):
        url = 'https://music.163.com/weapi/cloudsearch/get/web?csrf_token='
        song = input('请输入搜索词\n')
        text = {"hlpretag": "<span class=s-fc7>", "hlposttag": "</span>", "s": song, "type": "1", "offset": "0","total": "true", "limit": "30", "csrf_token": ""}
        text = json.dumps(text)
        random = self.get_random()
        params = self.get_params(text, random)
        encSeckey = self.get_encSeckey(random)
        self.get_url(url, params, encSeckey)

    def download(self):
        url = 'https://music.163.com/weapi/song/enhance/player/url/v1?csrf_token=2d598b9bf6c23f248d4bc046158747c4'
        id = input('请输入歌名id\n')
        id = '['+id+']'
        text = {"ids": id, "level": "standard", "encodeType": "aac", "csrf_token": ""}
        text = json.dumps(text)
        random = self.get_random()
        params = self.get_params(text, random)
        encSeckey = self.get_encSeckey(random)
        self.get_url(url, params, encSeckey)

    def today_random(self):
        pass

    def run(self):
        while True:
            num = input('请输入操作 1.搜索歌单 2.今日随机听 3.下载\n')
            self.today_random() if num == '2' else self.search() if num == '1' else self.download()



def main():
    wangyiyun = WangYiYun()
    wangyiyun.run()


if __name__ == '__main__':
    main()