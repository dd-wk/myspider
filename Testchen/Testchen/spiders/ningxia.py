import scrapy
import json
import scrapy
import re
from scrapy import cmdline, selector
from Testchen.items import TestchenItem
import time

# class NingxiaSpider(scrapy.Spider):
#     name = 'ningxia'
#
#     def start_requests(self):
#         url = 'http://www.ccgp-ningxia.gov.cn//site/InteractionQuestion_findVNotice.do'
#         # FormRequest 是Scrapy发送POST请求的方法
#         yield scrapy.FormRequest(
#             url=url,
#             headers={
#                         'Host': 'www.ccgp-ningxia.gov.cn',
#                         'Pragma': 'no-cache',
#                         'Referer': 'http://www.ccgp-ningxia.gov.cn/public/NXGPPNEW/dynamic/contents/CGGG/index.jsp?cid=312&sid=1',
#                         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
#                         'X-Requested-With': 'XMLHttpRequest'
#             },
#             formdata={'type': '101',
#                       'date': '',
#                       'page': '1',
#                       'regionId': '640000',
#                       'tab': 'Q',
#                       'dateq1': '',
#                       'dateq2': '',
#                       'keyword': '',
#                       'buyerName':'',
#                       'agentName ': '',
#                       'projectNumber': '',
#                       'planNumber': '',
#                       'authCode': ''
#                       },
#             callback=self.parse
#         )
#
#
#         # yield scrapy.Request(
#         #     method="POST",
#         #     url = url,
#         #     body={'type':'101','date': '','page': '2','regionId': '640000','tab': 'Q','dateq1': '','dateq2': '','keyword': '','authCode': '',},
#         #     callback = self.parse
#         # )
#
#     def parse(self, response, **kwargs):
#         print(response.text)
#         # paydata = json.loads(response.text)
#         # data = paydata['result']
#         # data1 = data['records']
#         # for i in data1:
#         #     sourceUrl = "https://www.cqggzy.com/xxhz/014001/014001001/014001001001/20200917/" + i['infoid'] + ".html"
#         #     yield scrapy.Request(sourceUrl,meta={'sourceUrl':sourceUrl}, callback=self.parse2)
#
#         # if 'num' in response.meta:
#         #     x = int(response.meta['num'])
#         # else:
#         #     x = 1
#         # if x < 1500:
#         #     x = x + 1
#         #     url = 'https://www.ccgp-hainan.gov.cn/cgw/cgw_list.jsp'
#         #     # FormRequest 是Scrapy发送POST请求的方法
#         #     yield scrapy.FormRequest(
#         #         url=url,
#         #         formdata = {'type': '101',
#         #                     'date': '',
#         #                     'page': '1',
#         #                     'regionId': '640000',
#         #                     'tab': 'Q',
#         #                     'dateq1': '',
#         #                     'dateq2': '',
#         #                     'keyword': '1',
#         #                     },
#         #         callback=self.parse, meta={'num': str(x)})
#
#     def parse2(self, response):
#         item = TestchenItem()
#         sourceUrl = response.request.meta['sourceUrl']
#
#         a = ''
#         content0 = ''
#         content1 = ''
#         nums = ''
#         content = response.xpath('//div[@id="con_TBAB_1"]')
#         for node in content:
#             p = node.xpath('./p')
#             for d in p:
#                 text = d.xpath('.//text()').getall()
#                 text_str = "".join(text).replace("\n", "")
#                 content0 += text_str + '\n'
#
#         content0 = content0.replace("\xa0", "")
#         content0 = content0.replace(" ", "")
#         content0 = content0.replace("&nbsp;", "")
#         content0 = content0.replace("\u3000", "")
#         content0 = content0.replace("\r", "")
#         content0 = content0.replace("\t", "")
#
#         content = response.xpath('//div[@id="con_TBAB_1"]')
#         for node in content:
#             p = node.xpath('.//div')
#             for d in p:
#                 text = d.xpath('.//text()').getall()
#                 text_str = "".join(text).replace("\n", "")
#                 content1 += text_str + '\n'
#
#         content1 = content1.replace("\xa0", "")
#         content1 = content1.replace(" ", "")
#         content1 = content1.replace("&nbsp;", "")
#         content1 = content1.replace("\u3000", "")
#         content1 = content1.replace("\r", "")
#         content1 = content1.replace("\t", "")
#
#         if len(content0) > len(content1):
#             a = content0
#         else:
#             a = content1
#
#         pName = response.xpath('//div[@class="content03"][2]//tr/td[2]/text()').getall()[0]
#
#         entName = response.xpath('//div[@class="content03"][10]//td[2]/text()').getall()[0]
#
#         pAddr = response.xpath('//div[@class="content03"][10]//tr[2]/td[2]/text()').getall()[0]
#
#         pNo = response.xpath('//div[@class="content03"][2]//tr/td[4]/text()').getall()[0]
#
#         pBudget = response.xpath('//div[@class="content03"][2]//tr[2]/td[2]/text()').getall()[0]
#
#         midlinkman = response.xpath('//div[@class="content03"][10]//tr/td[4]/text()').getall()[0]
#         linkman = re.findall('[\u4e00-\u9fa5]+', midlinkman, re.S)
#         if linkman:
#             linkman = linkman[0]
#             linkman = "".join(linkman.split())
#         else:
#             linkman = response.xpath('//div[@class="content03"][10]//tr[5]/td[2]/text()').getall()[0]
#
#         tel = response.xpath('//div[@class="content03"][10]//tr/td[4]/text()').getall()[0].replace(linkman, '').replace(
#             '/', '')
#
#         agentName = response.xpath('//div[@class="content03"][10]//tr[3]/td[2]/text()').getall()[0]
#
#         agentAddr = response.xpath('//div[@class="content03"][10]//tr[4]/td[2]/text()').getall()[0]
#
#         agentLinkman = response.xpath('//div[@class="content03"][10]//tr[5]/td[2]/text()').getall()[0]
#
#         agentTel = response.xpath('//div[@class="content03"][10]//tr[3]/td[4]/text()').getall()[0]
#
#         bidTime = response.xpath('//div[@class="content03"][7]//tr[1]/td[2]/text()').getall()[0]
#
#         bidAddr = response.xpath('//div[@class="content03"][6]//tr[2]/td[2]/text()').getall()[0]
#
#         getfileStartTime = response.xpath('//div[@class="content03"][6]//tr[1]/td[2]/text()').getall()[0]
#         getfileStartTime = [i for i in getfileStartTime if i != ' ']
#         getfileStartTime = [e for e in getfileStartTime if e != '']
#         getfileStartTime = "".join(getfileStartTime)
#         getfileStartTime = getfileStartTime.replace("\xa0", "").replace(" ", "").replace("&nbsp", "").replace("\n",
#                                                                                                               "").replace(
#             "\t", "").replace("\r", "")
#
#         getfileTimeDesc = response.xpath('//div[@class="content03"][10]//tr[3]/td[4]/text()').getall()[0]
#
#         mobile = tel
#
#         email = ''
#
#         fax = ''
#
#         agentEmail = ''
#
#         agentFax = ''
#
#         agentMobile = agentTel
#
#         text = a
#
#         getfileEndTime = ''
#
#         prov = ''
#
#         city = ''
#
#         district = ''
#
#         spider = 'ningxai'
#
#         source = ' 宁夏回族自治区政府采购网'
#
#         pApprovalName = ''
#
#         pApproveOrg = ''
#
#         pSupervision = ''
#
#         pubTime = ''
#
#         files = ''
#
#         # item['entName'] = entName
#         # item['pNo'] = pNo
#         # item['pName'] = pName
#         # item['pAddr'] = pAddr
#         # item['pApprovalName'] = pApprovalName
#         # item['pApproveOrg'] = pApproveOrg
#         # item['pSupervision'] = pSupervision
#         # item['pubTime'] = pubTime
#         # item['pBudget'] = pBudget
#         # item['linkman'] = linkman
#         # item['tel'] = tel
#         # item['mobile'] = mobile
#         # item['email'] = email
#         # item['fax'] = fax
#         # item['bidTime'] = bidTime
#         # item['bidAddr'] = bidAddr
#         # item['agentName'] = agentName
#         # item['agentAddr'] = agentAddr
#         # item['agentLinkman'] = agentLinkman
#         # item['agentTel'] = agentTel
#         # item['agentMobile'] = agentMobile
#         # item['agentEmail'] = agentEmail
#         # item['agentFax'] = agentFax
#         # item['prov'] = prov
#         # item['city'] = city
#         # item['district'] = district
#         # item['spider'] = spider
#         # item['source'] = source
#         item['sourceUrl'] = sourceUrl
#         # item['getfileStartTime'] = getfileStartTime
#         # item['getfileEndTime'] = getfileEndTime
#         # item['getfileTimeDesc'] = getfileTimeDesc
#         # item['text'] = text
#         # item['files'] = files
#
#         print(item)
#
#         # yield item

