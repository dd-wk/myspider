import json
import scrapy
from Testchen.items import TestchenItem
import re
from scrapy import cmdline, selector



class JilinSpider(scrapy.Spider):
    name = 'jilin'
    def start_requests(self):
        url = 'http://www.ccgp-jilin.gov.cn/shopHome/morePolicyNews.action'
        # FormRequest 是Scrapy发送POST请求的方法
        yield scrapy.FormRequest(
            url = url,
            formdata={'currentPage': '1',
                      'noticetypeId': '2',
                      'categoryId':'124'
                      },
            callback = self.parse
        )

    def parse(self, response, **kwargs):
        # print(response.text)
        a = response.xpath('//div[@id="list_right"]/ul')
        for node in a:
            url = node.xpath('./li/a/@href').extract()
            for c in url:
                sourceUrl = 'http://www.ccgp-jilin.gov.cn' + c
                yield scrapy.Request(sourceUrl, meta={'sourceUrl': sourceUrl}, callback=self.parse2)

        if 'num' in response.meta:
            x = int(response.meta['num'])
        else:
            x = 1
        if x < 143:
            x = x + 1
            url = 'http://www.ccgp-jilin.gov.cn/shopHome/morePolicyNews.action'
            # FormRequest 是Scrapy发送POST请求的方法
            yield scrapy.FormRequest(
                url=url,
                formdata={'currentPage': str(x),
                          'noticetypeId': '2',
                          'categoryId': '124'
                          },
                callback=self.parse,meta={'num': str(x)}
            )


    def parse2(self, response):
        item = TestchenItem()
        sourceUrl = response.request.meta['sourceUrl']
        item['sourceUrl'] = sourceUrl
        print(item)




if __name__ == '__main__':
    cmdline.execute("scrapy crawl jilin".split())