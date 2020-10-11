import scrapy
from Testchen.items import TestchenItem
import re
from scrapy import cmdline, selector
import json

class XinjiangSpider(scrapy.Spider):
    name = 'xinjiang'

    def start_requests(self):
        url = 'http://zwfw.xinjiang.gov.cn/inteligentsearch/rest/inteligentSearch/getFullTextData'
        # FormRequest 是Scrapy发送POST请求的方法
        yield scrapy.Request(
            method="POST",
            url = url,
            body='{"token":"","pn":3100,"rn":10,"sdt":"","edt":"","wd":"","inc_wd":"","exc_wd":"","fields":"title,projectnum","cnum":"005","sort":"{\\"infodate\\":\\"0\\"}","ssort":"title","cl":200,"terminal":"","condition":[{"fieldName":"categorynum","isLike":true,"likeType":2,"equal":"001001001"}],"time":null,"highlights":"title","statistics":null,"unionCondition":null,"accuracy":"100","noParticiple":"0","searchRange":null,"isBusiness":1}',

            callback = self.parse
        )

    def parse(self, response, **kwargs):
        print(response.text)
        paydata = json.loads(response.text)
        data = paydata['result']
        data1 = data['records']
        for i in data1:
            sourceUrl = "http://zwfw.xinjiang.gov.cn/xinjiangggzy" + i['linkurl']
            yield scrapy.Request(sourceUrl,meta={'sourceUrl':sourceUrl}, callback=self.parse2)

        # if 'num' in response.meta:
        #     x = int(response.meta['num'])
        # else:
        #     x = 1
        # if x < 10:
        #     x = x + 1
        #     z = (x-1)*10
        #     z = str(z)
        #     url = 'http://zwfw.xinjiang.gov.cn/inteligentsearch/rest/inteligentSearch/getFullTextData'
        #     # FormRequest 是Scrapy发送POST请求的方法
        #     yield scrapy.FormRequest(
        #         method="POST",
        #         url=url,
        #         body='{"token":"","pn":%s,"rn":10,"sdt":"","edt":"","wd":"","inc_wd":"","exc_wd":"","fields":"title,projectnum","cnum":"005","sort":"{\\"infodate\\":\\"0\\"}","ssort":"title","cl":200,"terminal":"","condition":[{"fieldName":"categorynum","isLike":true,"likeType":2,"equal":"001001001"}],"time":null,"highlights":"title","statistics":null,"unionCondition":null,"accuracy":"100","noParticiple":"0","searchRange":null,"isBusiness":1}'%z,
        #         callback=self.parse,meta={'num': str(x)}
        #     )


    def parse2(self, response):
        item = TestchenItem()
        sourceUrl = response.request.meta['sourceUrl']
        item['sourceUrl'] = sourceUrl
        print(item)


if __name__ == '__main__':
    cmdline.execute("scrapy crawl xinjiang".split())