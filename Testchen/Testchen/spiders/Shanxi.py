from Testchen.items import TestchenItem
import scrapy
import re
from scrapy import cmdline, selector
from lxml.html import etree
class ShanxiSpider(scrapy.Spider):
    name = 'Shanxi'
    # allowed_domains = ['ccgp-shanxi.gov.cn']
    # start_urls = ['http://www.ccgp-shanxi.gov.cn/view.php?app=&type=&nav=100&page=1']

    # def parse(self, response):
    #     a = response.xpath('//div[@class="zt3"]/table')
    #     for node in a:
    #         url = node.xpath('.//tr/td/a/@href').extract()
    #         for c in url:
    #             sourceUrl = 'http://ccgp-shanxi.gov.cn/' + c
    #             yield scrapy.Request(sourceUrl, meta={'sourceUrl':sourceUrl}, callback=self.parse2)
    #
    #
    #     if 'num' in response.meta:
    #         x = int(response.meta['num'])
    #     else:
    #         x = 1
    #     if x < 2:
    #         x = x + 1
    #         # print(x)
    #         url = "http://www.ccgp-shanxi.gov.cn/view.php?app=&type=&nav=100&page="+str(x)
    #         print(url)
    #         yield scrapy.Request(url, meta={'num': str(x)}, callback=self.parse)
    #
    # def parse2(self, response):
    #     item = TestchenItem()
    #     sourceUrl = response.request.meta['sourceUrl']
    #     print(sourceUrl)
    #     a = ''
    #     nums = '无'
    # start_urls = 'http://sczy.spprec.com:118/sczw/jyfwpt/005001/005001001/MoreInfo.aspx?CategoryNum=005001001'

    def start_requests(self):
        headers = {
            'Host': 'sczy.spprec.com:118',
            'Pragma': 'no-cache',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.90 Safari/537.36'
        }
        url = 'http://sczy.spprec.com:118/sczw/jyfwpt/005001/005001001/MoreInfo.aspx?CategoryNum=005001001'
        # FormRequest 是Scrapy发送POST请求的方法
        yield scrapy.Request(url,callback=self.parse,headers = headers)


    def parse(self, response, **kwargs):
        # print(response.text)
        __VIEWSTATE = re.findall('id="__VIEWSTATE" value="(.*?)" />', response.text)
        __VIEWSTATE = __VIEWSTATE[0] if __VIEWSTATE else ''
        # html = etree.HTML(response.text)
        a = response.xpath('//td[@id="MoreInfoList1_tdcontent"]/table')
        for node in a:
            url = node.xpath('.//tr/td/a/@href').getall()
            for c in url:
                c = c.replace('amp;','')
                print(c)
                sourceUrl = 'http://sczy.spprec.com:118' + c
                yield scrapy.Request(sourceUrl, meta={'sourceUrl':sourceUrl}, callback=self.parse2)

        if 'num' in response.meta:
            x = int(response.meta['num'])
        else:
            x = 1
        if x < 3:
            x = x + 1
            url = "http://sczy.spprec.com:118/sczw/jyfwpt/005001/005001001/MoreInfo.aspx?CategoryNum=005001001"
            formdata = {
                '__VIEWSTATE': __VIEWSTATE,
                '__VIEWSTATEGENERATOR': 'CB896DD0',
                '__EVENTTARGET': 'MoreInfoList1$Pager',
                '__EVENTARGUMENT': str(x)
            }
            yield scrapy.FormRequest(
                url=url,
                formdata=formdata,
                callback=self.parse, meta={'num': str(x)}
            )

    def parse2(self, response):
        item = TestchenItem()
        sourceUrl = response.request.meta['sourceUrl']
        item['sourceUrl'] = sourceUrl
        print(item)
        print('四川')


















if __name__ == '__main__':
    cmdline.execute("scrapy crawl Shanxi".split())