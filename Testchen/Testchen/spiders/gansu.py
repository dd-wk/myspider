import json
import scrapy
from Testchen.items import TestchenItem
import re
from scrapy import cmdline, selector


class GansuSpider(scrapy.Spider):
    name = 'gansu'
    # start_urls = ['http://www.ccgp-gansu.gov.cn/web/article/1280501/0/index.htm']
    start_urls = ['http://www.ccgp-jilin.gov.cn/helpFront/gotoHelpFrontList.action?articleId=150865']


    def parse(self, response, **kwargs):
        print(response.text)
        # a = response.xpath('//ul[@class="newsList TipsBox"]')
        # for node in a:
        #     url = node.xpath('./li/span/a/@href').extract()
        #     for c in url:
        #         sourceUrl = 'http://www.ccgp-gansu.gov.cn' + c
        #         yield scrapy.Request(sourceUrl, meta={'sourceUrl': sourceUrl}, callback=self.parse2)
        #
        #
        # if 'num' in response.meta:
        #     x = int(response.meta['num'])
        # else:
        #     x = 1
        # if x < 150:
        #     x = x + 1
        #     z = x*20
        #     url ="http://www.ccgp-gansu.gov.cn/web/article/1280501/" + str(z) + "/index.htm"
        #     yield scrapy.Request(url,meta={'num':str(x)},callback=self.parse)

    # def parse2(self, response):
    #     item = TestchenItem()
    #     sourceUrl = response.request.meta['sourceUrl']
    #
    #     a = ''
    #     nums = ''
    #     content = response.xpath('//div[@class="conTxt"]')
    #     for node in content:
    #         p = node.xpath('.//p')
    #         for d in p:
    #             text = d.xpath('.//text()').getall()
    #             text_str = "".join(text).replace("\n", "")
    #             a += text_str + '\n'
    #
    #     a = a.replace("\xa0", "")
    #     a = a.replace(" ", "")
    #     a = a.replace("&nbsp;", "")
    #     a = a.replace("\u3000", "")
    #     a = a.replace("\r", "")
    #     a = a.replace("\t", "")
    #
    #
    #     pName = re.findall('项目名称：(.*?)\s', a, re.S)
    #     if pName:
    #         pName = pName[0]
    #         pName = "".join(pName.split())
    #     else:
    #         pName = str(nums)
    #
    #     if len(pName) > 50:
    #         pName = str(nums)
    #     else:
    #         pName = pName
    #
    #
    #     entName = re.findall('采购人信息\s名称：(.*?)\s', a, re.S)
    #     if entName:
    #         entName = entName[0]
    #         entName = "".join(entName.split())
    #     else:
    #         entName = re.findall('采购人名称：(.*?)\s', a, re.S)
    #         if entName:
    #             entName = entName[0]
    #             entName = "".join(entName.split())
    #         else:
    #             entName = str(nums)
    #
    #     pAddr = re.findall('项目地点：(.*?)\s', a, re.S)
    #     if pAddr:
    #         pAddr = pAddr[0]
    #         pAddr = "".join(pAddr.split())
    #     else:
    #         midpAddr = "(?s){}[\s]+地址：(.*?)\s".format(entName)
    #         pAddr = re.findall(midpAddr, a, re.S)
    #         if pAddr:
    #             pAddr = pAddr[0]
    #             pAddr = "".join(pAddr.split())
    #         else:
    #             pAddr = str(nums)
    #
    #
    #     pNo = re.findall('项目编号：(.*?)\s', a, re.S)
    #     if pNo:
    #         pNo = pNo[0]
    #         pNo = "".join(pNo.split())
    #     else:
    #         pNo = re.findall('标段编号:(.*?)\s', a, re.S)
    #         if pNo:
    #             pNo = pNo[0]
    #             pNo = "".join(pNo.split())
    #         else:
    #             pNo = str(nums)
    #
    #
    #     pBudget = re.findall('预算金额：(.*?)\s', a, re.S)
    #     if pBudget:
    #         pBudget = pBudget[0]
    #         pBudget = "".join(pBudget.split())
    #     else:
    #         pBudget = re.findall('合同估算价(.*?)\s', a, re.S)
    #         if pBudget:
    #             pBudget = pBudget[0]
    #             pBudget = "".join(pBudget.split())
    #         else:
    #             pBudget = str(nums)
    #
    #     if len(pBudget)>20:
    #         pBudget = str(nums)
    #     else:
    #         pBudget = pBudget
    #
    #
    #     linkman = re.findall('联系人：(.*?)\s', a, re.S)
    #     if linkman:
    #         linkman = linkman[0]
    #         linkman = "".join(linkman.split())
    #     else:
    #         midlinkman = re.findall('联系方式：(.*?)\s', a, re.S)
    #         if midlinkman:
    #             midlinkman = midlinkman[0]
    #             midlinkman = "".join(midlinkman.split())
    #             linkman = re.findall('[\u4e00-\u9fa5]+', midlinkman, re.S)
    #             if linkman:
    #                 linkman = linkman[0]
    #                 linkman = "".join(linkman.split())
    #             else:
    #                 linkman = str(nums)
    #         else:
    #             linkman = str(nums)
    #
    #     if len(linkman) > 8:
    #         linkman = str(nums)
    #     else:
    #         linkman = linkman
    #
    #
    #     tel = re.findall('联系方式：(.*?)\s', a, re.S)
    #     if tel:
    #         tel = tel[0]
    #         tel = "".join(tel.split())
    #     else:
    #         tel = str(nums)
    #
    #
    #     if len(tel) > 20:
    #         tel = str(nums)
    #     else:
    #         tel = tel
    #
    #
    #     fax = re.findall('传真：(.*?)\s', a, re.S)
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
    #
    #     agentName = re.findall('招标代理机构：(.*?)\s', a, re.S)
    #     if agentName:
    #         agentName = agentName[0]
    #         agentName = "".join(agentName.split())
    #     else:
    #         agentName = re.findall('采购代理机构信息\s名称：(.*?)\s', a, re.S)
    #         if agentName:
    #             agentName = agentName[0]
    #             agentName = "".join(agentName.split())
    #         else:
    #             agentName = str(nums)
    #
    #
    #     agentAddr = re.findall('地址：(.*?)\s', a, re.S)
    #     if agentAddr:
    #             agentAddr = agentAddr[1]
    #             agentAddr = "".join(agentAddr.split())
    #     else:
    #         midagentAddr = "(?s){}[\s]+地址：(.*?)\s".format(agentName)
    #         agentAddr = re.findall(midagentAddr, a, re.S)
    #         if agentAddr:
    #                 agentAddr = agentAddr[0]
    #                 agentAddr = "".join(agentAddr.split())
    #         else:
    #             agentAddr = str(nums)
    #
    #     if len(agentAddr) > 50:
    #         agentAddr = str(nums)
    #     else:
    #         agentAddr = agentAddr
    #
    #
    #     agentLinkman = re.findall('项目联系人：(.*?)\s', a, re.S)
    #     if agentLinkman:
    #         agentLinkman = agentLinkman[0]
    #         agentLinkman = "".join(agentLinkman.split())
    #     else:
    #         agentLinkman = str(nums)
    #
    #     if len(agentLinkman) > 10:
    #         agentLinkman = str(nums)
    #     else:
    #         agentLinkman = agentLinkman
    #
    #
    #     midagentTel = "(?s){}[\s]+电话：(.*?)\s".format(agentLinkman)
    #     agentTel = re.findall(midagentTel, a, re.S)
    #     if agentTel:
    #         agentTel = agentTel[0]
    #         agentTel = "".join(agentTel.split())
    #     else:
    #         agentTel = str(nums)
    #
    #
    #     if len(agentTel) > 30:
    #         agentTel = str(nums)
    #     else:
    #         agentTel = agentTel
    #
    #
    #     agentEmail = re.findall('邮箱：(.*?)\s', a, re.S)
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
    #
    #     agentFax = re.findall('传真：(.*?)\s', a, re.S)
    #     if agentFax:
    #         agentFax = agentFax[0]
    #         agentFax = "".join(agentFax.split())
    #     else:
    #         agentFax = str(nums)
    #
    #     if len(agentFax) > 30:
    #         agentFax = str(nums)
    #     else:
    #         agentFax = agentFax
    #
    #
    #     bidTime = re.findall('提交投标文件截止时间、开标时间和地点\s时间：(.*?)\s', a, re.S)
    #     if bidTime:
    #         bidTime = bidTime[0]
    #         bidTime = "".join(bidTime.split())
    #     else:
    #         bidTime = re.findall('开标时间:(.*?)\s', a, re.S)
    #         if bidTime:
    #             bidTime = bidTime[0]
    #             bidTime = "".join(bidTime.split())
    #         else:
    #             bidTime = re.findall('截止时间：(.*?)\s', a, re.S)
    #             if bidTime:
    #                 bidTime = bidTime[0]
    #                 bidTime = "".join(bidTime.split())
    #             else:
    #                 bidTime = str(nums)
    #
    #
    #     bidAddr = re.findall('开标地点：(.*?)\s', a, re.S)
    #     if bidAddr:
    #         bidAddr = bidAddr[0]
    #         bidAddr = "".join(bidAddr.split())
    #     else:
    #         midbidAddr = "(?s){}[\s]+地点：(.*?)\s".format(bidTime)
    #         bidAddr = re.findall(midbidAddr, a, re.S)
    #         if bidAddr:
    #             bidAddr = bidAddr[0]
    #             bidAddr = "".join(bidAddr.split())
    #         else:
    #             bidAddr = str(nums)
    #
    #     if len(bidAddr) > 70:
    #         bidAddr = str(nums)
    #     else:
    #         bidAddr = bidAddr
    #
    #
    #     getfileStartTime = re.findall('获取招标文件\s时间：(.*?)\s', a, re.S)
    #     if getfileStartTime:
    #         getfileStartTime = getfileStartTime[0]
    #         getfileStartTime = "".join(getfileStartTime.split())
    #     else:
    #         getfileStartTime = re.findall('获取招标文件的时间：(.*?)\s', a, re.S)
    #         if getfileStartTime:
    #             getfileStartTime = getfileStartTime[0]
    #             getfileStartTime = "".join(getfileStartTime.split())
    #         else:
    #             getfileStartTime = re.findall('获取竞争性磋商文件的时间：(.*?)\s', a, re.S)
    #             if getfileStartTime:
    #                 getfileStartTime = getfileStartTime[0]
    #                 getfileStartTime = "".join(getfileStartTime.split())
    #             else:
    #                 getfileStartTime = str(nums)
    #
    #     if len(getfileStartTime) > 50:
    #         getfileStartTime = str(nums)
    #     else:
    #         getfileStartTime = getfileStartTime
    #
    #
    #
    #     getfileTimeDesc = re.findall('公告期限\s(.*?)\s', a, re.S)
    #     if getfileTimeDesc:
    #         getfileTimeDesc = getfileTimeDesc[0]
    #         getfileTimeDesc = "".join(getfileTimeDesc.split())
    #     else:
    #         getfileTimeDesc = re.findall('提交投标文件截止时间、开标时间和地点\s时间：(.*?)\s', a, re.S)
    #         if getfileTimeDesc:
    #             getfileTimeDesc = getfileTimeDesc[0]
    #             getfileTimeDesc = "".join(getfileTimeDesc.split())
    #         else:
    #             getfileTimeDesc = str(nums)
    #
    #     if len(getfileTimeDesc) > 40:
    #         getfileTimeDesc = str(nums)
    #     else:
    #         getfileTimeDesc = getfileTimeDesc
    #
    #     mobile = tel
    #
    #     email = ''
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
    #     spider = 'gansu'
    #
    #     source = '甘肃政府采购网'
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
    #     # print(item)
    #
    #     yield item



if __name__ == '__main__':
    cmdline.execute("scrapy crawl gansu".split())