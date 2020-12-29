import execjs
import requests

with open('code.js', 'r', encoding='utf-8') as f:
    a = f.read()
ex = execjs.compile(a).call('get_value')
print(ex)

headers = {
    'Cookie': ex
}
print(headers)
url = 'http://match.yuanrenxue.com/api/match/2?page=3'
response = requests.get(url, headers=headers)
print(response.text)
