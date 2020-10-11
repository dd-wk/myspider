import scrapy
import json
import scrapy
import re
from scrapy import cmdline, selector
from Testchen.items import TestchenItem


class XizangSpider(scrapy.Spider):
    name = 'xizang'
    def start_requests(self):
        url = 'http://www.ccgp-xizang.gov.cn/shopHome/morePolicyNews.action?categoryId=124,125'
        # FormRequest 是Scrapy发送POST请求的方法
        yield scrapy.FormRequest(
            url=url,
            formdata={'currentPage': '700',
                      },
            callback=self.parse
        )

    def parse(self, response, **kwargs):
        # print(response.text)
        a = response.xpath('//div[@id="news_div"]/ul/li/div/a')
        for i in a:
            z = i.xpath('.//text()').get()
            # print(z)

            if z.find('中标') >= 0 or z.find('结果') >= 0 or z.find('流标') >= 0 or z.find( '更正') >= 0 or z.find('废标') >= 0 or z.find('合同') >= 0 or z.find('成交') >= 0 or z.find('延长公告') >= 0:
                pass
            else:
                print(z,i.xpath('./@href').get())
                url = i.xpath('./@href').extract()
                for c in url:
                    sourceUrl = 'http://www.ccgp-xizang.gov.cn' + c
                    yield scrapy.Request(sourceUrl, meta={'sourceUrl':sourceUrl}, callback=self.parse2)

        # for node in a:
        #         url = node.xpath('./li//a/@href').extract()
        #     for c in url:
        #         c = c.replace('amp;','')
        #         sourceUrl = 'http://www.ccgp-xizang.gov.cn' + c
        #         yield scrapy.Request(sourceUrl, meta={'sourceUrl':sourceUrl}, callback=self.parse2)


        # if 'num' in response.meta:
        #     x = int(response.meta['num'])
        # else:
        #     x = 1
        # if x < 1500:
        #     x = x + 1
        #     url = 'http://www.ccgp-xizang.gov.cn/shopHome/morePolicyNews.action?categoryId=124,125'
        #     # FormRequest 是Scrapy发送POST请求的方法
        #     yield scrapy.FormRequest(
        #         url=url,
        #         formdata = {'currentPage': str(x),
        #                     },
        #         callback=self.parse, meta={'num': str(x)})




    def parse2(self, response):
        item = TestchenItem()
        sourceUrl = response.request.meta['sourceUrl']
        item['sourceUrl'] =sourceUrl
        print(item)







if __name__ == '__main__':
    cmdline.execute("scrapy crawl xizang".split())