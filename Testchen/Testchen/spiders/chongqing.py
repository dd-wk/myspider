import json
import scrapy
from Testchen.items import TestchenItem
import re
from scrapy import cmdline, selector


class ChongqingSpider(scrapy.Spider):
    name = 'chongqing'

    def start_requests(self):
        url = 'https://www.cqggzy.com/interface/rest/inteligentSearch/getFullTextData'
        # FormRequest 是Scrapy发送POST请求的方法
        yield scrapy.Request(
            method="POST",
            url = url,
            body='{"token":"","pn":0,"rn":18,"sdt":"","edt":"","wd":" ","inc_wd":"","exc_wd":"","fields":"title","cnum":"001","sort":"{\\"istop\\":0,\\"ordernum\\":0,\\"webdate\\":0,\\"rowid\\":0}","ssort":"title","cl":200,"terminal":"","condition":[{"fieldName":"categorynum","equal":"014001001","notEqual":null,"equalList":null,"notEqualList":null,"isLike":true,"likeType":2}],"time":null,"highlights":"title","statistics":null,"unionCondition":null,"accuracy":"","noParticiple":"0","searchRange":null,"isBusiness":"1"}',

            callback = self.parse
        )

    def parse(self, response, **kwargs):
        # print(response.text)
        paydata = json.loads(response.text)
        data = paydata['result']
        data1 = data['records']
        for i in data1:
            sourceUrl = "https://www.cqggzy.com/xxhz/014001/014001001/014001001001/20200917/" + i['infoid'] + ".html"
            yield scrapy.Request(sourceUrl,meta={'sourceUrl':sourceUrl}, callback=self.parse2)

        # if 'num' in response.meta:
        #     x = int(response.meta['num'])
        # else:
        #     x = 1
        # if x < 2:
        #     x = x + 1
        #
        #     url = 'http://www.ccgp-shandong.gov.cn/sdgp2017/site/listnew.jsp'
        #     # FormRequest 是Scrapy发送POST请求的方法
        #     yield scrapy.FormRequest(
        #         url=url,
        #         formdata={'subject': '', 'pdate': '', 'kindof': '', 'unitname': '', 'projectname': '',
        #                   'projectcode': '', 'colcode': '0301', 'curpage': str(x), 'grade': 'province', 'firstpage': '1'},
        #         callback=self.parse,meta={'num': str(x)}
        #     )


    def parse2(self, response):
        item = TestchenItem()
        sourceUrl = response.request.meta['sourceUrl']
        item['sourceUrl'] = sourceUrl
        print(item)




if __name__ == '__main__':
    cmdline.execute("scrapy crawl chongqing".split())