class NingxiaSpider(scrapy.Spider):
    name = 'ningxia'
    start_urls = ['http://www.nxggzyjy.org/ningxiaweb/002/002001/002001001/1.html']

    def parse(self, response, **kwargs):
        a = response.xpath('//div[@class="ewb-right l"]/div//ul')
        for node in a:
            url = node.xpath('./li/div/a/@href').getall()
            for c in url:
                # print(c)
                sourceUrl = 'http://www.nxggzyjy.org' + c
                yield scrapy.Request(sourceUrl, meta={'sourceUrl': sourceUrl,'c':c}, callback=self.parse2)
        # sourceUrl = 'http://www.nxggzyjy.org/ningxiaweb/002/002001/002001001/20170328/b785df4e-b1f5-4f35-8f1f-818165075f06.html'
        # yield scrapy.Request(sourceUrl, meta={'sourceUrl': sourceUrl, 'c': '/ningxiaweb/002/002001/002001001/20170328/b785df4e-b1f5-4f35-8f1f-818165075f06.html'}, callback=self.parse2)


    def parse2(self, response):
        s = response.text
        item = TestchenItem()
        sourceUrl = response.request.meta['sourceUrl']
        item['sourceUrl'] = sourceUrl
        c = response.request.meta['c']
        c = c.replace('/ningxiaweb/002/002001/002001001','').replace('.html','')
        x = re.findall(r'/(\d*?)/', c, re.S)
        if x:
            x = x[0]
            x = "".join(x.split())
        else:
            x = str(x)
        aurl = c.replace(x,'').replace('/','')
        a = ''
        nums = ''
        content = response.xpath('//div[@data-role="tab-content"]')
        for node in content:
            p = node.xpath('.//p')
            # q = node.xpath('./table')
            for d in p:
                text = d.xpath('.//text()').getall()
                text_str = "".join(text).replace("\n", "")
                a += text_str + '\n'

        a = a.replace("\xa0", "")
        a = a.replace(" ", "")
        a = a.replace("&nbsp;", "")
        a = a.replace("\u3000", "")
        a = a.replace("\u2002", "")
        a = a.replace("\r", "")
        a = a.replace("\t", "")

        if s.find('项目信息') >=0:
            yield scrapy.FormRequest('http://www.nxggzyjy.org/ningxiaweb/detailjson/getallprocessdetailInfo/'+'1'+aurl+'.json', callback=self.parse3, meta={'sourceUrl': sourceUrl,'aurl':aurl,'a':a,'item':item})
        else:
            pName = re.findall('项目名称：(.*?)\s', a, re.S)
            if pName:
                pName = pName[0]
                pName = "".join(pName.split())
            else:
                pName = re.findall('工程名称：(.*?)\s', a, re.S)
                if pName:
                    pName = pName[0]
                    pName = "".join(pName.split())
                else:
                    pName = re.findall('本招标项目(.*?)工程', a, re.S)
                    if pName:
                        pName = pName[0]
                        pName = "".join(pName.split())
                        pName = pName + '工程'
                    else:
                        pName = str(nums)

            if len(pName) > 50:
                pName = str(nums)
            else:
                pName = pName

            if pName == str(nums):
                pName = re.findall('本招标项目(.*?)项目', a, re.S)
                if pName:
                    pName = pName[0]
                    pName = "".join(pName.split())
                    pName = pName + '项目'
                else:
                    pName = str(nums)

            if len(pName) > 50:
                pName = str(nums)
            else:
                pName = pName

            entName = re.findall('采购人信息\s名称：(.*?)\s', a, re.S)
            if entName:
                entName = entName[0]
                entName = "".join(entName.split())
            else:
                entName = re.findall('招标人：(.*?)\s', a, re.S)
                if entName:
                    entName = entName[0]
                    entName = "".join(entName.split())
                else:
                    entName = str(nums)

            if entName:
                midpAddr = "(?s){}[\s]+地址：(.*?)\s".format(entName)
                pAddr = re.findall(midpAddr, a, re.S)
                if pAddr:
                    pAddr = pAddr[0]
                    pAddr = "".join(pAddr.split())
                else:
                    pAddr = str(nums)
            else:
                pAddr = str(nums)

            if pAddr == str(nums):
                pAddr = re.findall('建设地点：(.*?)\s', a, re.S)
                if pAddr:
                    pAddr = pAddr[0]
                    pAddr = "".join(pAddr.split())
                else:
                    pAddr = str(nums)

            pNo = re.findall('项目编号：(.*?)\s', a, re.S)
            if pNo:
                pNo = pNo[0]
                pNo = "".join(pNo.split())
            else:
                pNo = str(nums)

            pBudget = re.findall('预算金额：(.*?)\s', a, re.S)
            if pBudget:
                pBudget = pBudget[0]
                pBudget = "".join(pBudget.split())
                pBudget = pBudget + '元'
            else:
                pBudget = str(nums)

            linkman = re.findall('项目联系人：(.*?)\s', a, re.S)
            if linkman:
                linkman = linkman[0]
                linkman = "".join(linkman.split())
            else:
                linkman = re.findall('联系人：(.*?)\s', a, re.S)
                if linkman:
                    linkman = linkman[0]
                    linkman = "".join(linkman.split())
                else:
                    linkman = str(nums)

            if len(linkman) > 8:
                linkman = str(nums)
            else:
                linkman = linkman

            if pAddr:
                midtel = "(?s){}[\s]+联系方式：(.*?)\s".format(pAddr)
                tel = re.findall(midtel, a, re.S)
                if tel:
                    tel = tel[0]
                    tel = "".join(tel.split())
                else:
                    tel = str(nums)
            else:
                tel = str(nums)

            if tel == str(nums):
                tel = re.findall('电话/传真：(.*?)\s', a, re.S)
                if tel:
                    tel = tel[0]
                    tel = "".join(tel.split())
                else:
                    tel = re.findall('电话：(.*?)\s', a, re.S)
                    if tel:
                        tel = tel[0]
                        tel = "".join(tel.split())
                    else:
                        tel = str(nums)

            if len(tel) > 20:
                tel = str(nums)
            else:
                tel = tel

            agentName = re.findall('采购代理机构信息\s名称：(.*?)\s', a, re.S)
            if agentName:
                agentName = agentName[0]
                agentName = "".join(agentName.split())
            else:
                agentName = re.findall('招标代理机构：(.*?)\s', a, re.S)
                if agentName:
                    agentName = agentName[0]
                    agentName = "".join(agentName.split())
                else:
                    agentName = str(nums)

            midagentAddr = "(?s){}[\s]+地址：(.*?)\s".format(agentName)
            agentAddr = re.findall(midagentAddr, a, re.S)
            if agentAddr:
                agentAddr = agentAddr[0]
                agentAddr = "".join(agentAddr.split())
            else:
                agentAddr = str(nums)

            if len(agentAddr) > 50:
                agentAddr = str(nums)
            else:
                agentAddr = agentAddr

            agentLinkman = re.findall('项目联系人：(.*?)\s', a, re.S)
            if agentLinkman:
                agentLinkman = agentLinkman[0]
                agentLinkman = "".join(agentLinkman.split())
            else:
                agentLinkman = re.findall('联系人：(.*?)\s', a, re.S)
                if agentLinkman:
                    try:
                        agentLinkman = agentLinkman[1]
                        agentLinkman = "".join(agentLinkman.split())
                    except Exception as e:
                        agentLinkman = re.findall('联系人：(.*?)\s', a, re.S)
                        if agentLinkman:
                            agentLinkman = agentLinkman[0]
                            agentLinkman = "".join(agentLinkman.split())
                        else:
                            agentLinkman = str(nums)
                else:
                    agentLinkman = str(nums)

            if len(agentLinkman) > 10:
                agentLinkman = str(nums)
            else:
                agentLinkman = agentLinkman

            midagentTel = "(?s){}[\s]+联系方式：(.*?)\s".format(agentAddr)
            agentTel = re.findall(midagentTel, a, re.S)
            if agentTel:
                agentTel = agentTel[0]
                agentTel = "".join(agentTel.split())
            else:
                agentTel = str(nums)

            if agentTel == str(nums):
                agentTel = re.findall('电话/传真：(.*?)\s', a, re.S)
                if agentTel:
                    agentTel = agentTel[0]
                    agentTel = "".join(agentTel.split())
                else:
                    agentTel = re.findall('电话：(.*?)\s', a, re.S)
                    if agentTel:
                        try:
                            agentTel = agentTel[1]
                            agentTel = "".join(agentTel.split())
                        except Exception as e:
                            agentTel = re.findall('电话：(.*?)\s', a, re.S)
                            if agentTel:
                                agentTel = agentTel[0]
                                agentTel = "".join(agentTel.split())
                            else:
                                agentTel = str(nums)
                    else:
                        agentTel = str(nums)

            if len(agentTel) > 30:
                agentTel = str(nums)
            else:
                agentTel = agentTel

            agentEmail = re.findall('邮箱：(.*?)\s', a, re.S)
            if agentEmail:
                agentEmail = agentEmail[0]
                agentEmail = "".join(agentEmail.split())
            else:
                agentEmail = str(nums)

            if len(agentEmail) > 30:
                agentEmail = str(nums)
            else:
                agentEmail = agentEmail

            agentFax = re.findall('传真：(.*?)\s', a, re.S)
            if agentFax:
                agentFax = agentFax[0]
                agentFax = "".join(agentFax.split())
            else:
                agentFax = str(nums)

            if len(agentFax) > 30:
                agentFax = str(nums)
            else:
                agentFax = agentFax

            bidTime = re.findall('提交投标文件截止时间、开标时间和地点\s(.*?)\s', a, re.S)
            if bidTime:
                bidTime = bidTime[0]
                bidTime = "".join(bidTime.split())
            else:
                bidTime = re.findall('递交的截止时间(.*?)，', a, re.S)
                if bidTime:
                    bidTime = bidTime[0]
                    bidTime = "".join(bidTime.split())
                else:
                    bidTime = re.findall('开标时间(.*?)\s', a, re.S)
                    if bidTime:
                        bidTime = bidTime[0]
                        bidTime = "".join(bidTime.split()).replace()
                    else:
                        bidTime = str(nums)

            midtel = "(?s){}[\s]+地点：(.*?)\s".format(bidTime)
            bidAddr = re.findall(midtel, a, re.S)
            if bidAddr:
                bidAddr = bidAddr[0]
                bidAddr = "".join(bidAddr.split())
            else:
                bidAddr = str(nums)

            if len(bidAddr) > 70:
                bidAddr = str(nums)
            else:
                bidAddr = bidAddr

            getfileStartTime = re.findall('获取招标文件\s时间：(.*?)\s', a, re.S)
            if getfileStartTime:
                getfileStartTime = getfileStartTime[0]
                getfileStartTime = "".join(getfileStartTime.split())
            else:
                getfileStartTime = str(nums)

            getfileTimeDesc = re.findall('公告期限\s(.*?)\s', a, re.S)
            if getfileTimeDesc:
                getfileTimeDesc = getfileTimeDesc[0]
                getfileTimeDesc = "".join(getfileTimeDesc.split())
            else:
                getfileTimeDesc = str(nums)

            if len(getfileTimeDesc) > 40:
                getfileTimeDesc = str(nums)
            else:
                getfileTimeDesc = getfileTimeDesc

            mobile = tel

            email = ''

            fax = ''

            agentMobile = agentTel

            text = a

            getfileEndTime = ''

            prov = '宁夏回族自治区'

            city = ''

            district = ''

            spider = 'ningxia'

            source = '宁夏回族自治区公共资源交易网'

            pApprovalName = ''

            pApproveOrg = ''

            pSupervision = ''

            pubTime = ''

            files = ''

            item['pNo'] = pNo
            item['pName'] = pName
            item['entName'] = entName
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

    def parse3(self, response):
        # print(response.text)
        # item = TestchenItem()
        sourceUrl = response.request.meta['sourceUrl']
        item = response.request.meta['item']
        aurl = response.request.meta['aurl']
        a = response.request.meta['a']
        paydata = json.loads(response.text)
        data = paydata['ret'][0]

        pName = data['projectname']

        pNo = data['projectno']

        entName = data['jianshedanwei']

        pAddr = data['jiaoyizhongxin']

        pBudget = ''

        linkman = data['jiafalianxiren']

        tel = data['jiafalianxirentel']

        agentName = data['dailidanweiname']

        midagentAddr = "(?s){}[\s]+地址：(.*?)\s".format(agentName)
        agentAddr = re.findall(midagentAddr, a, re.S)
        if agentAddr:
            agentAddr = agentAddr[0]
            agentAddr = "".join(agentAddr.split())
        else:
            agentAddr = ''

        if len(agentAddr) > 50:
            agentAddr = ''
        else:
            agentAddr = agentAddr


        agentLinkman = re.findall('项目联系人：(.*?)\s', a, re.S)
        if agentLinkman:
            agentLinkman = agentLinkman[0]
            agentLinkman = "".join(agentLinkman.split())
        else:
            agentLinkman = re.findall('联系人：(.*?)\s', a, re.S)
            if agentLinkman:
                try:
                    agentLinkman = agentLinkman[1]
                    agentLinkman = "".join(agentLinkman.split())
                except Exception as e:
                    agentLinkman = re.findall('联系人：(.*?)\s', a, re.S)
                    if agentLinkman:
                        agentLinkman = agentLinkman[0]
                        agentLinkman = "".join(agentLinkman.split())
                    else:
                        agentLinkman = ''
            else:
                agentLinkman = ''

        if len(agentLinkman) > 10:
            agentLinkman = ''
        else:
            agentLinkman = agentLinkman

        agentTel = data['daililianxirentel']

        mobile = tel

        email = ''

        fax = ''

        agentEmail = ''

        agentFax = ''

        agentMobile = agentTel

        text = a

        getfileEndTime = ''

        prov = '宁夏回族自治区'

        city = pAddr

        district = ''

        spider = 'ningxia'

        source = '宁夏回族自治区公共资源交易网'

        pApprovalName = ''

        pApproveOrg = ''

        pSupervision = ''

        pubTime = ''

        files = ''

        item['pNo'] = pNo

        item['pName'] = pName

        item['entName'] = entName

        item['pAddr'] = pAddr

        item['pBudget'] = pBudget

        item['linkman'] = linkman

        item['tel'] = tel

        item['mobile'] = mobile

        item['email'] = email

        item['fax'] = fax

        item['agentName'] = agentName

        item['agentAddr'] = agentAddr

        item['agentLinkman'] = agentLinkman

        item['agentTel'] = agentTel

        item['agentMobile'] = agentMobile

        item['agentEmail'] = agentEmail

        item['agentFax'] = agentFax

        item['spider'] = spider

        item['source'] = source

        item['sourceUrl'] = sourceUrl

        item['text'] = a

        item['files'] = files

        item['pApprovalName'] = pApprovalName

        item['pApproveOrg'] = pApproveOrg

        item['pSupervision'] = pSupervision

        item['pubTime'] = pubTime

        item['prov'] = prov

        item['city'] = city

        item['district'] = district

        yield scrapy.FormRequest('http://www.nxggzyjy.org/ningxiaweb/detailjson/getallprocessdetailInfo/' + '3' + aurl + '.json',callback=self.parse4, meta={'item':item})


    def parse4(self, response):
        # item = TestchenItem()
        item = response.request.meta['item']
        paydata = json.loads(response.text)
        data = paydata['ret'][0]
        getfileStartTime = data['zbfiledate']
        getfileEndTime = data['zbfileenddate']
        getfileTimeDesc = ''
        bidTime = getfileStartTime
        bidAddr = ''
        item['getfileStartTime'] = getfileStartTime

        item['getfileEndTime'] = getfileEndTime

        item['getfileTimeDesc'] = getfileTimeDesc

        item['bidTime'] = bidTime

        item['bidAddr'] = bidAddr

        print(item)

        if 'num' in response.meta:
            x = int(response.meta['num'])
        else:
            x = 1
        if x < 2:

            x = x + 1
            url = 'http://www.nxggzyjy.org/ningxiaweb/002/002001/002001001/' + str(x) + '.html'

            yield scrapy.FormRequest(url=url,callback=self.parse, meta={'num': str(x)})







