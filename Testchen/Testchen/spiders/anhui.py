from Testchen.items import TestchenItem
import scrapy
import re
from scrapy import cmdline, selector

class AnhuiSpider(scrapy.Spider):
    name = 'anhui'
    start_urls = ['http://ggzy.hefei.gov.cn/jyxx/002001/002001001/moreinfo_jyxxgg2.html']

    def parse(self, response, **kwargs):
        a = response.xpath('//ul[@class="ewb-right-item"]')
        for node in a:
            url = node.xpath('./li/a/@href').extract()
            for c in url:
                sourceUrl = "http://ggzy.hefei.gov.cn" + c
                yield scrapy.Request("http://ggzy.hefei.gov.cn" + c, meta={'sourceUrl':sourceUrl}, callback=self.parse2)

        if 'num' in response.meta:
            x = int(response.meta['num'])
        else:
            x = 1
        if x < 50:
            x = x + 1
            url = 'http://ggzy.hefei.gov.cn/jyxx/002001/002001001/' +  str(x) + '.html'
            yield scrapy.Request(url, meta={'num': str(x)}, callback=self.parse)



    def parse2(self, response):
        item = TestchenItem()
        sourceUrl = response.request.meta['sourceUrl']
        item['sourceUrl'] = sourceUrl
        print(item)








if __name__ == '__main__':
    cmdline.execute("scrapy crawl anhui".split())