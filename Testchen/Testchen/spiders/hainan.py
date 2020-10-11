import json
import scrapy
import re
from scrapy import cmdline, selector
from Testchen.items import TestchenItem

class HainanSpider(scrapy.Spider):
    name = 'hainan'

    def start_requests(self):
        url = 'https://www.ccgp-hainan.gov.cn/cgw/cgw_list.jsp'
        # FormRequest 是Scrapy发送POST请求的方法
        yield scrapy.FormRequest(
            url=url,
            formdata={'title': '',
                      'bid_type': '101',
                      'proj_number': '',
                      'begindate': '',
                      'enddate': '',
                      'zone': '',
                      'currentPage': '1',
                      },
            callback=self.parse
        )


    def parse(self, response, **kwargs):
        a = response.xpath('//div[@class="index07_07_02"]/ul')
        for node in a:
            url = node.xpath('./li//a/@href').getall()
            for c in url:
                # print(c)
                sourceUrl = 'https://www.ccgp-hainan.gov.cn' + c
                yield scrapy.Request(sourceUrl, meta={'sourceUrl': sourceUrl}, callback=self.parse2)

        # if 'num' in response.meta:
        #     x = int(response.meta['num'])
        # else:
        #     x = 1
        # if x < 1500:
        #     x = x + 1
        #     url = 'https://www.ccgp-hainan.gov.cn/cgw/cgw_list.jsp'
        #     # FormRequest 是Scrapy发送POST请求的方法
        #     yield scrapy.FormRequest(
        #         url=url,
        #         formdata={'title': '',
        #                   'bid_type': '101',
        #                   'proj_number': '',
        #                   'begindate': '',
        #                   'enddate': '',
        #                   'zone': '',
        #                   'currentPage':str(x),
        #                   },
        #         callback=self.parse, meta={'num': str(x)})


    def parse2(self, response):
        item = TestchenItem()
        sourceUrl = response.request.meta['sourceUrl']

        a = ''
        content0 = ''
        content1 = ''
        nums = ''
        content = response.xpath('//div[@id="con_TBAB_1"]')
        for node in content:
            p = node.xpath('./p')
            for d in p:
                text = d.xpath('.//text()').getall()
                text_str = "".join(text).replace("\n", "")
                content0 += text_str + '\n'

        content0 = content0.replace("\xa0", "")
        content0 = content0.replace(" ", "")
        content0 = content0.replace("&nbsp;", "")
        content0 = content0.replace("\u3000", "")
        content0 = content0.replace("\r", "")
        content0 = content0.replace("\t", "")

        content = response.xpath('//div[@id="con_TBAB_1"]')
        for node in content:
            p = node.xpath('.//div')
            for d in p:
                text = d.xpath('.//text()').getall()
                text_str = "".join(text).replace("\n", "")
                content1 += text_str + '\n'

        content1 = content1.replace("\xa0", "")
        content1 = content1.replace(" ", "")
        content1 = content1.replace("&nbsp;", "")
        content1 = content1.replace("\u3000", "")
        content1 = content1.replace("\r", "")
        content1 = content1.replace("\t", "")

        if len(content0) >len(content1):
            a = content0
        else:
            a = content1


        pName = response.xpath('//div[@class="content03"][2]//tr/td[2]/text()').getall()[0]


        entName = response.xpath('//div[@class="content03"][10]//td[2]/text()').getall()[0]


        pAddr = response.xpath('//div[@class="content03"][10]//tr[2]/td[2]/text()').getall()[0]


        pNo = response.xpath('//div[@class="content03"][2]//tr/td[4]/text()').getall()[0]


        pBudget = response.xpath('//div[@class="content03"][2]//tr[2]/td[2]/text()').getall()[0]


        midlinkman = response.xpath('//div[@class="content03"][10]//tr/td[4]/text()').getall()[0]
        linkman = re.findall('[\u4e00-\u9fa5]+', midlinkman, re.S)
        if linkman:
            linkman = linkman[0]
            linkman = "".join(linkman.split())
        else:
            linkman = response.xpath('//div[@class="content03"][10]//tr[5]/td[2]/text()').getall()[0]


        tel = response.xpath('//div[@class="content03"][10]//tr/td[4]/text()').getall()[0].replace(linkman,'').replace('/','')


        agentName = response.xpath('//div[@class="content03"][10]//tr[3]/td[2]/text()').getall()[0]


        agentAddr = response.xpath('//div[@class="content03"][10]//tr[4]/td[2]/text()').getall()[0]


        agentLinkman = response.xpath('//div[@class="content03"][10]//tr[5]/td[2]/text()').getall()[0]


        agentTel = response.xpath('//div[@class="content03"][10]//tr[3]/td[4]/text()').getall()[0]


        bidTime = response.xpath('//div[@class="content03"][7]//tr[1]/td[2]/text()').getall()[0]


        bidAddr = response.xpath('//div[@class="content03"][6]//tr[2]/td[2]/text()').getall()[0]


        getfileStartTime = response.xpath('//div[@class="content03"][6]//tr[1]/td[2]/text()').getall()[0]
        getfileStartTime = [i for i in getfileStartTime if i != ' ']
        getfileStartTime = [e for e in getfileStartTime if e != '']
        getfileStartTime = "".join(getfileStartTime)
        getfileStartTime = getfileStartTime.replace("\xa0", "").replace(" ", "").replace("&nbsp", "").replace("\n", "").replace("\t", "").replace("\r", "")



        getfileTimeDesc = response.xpath('//div[@class="content03"][10]//tr[3]/td[4]/text()').getall()[0]


        mobile = tel

        email = ''

        fax = ''

        agentEmail = ''

        agentFax = ''

        agentMobile = agentTel

        text = a

        getfileEndTime = ''

        prov = ''

        city = ''

        district = ''

        spider = 'hainan'

        source = ' 海南省政府采购网'

        pApprovalName = ''

        pApproveOrg = ''

        pSupervision = ''

        pubTime = ''

        files = ''

        item['entName'] = entName
        item['pNo'] = pNo
        item['pName'] = pName
        item['pAddr'] = pAddr
        item['pApprovalName'] = pApprovalName
        item['pApproveOrg'] = pApproveOrg
        item['pSupervision'] = pSupervision
        item['pubTime'] = pubTime
        item['pBudget'] = pBudget
        item['linkman'] = linkman
        item['tel'] = tel
        item['mobile'] = mobile
        item['email'] = email
        item['fax'] = fax
        item['bidTime'] = bidTime
        item['bidAddr'] = bidAddr
        item['agentName'] = agentName
        item['agentAddr'] = agentAddr
        item['agentLinkman'] = agentLinkman
        item['agentTel'] = agentTel
        item['agentMobile'] = agentMobile
        item['agentEmail'] = agentEmail
        item['agentFax'] = agentFax
        item['prov'] = prov
        item['city'] = city
        item['district'] = district
        item['spider'] = spider
        item['source'] = source
        item['sourceUrl'] = sourceUrl
        item['getfileStartTime'] = getfileStartTime
        item['getfileEndTime'] = getfileEndTime
        item['getfileTimeDesc'] = getfileTimeDesc
        item['text'] = text
        item['files'] = files

        print(item)

        # yield item

if __name__ == '__main__':
    cmdline.execute("scrapy crawl hainan".split())