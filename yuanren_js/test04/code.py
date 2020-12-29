# -*- coding: utf-8 -*-
import requests
import base64
from lxml.html import etree
url = 'http://match.yuanrenxue.com/api/match/4?page=2'
headers = {
'Accept':'application/json,text/javascript,*/*;q=0.01',
'Accept-Encoding':'gzip,deflate',
'Accept-Language':'zh-CN,zh;q=0.9',
'Cache-Control':'no-cache',
'Connection':'keep-alive',
'Host': 'match.yuanrenxue.com',
'Pragma': 'no-cache',
'Referer': 'http//match.yuanrenxue.com/match/4',
'User-Agent': 'Mozilla/5.0(WindowsNT10.0;Win64;x64)AppleWebKit/537.36(KHTML,likeGecko)Chrome/87.0.4280.88Safari/537.36',
'X-Requested-With': 'XMLHttpRequest',
}
response = requests.get(url, headers=headers)
text = response.json()['info']
print(text)
etree = etree.HTML(text)
a = ''.join(etree.xpath('//img/@src')[0].split('data:image/png;base64,')[1:])
print(a)
b = base64.b64decode(a)
print(b)