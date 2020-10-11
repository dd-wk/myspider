import json
import scrapy
from Testchen.items import TestchenItem
import re
from scrapy import cmdline, selector

class ShanghaiSpider(scrapy.Spider):
    name = 'shanghai'
    start_urls = ['http://ggzy.sheic.org.cn/publicity/constructionProject/page?page=1&pageSize=20&tenderStatus=1&region=0']


    def parse(self, response, **kwargs):
        # print(response.text)
        paydata = json.loads(response.text)
        data = paydata['result']
        data1 = data['list']
        for i in data1:
            sourceUrl = "http://ggzy.sheic.org.cn/publicity/constructionBulletin/findBulletinList/" + i['tenderProjectCode']
            yield scrapy.Request(sourceUrl,meta={'sourceUrl':sourceUrl}, callback=self.parse2)

    def parse2(self, response):
        item = TestchenItem()
        sourceUrl = response.request.meta['sourceUrl']
        item['sourceUrl'] = sourceUrl

        paydata = json.loads(response.text)

        data = paydata['result']
        pNo = data['tenderProjectCode']
        pName = data['projectName']
        entName = data['tenderAgencyName']
        pAddr = data['address']
        pBudget = data['bidPrice']
        linkman = ''
        tel = ''
        mobile = ''
        email = ''
        fax = ''
        bidTime = data['docSubmitEndTime']
        bidAddr = data['setDocAddress']
        agentName = data['tenderAgencyName']
        agentAddr = ''
        agentLinkman = data['contactPerson']
        agentTel = data['contactInformation']
        agentMobile = agentTel
        agentEmail = ''
        agentFax = ''
        getfileStartTime = data['docTime']
        getfileEndTime = ''
        getfileTimeDesc = ''
        text = ''
        files = ''
        sourceUrl = data['source']
        prov = ''
        city = ''
        district = ''
        spider = ''
        source = ''
        pApprovalName = ''
        pApproveOrg = ''
        pSupervision = ''
        pubTime = ''





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


















if __name__ == '__main__':
    cmdline.execute("scrapy crawl shanghai".split())