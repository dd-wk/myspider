import json
import scrapy
import re
from scrapy import cmdline, selector
from Testchen.items import TestchenItem


class HunanSpider(scrapy.Spider):
    name = 'hunan'
    start_urls = ['https://www.hnsggzy.com/queryContent_20-jygk.jspx?title=&origin=&inDates=&channelId=845&ext=%E6%8B%9B%E6%A0%87/%E8%B5%84%E5%AE%A1%E5%85%AC%E5%91%8A&beginTime=&endTime=']

    def parse(self, response, **kwargs):
        a = response.xpath('//div[@class="article-content"]/ul/li')
        for node in a:
            url = node.xpath('./div/a/@href').extract()
            for c in url:
                sourceUrl = c
                yield scrapy.Request(sourceUrl, meta={'sourceUrl':sourceUrl}, callback=self.parse2)


        if 'num' in response.meta:
            x = int(response.meta['num'])
        else:
            x = 20
        if x < 40:
            x = x + 1
            url = "https://www.hnsggzy.com/queryContent_" + str(x) + "-jygk.jspx?title=&origin=&inDates=&channelId=845&ext=%E6%8B%9B%E6%A0%87/%E8%B5%84%E5%AE%A1%E5%85%AC%E5%91%8A&beginTime=&endTime="
            yield scrapy.Request(url, meta={'num': str(x)}, callback=self.parse)


    def parse2(self, response):
        item = TestchenItem()
        sourceUrl = response.request.meta['sourceUrl']
        a = ''
        nums = ''
        content = response.xpath('//div[@class="content-article"]')
        for node in content:
            p = node.xpath('./div//p')
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

        pName = re.findall('工程名称：(.*?)\s', a, re.S)
        if pName:
            pName = pName[0]
            pName = "".join(pName.split())
        else:
            pName = re.findall('项目名称：(.*?)\s', a, re.S)
            if pName:
                pName = pName[0]
                pName = "".join(pName.split())
            else:
                pName = re.findall('项目名称:(.*?)\s', a, re.S)
                if pName:
                    pName = pName[0]
                    pName = "".join(pName.split())
                else:
                    pName = re.findall('\）名称：(.*?)\s', a, re.S)
                    if pName:
                        pName = pName[0]
                        pName = "".join(pName.split())
                    else:
                        pName = str(nums)

        if len(pName) > 50:
            pName = str(nums)
        else:
            pName = pName

        entName = re.findall('招标人：(.*?)\s', a, re.S)
        if entName:
            entName = entName[0]
            entName = "".join(entName.split())
        else:
            entName = re.findall('采购人：(.*?)\s', a, re.S)
            if entName:
                entName = entName[0]
                entName = "".join(entName.split())
            else:
                entName = re.findall('招标人：\s(.*?)\s地址', a, re.S)
                if entName:
                    entName = entName[0]
                    entName = "".join(entName.split())
                else:
                    entName = str(nums)



        pAddr = re.findall('建设地点：(.*?)\s', a, re.S)
        if pAddr:
            pAddr = pAddr[0]
            pAddr = "".join(pAddr.split())
        else:
            pAddr = str(nums)

        pNo = re.findall('招标代理编号：(.*?)\s', a, re.S)
        if pNo:
            pNo = pNo[0]
            pNo = "".join(pNo.split())
        else:
            pNo = re.findall('招标编号：(.*?)\s', a, re.S)
            if pNo:
                pNo = pNo[0]
                pNo = "".join(pNo.split())
            else:
                pNo = str(nums)

        pBudget = re.findall('招标金额为(.*?)元', a, re.S)
        if pBudget:
            pBudget = pBudget[0]
            pBudget = "".join(pBudget.split())
            pBudget = pBudget + '元'
        else:
            pBudget = re.findall('项目总投资(.*?)元', a, re.S)
            if pBudget:
                pBudget = pBudget[0]
                pBudget = "".join(pBudget.split())
                pBudget = pBudget + '元'
            else:
                pBudget = str(nums)

        linkman = re.findall('联系人:(.*?)\s', a, re.S)
        if linkman:
            linkman = linkman[0]
            linkman = "".join(linkman.split())
        else:
            linkman = re.findall('联系人：(.*?)\s', a, re.S)
            if linkman:
                linkman = linkman[0]
                linkman = "".join(linkman.split())
            else:
                linkman = re.findall('联系人：\s(.*?)\s电话', a, re.S)
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
            midtel = "(?s){}[\s]+电话：(.*?)\s".format(linkman)
            tel = re.findall(midtel, a, re.S)
            if tel:
                tel = tel[0]
                tel = "".join(tel.split())
            else:
                tel = str(nums)
        else:
            tel = str(nums)


        if tel == str(nums):
            tel = re.findall('电话：(.*?)\s', a, re.S)
            if tel:
                tel = tel[0]
                tel = "".join(tel.split())
            else:
                tel = re.findall('电话：\s(.*?)\s传真', a, re.S)
                if tel:
                    tel = tel[0]
                    tel = "".join(tel.split())
                else:
                    tel = str(nums)
        else:
            tel = tel

        if len(tel) > 20:
            tel = str(nums)
        else:
            tel = tel


        agentName = re.findall('招标代理机构：(.*?)\s', a, re.S)
        if agentName:
            agentName = agentName[0]
            agentName = "".join(agentName.split())
        else:
            agentName = re.findall('代理机构：(.*?)\s', a, re.S)
            if agentName:
                agentName = agentName[0]
                agentName = "".join(agentName.split())
            else:
                agentName = re.findall('代理机构：\s(.*?)\s地址', a, re.S)
                if agentName:
                    agentName = agentName[0]
                    agentName = "".join(agentName.split())
                else:
                    agentName = str(nums)

        agentAddr = re.findall('地址：(.*?)\s', a, re.S)
        if agentAddr:
            try:
                agentAddr = agentAddr[1]
                agentAddr = "".join(agentAddr.split())
            except Exception as e:
                print('无', e)
                agentAddr = re.findall('地址：(.*?)\s', a, re.S)
                if agentAddr:
                    agentAddr = agentAddr[0]
                    agentAddr = "".join(agentAddr.split())
                else:
                    agentAddr = str(nums)
            pass
        else:
            agentAddr = str(nums)

        if len(agentAddr) > 50:
            agentAddr = str(nums)
        else:
            agentAddr = agentAddr

        agentLinkman = re.findall('联系人：(.*?)\s', a, re.S)
        if agentLinkman:
            try:
                agentLinkman = agentLinkman[1]
                agentLinkman = "".join(agentLinkman.split())
            except Exception as e:
                print('无', e)
                agentLinkman = re.findall('联系人:(.*?)\s', a, re.S)
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
            pass
        else:
            agentLinkman = str(nums)

        if agentLinkman != str(nums):
            agentLinkman = agentLinkman
        else:
            agentLinkman = re.findall('联系人：(.*?)\s', a, re.S)
            if agentLinkman:
                try:
                    agentLinkman = agentLinkman[0]
                    agentLinkman = "".join(agentLinkman.split())
                except Exception as e:
                    print('无', e)
                    agentLinkman = re.findall('联系人:(.*?)\s', a, re.S)
                    if agentLinkman:
                        try:
                            agentLinkman = agentLinkman[0]
                            agentLinkman = "".join(agentLinkman.split())
                        except Exception as e:
                            print('无', e)
                            agentLinkman = str(nums)
                        pass
                    else:
                        agentLinkman = str(nums)
                pass
            else:
                agentLinkman = str(nums)

        if len(agentLinkman) > 10:
            agentLinkman = str(nums)
        else:
            agentLinkman = agentLinkman

        if agentLinkman:
            midagentTel = "(?s){}[\s]+电话：(.*?)\s".format(agentLinkman)
            agentTel = re.findall(midagentTel, a, re.S)
            if agentTel:
                agentTel = agentTel[0]
                agentTel = "".join(agentTel.split())
            else:
                agentTel = re.findall('联系方式：(.*?)\s', a, re.S)
                if agentTel:
                    try:
                        agentTel = agentTel[1]
                        agentTel = "".join(agentTel.split())
                    except Exception as e:
                        print('无', e)
                        agentTel = re.findall('联系方式：(.*?)\s', a, re.S)
                        if agentTel:
                            agentTel = agentTel[0]
                            agentTel = "".join(agentTel.split())
                        else:
                            agentTel = str(nums)
                    pass
                else:
                    agentTel = re.findall('电话：(.*?)\s', a, re.S)
                    if agentTel:
                        try:
                            agentTel = agentTel[1]
                            agentTel = "".join(agentTel.split())
                        except Exception as e:
                            print('无', e)
                            agentTel = re.findall('电话：(.*?)\s', a, re.S)
                            if agentTel:
                                agentTel = agentTel[0]
                                agentTel = "".join(agentTel.split())
                            else:
                                agentTel = str(nums)
                        pass
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
            agentFax = agentFax.replace('传真：', '')
        else:
            agentFax = str(nums)

        if len(agentFax) > 30:
            agentFax = str(nums)
        else:
            agentFax = agentFax

        bidTime = re.findall('开标时间(.*?)分', a, re.S)
        if bidTime:
            bidTime = bidTime[0]
            bidTime = "".join(bidTime.split())
            bidTime = bidTime.replace("：", "")
            bidTime = bidTime + '分'
        else:
            bidTime = re.findall('，下同\）(.*?)分', a, re.S)
            if bidTime:
                bidTime = bidTime[0]
                bidTime = "".join(bidTime.split())
                bidTime = bidTime + '分'
            else:
                bidTime = str(nums)

        if len(bidTime) > 50:
            bidTime = str(nums)
        else:
            bidTime = bidTime

        bidAddr = re.findall('开标地点：(.*?)，', a, re.S)
        if bidAddr:
            bidAddr = bidAddr[0]
            bidAddr = "".join(bidAddr.split())
        else:
            bidAddr = re.findall('递交地点为(.*?)\s', a, re.S)
            if bidAddr:
                bidAddr = bidAddr[0]
                bidAddr = "".join(bidAddr.split())
            else:
                bidAddr = str(nums)

        if len(bidAddr) > 70:
            bidAddr = str(nums)
        else:
            bidAddr = bidAddr

        getfileStartTime = re.findall('请于(.*?)止', a, re.S)
        if getfileStartTime:
            getfileStartTime = getfileStartTime[0]
            getfileStartTime = "".join(getfileStartTime.split())
        else:
            getfileStartTime = re.findall('投标人从(.*?)止', a, re.S)
            if getfileStartTime:
                getfileStartTime = getfileStartTime[0]
                getfileStartTime = "".join(getfileStartTime.split())
            else:
                getfileStartTime = re.findall('请从(.*?)\（北京时间', a, re.S)
                if getfileStartTime:
                    getfileStartTime = getfileStartTime[0]
                    getfileStartTime = "".join(getfileStartTime.split())
                else:
                    getfileStartTime = re.findall('请从(.*?)分', a, re.S)
                    if getfileStartTime:
                        getfileStartTime = getfileStartTime[0]
                        getfileStartTime = "".join(getfileStartTime.split())
                        getfileStartTime = getfileStartTime + '分'
                    else:
                        getfileStartTime = str(nums)

        if len(getfileStartTime) > 50:
            getfileStartTime = str(nums)
        else:
            getfileStartTime = getfileStartTime

        getfileTimeDesc = re.findall('开标时间(.*?)分', a, re.S)
        if getfileTimeDesc:
            getfileTimeDesc = getfileTimeDesc[0]
            getfileTimeDesc = "".join(getfileTimeDesc.split())
            getfileTimeDesc = getfileTimeDesc.replace("：", "")
            getfileTimeDesc = getfileTimeDesc + '分'
        else:
            getfileTimeDesc = re.findall('，下同\）(.*?)分', a, re.S)
            if getfileTimeDesc:
                getfileTimeDesc = getfileTimeDesc[0]
                getfileTimeDesc = "".join(getfileTimeDesc.split())
                getfileTimeDesc = getfileTimeDesc + '分'
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

        prov = ''

        city = ''

        district = ''

        spider = 'hunan'

        source = ' 湖南省公共资源交易服务平台'

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

        # print(item)

        yield item


if __name__ == '__main__':
    cmdline.execute("scrapy crawl hunan".split())