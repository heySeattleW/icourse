import scrapy
from icourse.items import IcourseItem
from icourse.settings import USER_AGENT_LIST
import re
import requests
import random
import time


class ICourseSpider(scrapy.Spider):

    name = 'ICourseSpider'
    # 允许访问的域
    allowed_domains = ['icourse8.com']
    # 爬取的地址
    start_urls = ['http://www.icourse8.com/']

    # 浏览器登录后得到的cookie，也就是刚才复制的字符串
    # cookie_str = r'_cliid=UjXEFI0xRWOMURij; _lastEnterDay=2018-12-26; _siteStatId=cb4f38e5-c9d6-486d-88bf-e0f4fca11e8c; _siteStatDay=20181226; _siteStatRedirectUv=redirectUv_16779352; _siteStatVisitorType=visitorType_16779352; lastLoginTime16779352146=2018-12-26; loginMemberCacct=jf16072768; loginMemberAcct=jaychou114118; _FSESSIONID=86tUGBB-LS0OeHkl; tabSwitch=0; _pdDay_285_0=20181226; _pdDay_256_0=20181226; _pdDay_294_0=20181226; _pdDay_368_0=20181226; _pdDay_743_0=20181226; _pdDay_877_0=20181226; _siteStatVisit=visit_16779352; _siteStatVisitTime=1545835071860'
    # cookie_str = r'_cliid=UjXEFI0xRWOMURij; _siteStatVisitorType=visitorType_16779352; loginMemberCacct=jf16072768; loginMemberAcct=jaychou114118; _lastEnterDay=2018-12-28; _siteStatId=9ff92641-8d27-42de-bebc-ecf185c8351a; _siteStatDay=20181228; _siteStatRedirectUv=redirectUv_16779352; lastLoginTime16779352146=2018-12-28; _FSESSIONID=86tAp6_gFBQyQUAc; tabSwitch=0; _pdDay_877_0=20181228; _siteStatVisit=visit_16779352; _siteStatVisitTime=1546000679031'
    # cookie_str = r'loginMemberCacct=jf16072768; loginMemberAcct=jaychou114118; _cliid=FIXwhWG8odivaHbr; _siteStatVisitorType=visitorType_16779352; _cliid=-uQIf7mCX27gV5s4; _lastEnterDay=2018-12-29; _loginBeforeFiveMin=true; _siteStatId=2514a8a0-b9ae-4770-86de-162f57059bc7; _siteStatDay=20181229; _siteStatRedirectUv=redirectUv_16779352; _siteStatVisit=visit_16779352; _siteStatReVisit=reVisit_16779352; lastLoginTime16779352146=2018-12-29; _FSESSIONID=KXFYbWWMhYWjHB1B; _siteStatVisitTime=1546053931045'
    cookie_str = r'loginMemberCacct=jf16072768; loginMemberAcct=jaychou114118; _cliid=FIXwhWG8odivaHbr; _siteStatVisitorType=visitorType_16779352; _cliid=-uQIf7mCX27gV5s4; _lastEnterDay=2018-12-29; _siteStatId=2514a8a0-b9ae-4770-86de-162f57059bc7; _siteStatDay=20181229; _siteStatRedirectUv=redirectUv_16779352; lastLoginTime16779352146=2018-12-29; _FSESSIONID=KXFYbWWMhYWjHB1B'
    # 设置请求头
    headers = {"User-Agent": ''}
    # 把cookie字符串处理成字典，以便接下来使用
    cookies = {}
    for line in cookie_str.split(';'):
        key, value = line.split('=', 1)
        cookies[key] = value

    # 爬取方法

    def parse(self, response):
        # 实例化容器存放数据
        in_html_code_pattern = '<span>([a-zA-Z0-9]{4})</span>'
        in_html_url_pattern = 'https://pan.baidu.com/s/[\s\S]*?</span>'
        item = IcourseItem()
        for course in response.xpath('//div[@topclassname="productListTopIcon"]'):
            item['video_title'] = course.xpath('.//a[@class="fk-productName"]/text()').extract()[0].strip()
            item['video_img'] = course.xpath('.//@src').extract()[0].strip()
            item['video_desc'] = course.xpath('.//span[@class="propValue   fk-prop-other"]/text()').extract()[0].strip()
            item['video_time'] = course.xpath('.//span[@class="propValue   fk-prop-other"]/text()').extract()[1].strip()
            item['video_type'] = course.xpath('.//span[@class="propValue   fk-prop-other"]/text()').extract()[2].strip()
            # 下面两个属性需要进入到页面内部
            url_list = []
            url_list.append(self.start_urls[0] + course.xpath('.//@href').extract()[0].strip())
            for url_in in url_list:
                # 在发送get请求时带上请求头和cookies
                rand_use = random.choice(USER_AGENT_LIST)
                self.headers['User-Agent'] = rand_use
                resp_in = requests.get(url_in, headers=self.headers, cookies=self.cookies)
                # 拿到网页内容
                content_in = resp_in.content.decode('utf-8')
                content_in = content_in.replace('\r\n', '')
                pan_url = re.findall(in_html_url_pattern, content_in)
                video_code = re.findall(in_html_code_pattern, content_in)
                item['pan_url'] = pan_url[0][:-7]
                item['video_code'] = video_code[0]
            yield item
            # url跟进开始
            # 获取下一页的url信息
            time.sleep(3)
            url = response.xpath('//a[@hidefocus="true"]/@href').extract()[-6]
            if url:
                # 将信息组合成下一页的url
                page = 'http://www.icourse8.com' + url
                # 返回url
                yield scrapy.Request(page, callback=self.parse)
            # url跟进结束
