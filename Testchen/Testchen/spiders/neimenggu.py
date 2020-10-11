import json
import scrapy
from Testchen.items import TestchenItem
import re
from scrapy import cmdline, selector


class NeimengguSpider(scrapy.Spider):
    name = 'neimenggu'
    def start_requests(self):
        url = 'http://www.nmgp.gov.cn/zfcgwslave/web/index.php?r=new-data%2Fanndata'
        # FormRequest 是Scrapy发送POST请求的方法
        yield scrapy.FormRequest(
            url = url,
            formdata={'type_name':'1',
                      'purmet':'1',
                      'annstartdate_S':'',
                      'byf_page': '1',
                      'fun': 'cggg',
                      'page_size': '18',
                      },
            callback = self.parse
        )

    def parse(self, response, **kwargs):
        # print(response.text)
        paydata = json.loads(response.text)
        for i in paydata[0]:
            sourceUrl ='http://www.nmgp.gov.cn/category/cggg?tb_id='+ i['ay_table_tag'] + '&p_id=' + i['wp_mark_id'] + '&type='+ i['type']

            yield scrapy.Request(sourceUrl,meta={'sourceUrl':sourceUrl}, callback=self.parse2)

        if 'num' in response.meta:
            x = int(response.meta['num'])
        else:
            x = 1
        if x < 3:
            x = x + 1

            url = 'http://www.nmgp.gov.cn/zfcgwslave/web/index.php?r=new-data%2Fanndata'
            # FormRequest 是Scrapy发送POST请求的方法
            yield scrapy.FormRequest(
                url=url,
                formdata={'type_name': '1',
                          'purmet': '1',
                          'annstartdate_S': '',
                          'byf_page': str(x),
                          'fun': 'cggg',
                          'page_size': '18',
                          },
                callback=self.parse,meta={'num': str(x)})


    def parse2(self, response):
        item = TestchenItem()
        sourceUrl = response.request.meta['sourceUrl']
        item['sourceUrl'] = sourceUrl
        print(item)




if __name__ == '__main__':
    cmdline.execute("scrapy crawl neimenggu".split())