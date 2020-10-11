import json
from Testchen.items import TestchenItem
import scrapy
import re
from scrapy import cmdline, selector


class JiangsuSpider(scrapy.Spider):
    name = 'jiangsu'
    # allowed_domains = ['jstba.org.cn']
    # start_urls = ['http://jstba.org.cn/']

    def start_requests(self):
        url = 'http://www.jstba.org.cn/Home/NewsList.aspx?newstype=1'
        # FormRequest 是Scrapy发送POST请求的方法
        yield scrapy.FormRequest(
            url = url,
            formdata={'__VIEWSTATE': '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',
                      '__VIEWSTATEGENERATOR': '3969332F',
                      '__EVENTTARGET': 'AspNetPager1',
                      '__EVENTARGUMENT': '1',
                      '__EVENTVALIDATION': '/ wEWEgL4ioGkBQKvruvcAgKx6Pr3CQL + is7lCAKR + t2ICwLN5PyLDwKln / PuCgKpzaSICQKpzaCICQKpzZyICQKpzZiICQKpzZSICQKpzZCICQKpzYyICQKpzciLCQKpzcSLCQLPjMvfDgLPjMvfDrHmRJTqQL6zyLEfcUZ74laodd8i',
                      'tempTB':'',
                      'ctl05$tempTB':'',
                      'tbSearchTitle':'',
                      'AspNetPager1_input':'15'
                      },
            callback = self.parse
        )




    def parse(self, response):
        print(response.text)
        a = response.xpath('//div[@id="listContent"]/div[@style]/div[2]/div[@style]')
        for node in a:
            url = node.xpath('./div[@style]/a/@href').extract()
            for c in url:
                sourceUrl = 'http://www.jstba.org.cn/Home/' + c
                yield scrapy.Request(sourceUrl, meta={'sourceUrl': sourceUrl}, callback=self.parse2)



        if 'num' in response.meta:
            x = int(response.meta['num'])
        else:
            x = 1
        if x < 2:
            x = x + 1

            url = 'http://www.jstba.org.cn/Home/NewsList.aspx?newstype=1'
            # FormRequest 是Scrapy发送POST请求的方法
            yield scrapy.FormRequest(
                url=url,
                formdata={
                    '__VIEWSTATE': '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',
                    '__VIEWSTATEGENERATOR': '3969332F',
                    '__EVENTTARGET': 'AspNetPager1',
                    '__EVENTARGUMENT': str(x),
                    '__EVENTVALIDATION': '/ wEWEgL4ioGkBQKvruvcAgKx6Pr3CQL + is7lCAKR + t2ICwLN5PyLDwKln / PuCgKpzaSICQKpzaCICQKpzZyICQKpzZiICQKpzZSICQKpzZCICQKpzYyICQKpzciLCQKpzcSLCQLPjMvfDgLPjMvfDrHmRJTqQL6zyLEfcUZ74laodd8i',
                    'tempTB': '',
                    'ctl05$tempTB': '',
                    'tbSearchTitle': '',
                    'AspNetPager1_input': '15'
                    },
                callback=self.parse,meta={'num': str(x)}
            )

    def parse2(self, response):
        item = TestchenItem()
        sourceUrl = response.request.meta['sourceUrl']

        print(sourceUrl)









if __name__ == '__main__':
    cmdline.execute("scrapy crawl jiangsu".split())