if __name__ == '__main__':
    cmdline.execute("scrapy crawl ningxia".split())

    # content = response.xpath('//div[@id="con_TBAB_1"]')
        # for node in content:
        #     p = node.xpath('./p')
        #     for d in p:
        #         text = d.xpath('.//text()').getall()
        #         text_str = "".join(text).replace("\n", "")
        #         content0 += text_str + '\n'
        #
        # content0 = content0.replace("\xa0", "")
        # content0 = content0.replace(" ", "")
        # content0 = content0.replace("&nbsp;", "")
        # content0 = content0.replace("\u3000", "")
        # content0 = content0.replace("\r", "")
        # content0 = content0.replace("\t", "")
        #
        # content = response.xpath('//div[@id="con_TBAB_1"]')
        # for node in content:
        #     p = node.xpath('.//div')
        #     for d in p:
        #         text = d.xpath('.//text()').getall()
        #         text_str = "".join(text).replace("\n", "")
        #         content1 += text_str + '\n'
        #
        # content1 = content1.replace("\xa0", "")
        # content1 = content1.replace(" ", "")
        # content1 = content1.replace("&nbsp;", "")
        # content1 = content1.replace("\u3000", "")
        # content1 = content1.replace("\r", "")
        # content1 = content1.replace("\t", "")
        #
        # if len(content0) > len(content1):
        #     a = content0
        # else:
        #     a = content1
        #
        # pName = response.xpath('//div[@class="content03"][2]//tr/td[2]/text()').getall()[0]
        #
        # entName = response.xpath('//div[@class="content03"][10]//td[2]/text()').getall()[0]
        #
        # pAddr = response.xpath('//div[@class="content03"][10]//tr[2]/td[2]/text()').getall()[0]
        #
        # pNo = response.xpath('//div[@class="content03"][2]//tr/td[4]/text()').getall()[0]
        #
        # pBudget = response.xpath('//div[@class="content03"][2]//tr[2]/td[2]/text()').getall()[0]
        #
        # midlinkman = response.xpath('//div[@class="content03"][10]//tr/td[4]/text()').getall()[0]
        # linkman = re.findall('[\u4e00-\u9fa5]+', midlinkman, re.S)
        # if linkman:
        #     linkman = linkman[0]
        #     linkman = "".join(linkman.split())
        # else:
        #     linkman = response.xpath('//div[@class="content03"][10]//tr[5]/td[2]/text()').getall()[0]
        #
        # tel = response.xpath('//div[@class="content03"][10]//tr/td[4]/text()').getall()[0].replace(linkman, '').replace(
        #     '/', '')
        #
        # agentName = response.xpath('//div[@class="content03"][10]//tr[3]/td[2]/text()').getall()[0]
        #
        # agentAddr = response.xpath('//div[@class="content03"][10]//tr[4]/td[2]/text()').getall()[0]
        #
        # agentLinkman = response.xpath('//div[@class="content03"][10]//tr[5]/td[2]/text()').getall()[0]
        #
        # agentTel = response.xpath('//div[@class="content03"][10]//tr[3]/td[4]/text()').getall()[0]
        #
        # bidTime = response.xpath('//div[@class="content03"][7]//tr[1]/td[2]/text()').getall()[0]
        #
        # bidAddr = response.xpath('//div[@class="content03"][6]//tr[2]/td[2]/text()').getall()[0]
        #
        # getfileStartTime = response.xpath('//div[@class="content03"][6]//tr[1]/td[2]/text()').getall()[0]
        # getfileStartTime = [i for i in getfileStartTime if i != ' ']
        # getfileStartTime = [e for e in getfileStartTime if e != '']
        # getfileStartTime = "".join(getfileStartTime)
        # getfileStartTime = getfileStartTime.replace("\xa0", "").replace(" ", "").replace("&nbsp", "").replace("\n",
        #                                                                                                       "").replace(
        #     "\t", "").replace("\r", "")
        #
        # getfileTimeDesc = response.xpath('//div[@class="content03"][10]//tr[3]/td[4]/text()').getall()[0]
        #
        # mobile = tel
        #
        # email = ''
        #
        # fax = ''
        #
        # agentEmail = ''
        #
        # agentFax = ''
        #
        # agentMobile = agentTel
        #
        # text = a
        #
        # getfileEndTime = ''
        #
        # prov = ''
        #
        # city = ''
        #
        # district = ''
        #
        # spider = 'ningxai'
        #
        # source = ' 宁夏回族自治区政府采购网'
        #
        # pApprovalName = ''
        #
        # pApproveOrg = ''
        #
        # pSupervision = ''
        #
        # pubTime = ''
        #
        # files = ''
        # item['entName'] = entName
        # item['pNo'] = pNo
        # item['pName'] = pName
        # item['pAddr'] = pAddr
        # item['pApprovalName'] = pApprovalName
        # item['pApproveOrg'] = pApproveOrg
        # item['pSupervision'] = pSupervision
        # item['pubTime'] = pubTime
        # item['pBudget'] = pBudget
        # item['linkman'] = linkman
        # item['tel'] = tel
        # item['mobile'] = mobile
        # item['email'] = email
        # item['fax'] = fax
        # item['bidTime'] = bidTime
        # item['bidAddr'] = bidAddr
        # item['agentName'] = agentName
        # item['agentAddr'] = agentAddr
        # item['agentLinkman'] = agentLinkman
        # item['agentTel'] = agentTel
        # item['agentMobile'] = agentMobile
        # item['agentEmail'] = agentEmail
        # item['agentFax'] = agentFax
        # item['prov'] = prov
        # item['city'] = city
        # item['district'] = district
        # item['spider'] = spider
        # item['source'] = source
        # item['getfileStartTime'] = getfileStartTime
        # item['getfileEndTime'] = getfileEndTime
        # item['getfileTimeDesc'] = getfileTimeDesc
        # item['text'] = text
        # item['files'] = files