import json
import scrapy
from Testchen.items import TestchenItem
import re
from scrapy import cmdline, selector

class HubeiSpider(scrapy.Spider):
    name = 'hubei'

    def start_requests(self):
        url = 'http://www.hbbidcloud.cn/EpointWebBuilder_hubeiggzy/frontAppAction.action?cmd=getPageInfoList'
        # FormRequest 是Scrapy发送POST请求的方法
        yield scrapy.FormRequest(
            url = url,
            formdata={'categoryNum':'004002',
                      'siteGuid': '7eb5f7f1-9041-43ad-8e13-8fcb82ea831a',
                      'pageIndex': '102',
                      'controlName': 'subpagelist'},
            callback = self.parse
        )


    def parse(self, response, **kwargs):
        # print(response.text)
        paydata = json.loads(response.text)

        data = paydata['custom']

        data1 =json.loads(data)

        data2 = data1['infodata']

        for i in data2:

            sourceUrl = 'http://www.hbbidcloud.cn' + i['infourl']

            yield scrapy.Request(sourceUrl,meta={'sourceUrl':sourceUrl}, callback=self.parse2)


        if 'num' in response.meta:
            x = int(response.meta['num'])
        else:
            x = 102
        if x < 105:
            x = x + 1
            url = 'http://www.hbbidcloud.cn/EpointWebBuilder_hubeiggzy/frontAppAction.action?cmd=getPageInfoList'
            # FormRequest 是Scrapy发送POST请求的方法
            yield scrapy.FormRequest(
                url=url,
                formdata={'categoryNum': '004002',
                          'siteGuid': '7eb5f7f1-9041-43ad-8e13-8fcb82ea831a',
                          'pageIndex': str(x),
                          'controlName': 'subpagelist'},
                callback=self.parse,meta={'num': str(x)}
            )


    def parse2(self, response):
        item = TestchenItem()
        sourceUrl = response.request.meta['sourceUrl']
        item['sourceUrl'] = sourceUrl
        print(item)
        a = ''
        b = ''
        nums = ''

    # def parse2(self, response):
    #     item = TestchenItem()
    #     sourceUrl = response.request.meta['sourceUrl']
    #     a = ''
    #     b = ''
    #     nums = ''
    #
    #     content = response.xpath('//div[@class="ewb-article-info"]')
    #     for node in content:
    #         p = node.xpath('./div/p')
    #         for d in p:
    #             text = d.xpath('.//text()').getall()
    #             text_str = "".join(text).replace("\n", "")
    #             a += text_str + '\n'
    #
    #     a = a.replace("\xa0", "")
    #     a = a.replace(" ", "")
    #     a = a.replace("&nbsp;", "")
    #     a = a.replace("\r", "")
    #     a = a.replace("\t", "")
    #
    #     print(a)
    #
    #     pName = re.findall('本招标项目(.*?)\(项目名称', a, re.S)
    #     if pName:
    #         pName = pName[0]
    #         pName = "".join(pName.split())
    #         pName = pName + '项目'
    #     else:
    #         pName = str(nums)
    #
    #     if len(pName) > 50:
    #         pName = re.findall('本招标项目(.*?)项目', a, re.S)
    #         if pName:
    #             pName = pName[0]
    #             pName = "".join(pName.split())
    #             pName = pName + '项目'
    #         else:
    #             pName = str(nums)
    #
    #     if len(pName) > 50:
    #         pName = str(nums)
    #     else:
    #         pName = pName
    #
    #     entName = re.findall('招标人：(.*?)招标代理机构：', a, re.S)
    #     if entName:
    #         entName = entName[0]
    #         entName = "".join(entName.split())
    #     else:
    #         entName = re.findall('采购人：(.*?)\s', a, re.S)
    #         if entName:
    #             entName = entName[0]
    #             entName = "".join(entName.split())
    #         else:
    #             entName = str(nums)
    #
    #     pAddr = re.findall('建设地点：(.*?)\s', a, re.S)
    #     if pAddr:
    #         pAddr = pAddr[0]
    #         pAddr = "".join(pAddr.split())
    #     else:
    #         pAddr = str(nums)
    #
    #     pNo = re.findall('招标编号：(.*?)\s', a, re.S)
    #     if pNo:
    #         pNo = pNo[0]
    #         pNo = "".join(pNo.split())
    #     else:
    #         pNo = str(nums)
    #
    #     pBudget = re.findall('合同估算价：(.*?)\s', a, re.S)
    #     if pBudget:
    #         pBudget = pBudget[0]
    #         pBudget = "".join(pBudget.split())
    #     else:
    #         pBudget = re.findall('招标控制价价：(.*?)\s', a, re.S)
    #         if pBudget:
    #             pBudget = pBudget[0]
    #             pBudget = "".join(pBudget.split())
    #         else:
    #             pBudget = re.findall('项目控制价：(.*?)\s', a, re.S)
    #             if pBudget:
    #                 pBudget = pBudget[0]
    #                 pBudget = "".join(pBudget.split())
    #             else:
    #                 pBudget = re.findall('合同估算价为：(.*?)\s', a, re.S)
    #                 if pBudget:
    #                     pBudget = pBudget[0]
    #                     pBudget = "".join(pBudget.split())
    #                 else:
    #                     pBudget = str(nums)
    #
    #     linkman = re.findall('联系人：(.*?)联系人', a, re.S)
    #     if linkman:
    #         linkman = linkman[0]
    #         linkman = "".join(linkman.split())
    #     else:
    #         linkman = str(nums)
    #
    #     if len(linkman) > 8:
    #         linkman = str(nums)
    #     else:
    #         linkman = linkman
    #
    #     tel = re.findall('电话：(.*?)电话', a, re.S)
    #     if tel:
    #         tel = tel[0]
    #         tel = "".join(tel.split())
    #     else:
    #         tel = str(nums)
    #
    #     if len(tel) > 20:
    #         tel = str(nums)
    #     else:
    #         tel = tel
    #
    #     email = re.findall('电子邮件：(.*?)电子邮件', a, re.S)
    #     if email:
    #         email = email[0]
    #         email = "".join(email.split())
    #     else:
    #         email = str(nums)
    #
    #     if len(email) > 20:
    #         email = str(nums)
    #     else:
    #         email = email
    #
    #     fax = re.findall('传真：(.*?)传真', a, re.S)
    #     if fax:
    #         fax = fax[0]
    #         fax = "".join(fax.split())
    #     else:
    #         fax = str(nums)
    #
    #     if len(fax) > 20:
    #         fax = str(nums)
    #     else:
    #         fax = fax
    #
    #     agentName = re.findall('招标代理机构：(.*?)\s', a, re.S)
    #     if agentName:
    #         agentName = agentName[0]
    #         agentName = "".join(agentName.split())
    #     else:
    #         agentName = re.findall('代理机构：(.*?)\s', a, re.S)
    #         if agentName:
    #             agentName = agentName[0]
    #             agentName = "".join(agentName.split())
    #         else:
    #             agentName = str(nums)
    #
    #     midAddr = re.findall('地址：(.*?)地址', a, re.S)
    #     if midAddr:
    #         midAddr = midAddr[0]
    #     else:
    #         midAddr = str(nums)
    #
    #     if len(midAddr) > 30:
    #         midAddr = str(nums)
    #     else:
    #         midAddr = midAddr
    #
    #     if midAddr:
    #         midagentAddr = "(?s){}+地址：(.*?)\s".format(midAddr)
    #         agentAddr = re.findall(midagentAddr, a, re.S)
    #         if agentAddr:
    #             agentAddr = agentAddr[0]
    #             agentAddr = "".join(agentAddr.split())
    #         else:
    #             agentAddr = str(nums)
    #     else:
    #         agentAddr = str(nums)
    #
    #     if len(agentAddr) > 50:
    #         agentAddr = str(nums)
    #     else:
    #         agentAddr = agentAddr
    #
    #     if linkman:
    #         midagentLinkman = "(?s){}+联系人：(.*?)\s".format(linkman)
    #         agentLinkman = re.findall(midagentLinkman, a, re.S)
    #         if agentLinkman:
    #             agentLinkman = agentLinkman[0]
    #             agentLinkman = "".join(agentLinkman.split())
    #         else:
    #             agentLinkman = str(nums)
    #     else:
    #         agentLinkman = str(nums)
    #
    #     if len(agentLinkman) > 10:
    #         agentLinkman = str(nums)
    #     else:
    #         agentLinkman = agentLinkman
    #
    #     midagentTel = "(?s){}电话：(.*?)\s".format(tel)
    #     agentTel = re.findall(midagentTel, a, re.S)
    #     if agentTel:
    #         agentTel = agentTel[0]
    #         agentTel = "".join(agentTel.split())
    #     else:
    #         agentTel = str(nums)
    #
    #     if len(agentTel) > 30:
    #         agentTel = str(nums)
    #     else:
    #         agentTel = agentTel
    #
    #     midagentEmail = "(?s){}电子邮件：(.*?)\s".format(email)
    #     agentEmail = re.findall(midagentEmail, a, re.S)
    #     if agentEmail:
    #         agentEmail = agentEmail[0]
    #         agentEmail = "".join(agentEmail.split())
    #     else:
    #         agentEmail = str(nums)
    #
    #     if len(agentEmail) > 30:
    #         agentEmail = str(nums)
    #     else:
    #         agentEmail = agentEmail
    #
    #     midagentFax = "(?s){}传真：(.*?)\s".format(fax)
    #     agentFax = re.findall(midagentFax, a, re.S)
    #     if agentFax:
    #         agentFax = agentFax[0]
    #         agentFax = "".join(agentFax.split())
    #         agentFax = agentFax.replace('传真：', '')
    #     else:
    #         agentFax = str(nums)
    #
    #     if len(agentFax) > 30:
    #         agentFax = str(nums)
    #     else:
    #         agentFax = agentFax
    #
    #     bidTime = re.findall('投标文件递交截止时间为(.*?)。', a, re.S)
    #     if bidTime:
    #         bidTime = bidTime[0]
    #         bidTime = "".join(bidTime.split())
    #     else:
    #         bidTime = str(nums)
    #
    #     if len(bidTime) > 30:
    #         bidTime = str(nums)
    #     else:
    #         bidTime = bidTime
    #
    #     bidAddr = re.findall('递交至(.*?)。', a, re.S)
    #     if bidAddr:
    #         bidAddr = bidAddr[0]
    #         bidAddr = "".join(bidAddr.split())
    #     else:
    #         bidAddr = str(nums)
    #
    #     if len(bidAddr) > 30:
    #         bidAddr = str(nums)
    #     else:
    #         bidAddr = bidAddr
    #
    #     getfileStartTime = re.findall('请于(.*?)止', a, re.S)
    #     if getfileStartTime:
    #         getfileStartTime = getfileStartTime[0]
    #         getfileStartTime = "".join(getfileStartTime.split())
    #     else:
    #         getfileStartTime = str(nums)
    #
    #     if len(getfileStartTime) > 40:
    #         getfileStartTime = str(nums)
    #     else:
    #         getfileStartTime = getfileStartTime
    #
    #     getfileTimeDesc = re.findall('投标文件递交截止时间为(.*?)。', a, re.S)
    #     if getfileTimeDesc:
    #         getfileTimeDesc = getfileTimeDesc[0]
    #         getfileTimeDesc = "".join(getfileTimeDesc.split())
    #     else:
    #         getfileTimeDesc = str(nums)
    #
    #     if len(getfileTimeDesc) > 40:
    #         getfileTimeDesc = str(nums)
    #     else:
    #         getfileTimeDesc = getfileTimeDesc
    #
    #     mobile = tel
    #
    #     agentMobile = agentTel
    #
    #     text = a
    #
    #     getfileEndTime = ''
    #
    #     prov = ''
    #
    #     city = ''
    #
    #     district = ''
    #
    #     spider = 'hubei'
    #
    #     source = ' 湖北省电子招投标交易平台'
    #
    #     pApprovalName = ''
    #
    #     pApproveOrg = ''
    #
    #     pSupervision = ''
    #
    #     pubTime = ''
    #
    #     files = ''
    #
    #
    #     item['pNo'] = pNo
    #
    #     item['pName'] = pName
    #
    #     item['entName'] = entName
    #
    #     item['pAddr'] = pAddr
    #
    #     item['pApprovalName'] = pApprovalName
    #
    #     item['pApproveOrg'] = pApproveOrg
    #
    #     item['pSupervision'] = pSupervision
    #
    #     item['pubTime'] = pubTime
    #
    #     item['pBudget'] = pBudget
    #
    #     item['linkman'] = linkman
    #
    #     item['tel'] = tel
    #
    #     item['mobile'] = mobile
    #
    #     item['email'] = email
    #
    #     item['fax'] = fax
    #
    #     item['bidTime'] = bidTime
    #
    #     item['bidAddr'] = bidAddr
    #
    #     item['agentName'] = agentName
    #
    #     item['agentAddr'] = agentAddr
    #
    #     item['agentLinkman'] = agentLinkman
    #
    #     item['agentTel'] = agentTel
    #
    #     item['agentMobile'] = agentMobile
    #
    #     item['agentEmail'] = agentEmail
    #
    #     item['agentFax'] = agentFax
    #
    #     item['prov'] = prov
    #
    #     item['city'] = city
    #
    #     item['district'] = district
    #
    #     item['spider'] = spider
    #
    #     item['source'] = source
    #
    #     item['sourceUrl'] = sourceUrl
    #
    #     item['getfileStartTime'] = getfileStartTime
    #
    #     item['getfileEndTime'] = getfileEndTime
    #
    #     item['getfileTimeDesc'] = getfileTimeDesc
    #
    #     item['text'] = text
    #
    #     item['files'] = files
    #
    #
    #     print(item)
    #
    #     yield item








if __name__ == '__main__':
    cmdline.execute("scrapy crawl hubei".split())