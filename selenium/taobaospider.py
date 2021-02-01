from selenium import webdriver
import time
from lxml.html import etree

class SapiderTaobao:
    def __init__(self):
        self.path = r'C:\Users\15220\Desktop\auto_Test\chromedriver.exe'

    def webdriver_clear(self):
        option = webdriver.ChromeOptions()
        driver = webdriver.Chrome(self.path, chrome_options=option)
        # 跳过阿里滑动验证码对selenium的校验
        driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source": '''
                   Object.defineProperty(navigator, 'webdriver', {
                     get: () => undefined
                   })
                 '''
        })
        # 设置全屏
        driver.maximize_window()
        return driver

    def get_url(self, driver):
        url = 'https://login.taobao.com/member/login.jhtml?spm=a21bo.2017.754894437.1.607811d9UWXkLt&f=top&redirect' \
              'URL=https%3A%2F%2Fwww.taobao.com%2F%3Fspm%3Da1z02.1.1581860521.1.Ocw83k'
        driver.get(url)
        self.login_search_deal(driver)

    def login_search_deal(self, driver):
        # 登录
        num = '输入你的登陆账号'
        for index in num:
            driver.find_element_by_xpath('//input[@placeholder="会员名/邮箱/手机号"]').send_keys(f'{index}')
        ps = '输入你的密码'
        for indexs in ps:
            driver.find_element_by_xpath('//input[@placeholder="请输入登录密码"]').send_keys(f'{indexs}')
        driver.find_element_by_xpath('//div[@class="fm-btn"]/button').click()
        cook = driver.get_cookies()
        time.sleep(4)
        url = 'https://www.taobao.com/?spm=a1z02.1.1581860521.1.Ocw83k'
        driver.add_cookie(cook[0])
        driver.get(url)
        time.sleep(1)
        # 搜索大衣商品
        driver.find_element_by_id('q').send_keys('大衣')
        time.sleep(1)
        driver.find_element_by_xpath('//button[@class="btn-search tb-bg"]').click()
        time.sleep(1)
        text = driver.execute_script("return document.documentElement.outerHTML")
        # 生产html文本
        parse_test = etree.HTML(text)
        html = parse_test.xpath('//div[@class="grid g-clearfix"]/div[@class="items"][1]/div')
        # 处理文本
        for index2 in html:
            item = {}
            item['name'] = index2.xpath('.//div[@class="pic-box J_MouseEneterLeave J_PicBox"]//div[@class="pic"]/a/img/@alt')
            item['url'] = index2.xpath('.//div[@class="row row-2 title"]/a/@href')[0]
            if 'http:' not in item['url']:
                item['url'] = 'https://' + item['url']
            item['price'] = index2.xpath('.//div[@class="row row-2 title"]/a/@trace-price')[0]
            print(item)

        time.sleep(100000)



def run():
    tb = SapiderTaobao()
    driver = tb.webdriver_clear()
    tb.get_url(driver)


if __name__ == '__main__':
    run()
