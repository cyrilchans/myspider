import re

def run_Header(headers):
    header = ''
    for i in headers:
        if i == '\n':
            i = "',\n'"
        header += i
    header = re.sub(':', "': '", header)
    ret = header[2:].replace(' ', '')+'\''
    print(ret[1: -3])

headers = """
Accept: application/json, text/javascript, */*; q=0.01
Accept-Encoding: gzip, deflate
Accept-Language: zh-CN,zh;q=0.9
Cache-Control: no-cache
Connection: keep-alive
Host: match.yuanrenxue.com
Pragma: no-cache
Referer: http://match.yuanrenxue.com/match/4
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36
X-Requested-With: XMLHttpRequest
"""
run = run_Header(headers)

