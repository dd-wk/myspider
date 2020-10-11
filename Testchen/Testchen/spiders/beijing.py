import json
import scrapy
from Testchen.items import TestchenItem
import re
from scrapy import cmdline, selector
import time

class BeijingSpider(scrapy.Spider):
    name = 'beijing'
    start_urls = ['http://www.ccgp-beijing.gov.cn/xxgg/sjzfcggg/sjzbgg/index_1.html']

    def parse(self, response, **kwargs):
        # print(response.text)
        a = response.xpath('//ul[@class="xinxi_ul"]')
        for node in a:
            url = node.xpath('./li/a/@href').extract()
            for c in url:
                c = c.replace('./','/')
                # print(c)
                sourceUrl = 'http://www.ccgp-beijing.gov.cn/xxgg/sjzfcggg/sjzbgg' + c
                yield scrapy.Request(sourceUrl, meta={'sourceUrl': sourceUrl}, callback=self.parse2)


        if 'num' in response.meta:
            x = int(response.meta['num'])
        else:
            x = 1
        if x < 143:
            x = x + 1
            url ="http://www.ccgp-beijing.gov.cn/xxgg/sjzfcggg/sjzbgg/index_" + str(x) + ".html"
            yield scrapy.Request(url,meta={'num':str(x)},callback=self.parse)


    def parse2(self, response):
        item = TestchenItem()
        sourceUrl = response.request.meta['sourceUrl']
        a = ''
        nums = ''
        content = response.xpath('//div[@align="left"]')
        for node in content:
            p = node.xpath('.//p')
            for d in p:
                text = d.xpath('.//text()').getall()
                text_str = "".join(text).replace("\n", "")
                a += text_str + '\n'

        a = a.replace("\xa0", "")
        a = a.replace(" ", "")
        a = a.replace("&nbsp;", "")
        a = a.replace("\u3000", "")
        a = a.replace("\r", "")
        a = a.replace("\t", "")

        pName = re.findall('项目名称：(.*?)\s', a, re.S)
        if pName:
            pName = pName[0]
            pName = "".join(pName.split())
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
            entName = re.findall('采购人名称：(.*?)\s', a, re.S)
            if entName:
                entName = entName[0]
                entName = "".join(entName.split())
            else:
                entName = str(nums)


        pAddr = re.findall('项目地点：(.*?)\s', a, re.S)
        if pAddr:
            pAddr = pAddr[0]
            pAddr = "".join(pAddr.split())
        else:
            midpAddr = "(?s){}[\s]+地址：(.*?)\s".format(entName)
            pAddr = re.findall(midpAddr, a, re.S)
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
            pNo = re.findall('标段编号:(.*?)\s', a, re.S)
            if pNo:
                pNo = pNo[0]
                pNo = "".join(pNo.split())
            else:
                pNo = str(nums)


        pBudget = re.findall('预算金额：(.*?)\s', a, re.S)
        if pBudget:
            pBudget = pBudget[0]
            pBudget = "".join(pBudget.split())
        else:
            pBudget = re.findall('资金来源及项目投资估算额：(.*?)\s', a, re.S)
            if pBudget:
                pBudget = pBudget[0]
                pBudget = "".join(pBudget.split())
            else:
                pBudget = str(nums)

        if len(pBudget)>20:
            pBudget = str(nums)
        else:
            pBudget = pBudget


        midlinkman = re.findall('联系方式：(.*?)\s', a, re.S)
        if midlinkman:
            midlinkman = midlinkman[0]
            midlinkman = "".join(midlinkman.split())
            linkman = re.findall('[\u4e00-\u9fa5]+', midlinkman, re.S)
            if linkman:
                linkman = linkman[0]
                linkman = "".join(linkman.split())
            else:
                linkman = str(nums)
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

        if linkman:
            midtel = "(?s){}+,(.*?)\s".format(linkman)
            tel = re.findall(midtel, a, re.S)
            if tel:
                tel = tel[0]
                tel = "".join(tel.split())
            else:
                tel = str(nums)
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


        fax = re.findall('传真：(.*?)\s', a, re.S)
        if fax:
            fax = fax[0]
            fax = "".join(fax.split())
        else:
            fax = str(nums)

        if len(fax) > 20:
            fax = str(nums)
        else:
            fax = fax


        agentName = re.findall('招标代理机构：(.*?)\s', a, re.S)
        if agentName:
            agentName = agentName[0]
            agentName = "".join(agentName.split())
        else:
            agentName = re.findall('采购代理机构信息\s名称：(.*?)\s', a, re.S)
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
            agentAddr = re.findall('地址：(.*?)\s', a, re.S)
            if agentAddr:
                try:
                    agentAddr = agentAddr[1]
                    agentAddr = "".join(agentAddr.split())
                except Exception as e:
                    print('无', e)
                    agentAddr = str(nums)
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
                    print('无', e)
                    agentLinkman = str(nums)
                pass
            else:
                agentLinkman = str(nums)

        if len(agentLinkman) > 10:
            agentLinkman = str(nums)
        else:
            agentLinkman = agentLinkman


        midagentTel = re.findall('电话：(.*?)\s', a, re.S)
        if midagentTel:
            midagentTel = midagentTel[0]
            midagentTel = "".join(midagentTel.split())
            agentTel = re.findall(r'\d{4}-\d{7}|\d{3}-\d{8}|d{11}', a, re.S)
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
            try:
                agentFax = agentFax[1]
                agentFax = "".join(agentFax.split())
            except Exception as e:
                print('无', e)
                agentFax = str(nums)
            pass
        else:
            agentFax = str(nums)

        if len(agentFax) > 30:
            agentFax = str(nums)
        else:
            agentFax = agentFax


        bidTime = re.findall('开启\s时间：(.*?)\s', a, re.S)
        if bidTime:
            bidTime = bidTime[0]
            bidTime = "".join(bidTime.split())
        else:
            bidTime = re.findall('开标时间:(.*?)\s', a, re.S)
            if bidTime:
                bidTime = bidTime[0]
                bidTime = "".join(bidTime.split())
            else:
                bidTime = re.findall('提交投标文件截止时间、开标时间和地点\s(.*?)\s', a, re.S)
                if bidTime:
                    bidTime = bidTime[0]
                    bidTime = "".join(bidTime.split())
                else:
                    bidTime = str(nums)


        midbidAddr = "(?s){}[\s]+地点：(.*?)\s".format(bidTime)
        bidAddr = re.findall(midbidAddr, a, re.S)
        if bidAddr:
            bidAddr = bidAddr[0]
            bidAddr = "".join(bidAddr.split())
        else:
            bidAddr = re.findall('开标地点:(.*?)\s', a, re.S)
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
            getfileStartTime = re.findall('获取采购文件\s时间：(.*?)\s', a, re.S)
            if getfileStartTime:
                getfileStartTime = getfileStartTime[0]
                getfileStartTime = "".join(getfileStartTime.split())
            else:
                getfileStartTime = re.findall('获取竞争性磋商文件的时间：(.*?)\s', a, re.S)
                if getfileStartTime:
                    getfileStartTime = getfileStartTime[0]
                    getfileStartTime = "".join(getfileStartTime.split())
                else:
                    getfileStartTime = str(nums)

        if len(getfileStartTime) > 80:
            getfileStartTime = str(nums)
        else:
            getfileStartTime = getfileStartTime



        getfileTimeDesc = re.findall('公告期限\s(.*?)\s', a, re.S)
        if getfileTimeDesc:
            getfileTimeDesc = getfileTimeDesc[0]
            getfileTimeDesc = "".join(getfileTimeDesc.split())
        else:
            getfileTimeDesc = re.findall('递交投标文件的截止时间为(.*?)。', a, re.S)
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

        agentMobile = agentTel

        text = a

        getfileEndTime = ''

        prov = ''

        city = ''

        district = ''

        spider = 'beijing'

        source = '北京政府采购网'

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

        # print(item)

        yield item





if __name__ == '__main__':
    cmdline.execute("scrapy crawl beijing".split())