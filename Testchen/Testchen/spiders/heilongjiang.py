import json
import scrapy
from Testchen.items import TestchenItem
import re
from scrapy import cmdline, selector
import time



class HeilongjiangSpider(scrapy.Spider):
    name = 'heilongjiang'
    start_urls = ['http://www.hljggzyjyw.gov.cn/portal/trade/tradezfcg?cid=16&pageNo=1&type=1&notice_name=']

    def parse(self, response, **kwargs):
        # print(response.text)
        a = response.xpath('//div[@class="right_box"]/ul')
        for node in a:
            url = node.xpath('./li/a/@href').extract()
            for c in url:
                c = c.replace('amp;','')
                sourceUrl = 'http://www.hljggzyjyw.gov.cn' + c
                yield scrapy.Request(sourceUrl, meta={'sourceUrl': sourceUrl}, callback=self.parse2)


        if 'num' in response.meta:
            x = int(response.meta['num'])
        else:
            x = 1
        if x < 143:
            x = x + 1
            url ="http://www.hljggzyjyw.gov.cn/portal/trade/tradezfcg?cid=16&pageNo=" + str(x) + "&type=1&notice_name="
            yield scrapy.Request(url,meta={'num':str(x)},callback=self.parse)


    def parse2(self, response):
        item = TestchenItem()
        sourceUrl = response.request.meta['sourceUrl']
        item['sourceUrl'] = sourceUrl
        print(item)




if __name__ == '__main__':
    cmdline.execute("scrapy crawl heilongjiang".split())