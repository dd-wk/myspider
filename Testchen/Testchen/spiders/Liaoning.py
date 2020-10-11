from Testchen.items import TestchenItem
import scrapy
import re
from scrapy import cmdline, selector
import json

class LiaoningSpider(scrapy.Spider):
    name = 'Liaoning'

    def start_requests(self):
        url = 'http://www.ccgp-liaoning.gov.cn/portalindex.do?method=getPubInfoList&t_k=null&tk=0.3670561851680092'
        # FormRequest 是Scrapy发送POST请求的方法
        yield scrapy.FormRequest(
            url = url,
            formdata={'current': '1',
                      'rowCount': '20',
                      'searchPhrase':'',
                      'infoTypeCode': '1001',
                      'privateOrCity': '1'},
            callback = self.parse
        )

    def parse(self, response, **kwargs):
        # print(response.text)
        paydata = json.loads(response.text)

        data = paydata['rows']

        for i in data:

            sourceUrl ='http://www.ccgp-liaoning.gov.cn/portalindex.do?method=getPubInfoViewOpenNew&infoId=' + i['id']
            yield scrapy.Request(sourceUrl,meta={'sourceUrl':sourceUrl}, callback=self.parse2)

        if 'num' in response.meta:
            x = int(response.meta['num'])
        else:
            x = 1
        if x < 36:
            x = x + 1

            url = 'http://www.ccgp-liaoning.gov.cn/portalindex.do?method=getPubInfoList&t_k=null&tk=0.3670561851680092'
            # FormRequest 是Scrapy发送POST请求的方法
            yield scrapy.FormRequest(
                url=url,
                formdata={'current': str(x),
                          'rowCount': '20',
                          'searchPhrase': '',
                          'infoTypeCode': '1001',
                          'privateOrCity': '1'},
                callback=self.parse,meta={'num': str(x)}
            )



    def parse2(self, response):
            item = TestchenItem()
            sourceUrl = response.request.meta['sourceUrl']
            item['sourceUrl'] = sourceUrl
            # content = response.xpath('//text()').getall()
            # item['text'] = content
            print(item)





if __name__ == '__main__':
    cmdline.execute("scrapy crawl Liaoning".split())