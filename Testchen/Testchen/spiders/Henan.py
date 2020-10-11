import json
import scrapy
from Testchen.items import TestchenItem
import re
from scrapy import cmdline, selector



class JiangxiSpider(scrapy.Spider):
    name = 'Jiangxi'
    allowed_domains = ['hndzzbtb.hndrc.gov.cn']
    start_urls = ['http://hndzzbtb.hndrc.gov.cn/services/hl/getSelect?response=application/json&pageIndex=1&pageSize=22&day=&sheng=x1&qu=&xian=&title=&timestart=&timeend=&categorynum=002001001&siteguid=3955b792-fb32-4dc1-8935-49ad516ae6db']


    def parse(self, response):
        # print(response.text)
        paydata = json.loads(response.text)

        data = paydata['return']

        data_json = json.loads(data)

        for i in data_json['Table']:
            # print('http://hndzzbtb.hndrc.gov.cn' + i['href'])

            sourceUrl ='http://hndzzbtb.hndrc.gov.cn' + i['href']

            yield scrapy.Request("http://hndzzbtb.hndrc.gov.cn" + i['href'],meta={'sourceUrl':sourceUrl}, callback=self.parse2)


        if 'num' in response.meta:
            x = int(response.meta['num'])
        else:
            x = 1
        if x<=2:
            x = x + 1
            print(x)
            url ="http://hndzzbtb.hndrc.gov.cn/services/hl/getSelect?response=application/json&pageIndex="+str(x)+"&pageSize=22&day=&sheng=x1&qu=&xian=&title=&timestart=&timeend=&categorynum=002001001&siteguid=3955b792-fb32-4dc1-8935-49ad516ae6db"
            # print(url)
            yield scrapy.Request(url,meta={'num':str(x)},callback=self.parse)



    def parse2(self, response):
            item = TestchenItem()
            sourceUrl = response.request.meta['sourceUrl']
            print(sourceUrl)
            #item['sourceUrl'] = sourceUrl
            nums = '无'
            a = ''
            content = response.xpath('//div[@class="ewb-container ewb-mt24"]')
            for node in content:
                p = node.xpath('.//p')

                for d in p:
                    text = d.xpath('.//text()').extract()
                    text_str = "".join(text).replace("\n", "")
                    a += text_str + '\n'

            a = a.replace("\xa0", "")
            a = a.replace(" ", "")
            a = a.replace("&nbsp", "")
            a = a.replace("建设地点：\n", "建设地点：")


            # print(a)

            pNo = re.findall('项目编号：(.*?)\n', a, re.S)
            if pNo:
                pNo = pNo[0]
                pNo = "".join(pNo.split())
            else:
                pNo = re.findall('工程编号：(.*?)\n', a, re.S)
                if pNo:
                    pNo = pNo[0]
                    pNo = "".join(pNo.split())
                else:
                    pNo = re.findall('招标编号：(.*?)\n|招标编号：[0-9A-Z]{7}-[0-9A-Z]{8}\n', a, re.S)
                    if pNo:
                        pNo = pNo[0]
                        pNo = "".join(pNo.split())
                    else:
                        pNo = re.findall('采购编号：(.*?)\n', a, re.S)
                        if pNo:
                            pNo = pNo[0]
                            pNo = "".join(pNo.split())
                        else:
                            pNo = str(nums)




            pName = re.findall('采购项目名称：：(.*?)\n', a, re.S)
            if pName:
                pName = pName[0]
                pName = "".join(pName.split())
            else:
                pName = re.findall('项目名称：(.*?)\n', a, re.S)
                if pName:
                    pName = pName[0]
                    pName = "".join(pName.split())
                else:
                    pName = re.findall('工程名称：(.*?)\n', a, re.S)
                    if pName:
                        pName = pName[0]
                        pName = "".join(pName.split())
                    else:
                        pName = re.findall('项目(.*?)已', a, re.S)
                        if pName:
                            pName = pName[0]
                            pName = "".join(pName.split())
                        else:
                            pName = str(nums)


            entName = re.findall('投标人：(.*?)\n', a, re.S)
            if entName:
                entName = entName[0]
                entName = "".join(entName.split())
            else:
                entName = str(nums)


            pAddr = re.findall('建设地点：(.*?)\n', a, re.S)
            if pAddr:
                pAddr = pAddr[0]
                pAddr = "".join(pAddr.split())
            else:
                pAddr = re.findall('工程地点：(.*?)\n', a, re.S)
                if pAddr:
                    pAddr = pAddr[0]
                    pAddr = "".join(pAddr.split())
                else:
                    pAddr = str(nums)


            pApprovalName = str(nums)

            pApproveOrg = str(nums)

            pSupervision = re.findall('行政监督部门：(.*?)\n', a, re.S)
            if pSupervision:
                pSupervision = pSupervision[0]
                pSupervision = "".join(pSupervision.split())
            pSupervision = str(nums)


            pubTime = str(nums)


            pBudget = re.findall('总投资：(.*?)\n', a, re.S)
            if pBudget:
                pBudget = pBudget[0]
                pBudget = "".join(pBudget.split())
            else:
                pBudget = re.findall('估算价：(.*?)\n', a, re.S)
                if pBudget:
                    pBudget = pBudget[0]
                    pBudget = "".join(pBudget.split())
                else:
                    pBudget = re.findall('招标控制价：(.*?)\n', a, re.S)
                    if pBudget:
                        pBudget = pBudget[0]
                        pBudget = "".join(pBudget.split())
                    else:
                        pBudget = re.findall('预算金额：(.*?)\n', a, re.S)
                        if pBudget:
                            pBudget = pBudget[0]
                            pBudget = "".join(pBudget.split())
                        else:
                            pBudget = re.findall('资金总额：(.*?)\n', a, re.S)
                            if pBudget:
                                pBudget = pBudget[0]
                                pBudget = "".join(pBudget.split())
                            else:
                                pBudget = re.findall('投资金额：(.*?)\n', a, re.S)
                                if pBudget:
                                    pBudget = pBudget[0]
                                    pBudget = "".join(pBudget.split())
                                else:
                                    pBudget = str(nums)


            linkman = re.findall('联系人：[\u3400-\u9FFF]{3}|联系人：[\u3400-\u9FFF]{2}', a, re.S)
            if linkman:
                linkman = linkman[0]
                linkman = "".join(linkman.split())
            else:
                linkman = re.findall('项目负责人：(.*?)\n', a, re.S)
                if linkman:
                    linkman = linkman[0]
                    linkman = "".join(linkman.split())
                else:
                    linkman = re.findall('联系人：(.*?)\n', a, re.S)
                    if linkman:
                        linkman = linkman[0]
                        linkman = "".join(linkman.split())
                    else:
                        linkman = str(nums)


            tel = re.findall('电话：(.*?)\n', a, re.S)
            if tel:
                tel = tel[0]
                tel = "".join(tel.split())
            else:
                tel = re.findall('联系方式：(.*?)\n', a, re.S)
                if tel:
                    tel = tel[0]
                    tel = "".join(tel.split())
                else:
                    tel = str(nums)

            Mobile = tel

            email = re.findall('电子邮件：(.*?)\n', a, re.S)
            if email:
                email = email[0]
                email = "".join(email.split())
            else:
                email = str(nums)


            fox = re.findall('传真：(.*?)\n', a, re.S)
            if fox:
                fox = fox[0]
                fox = "".join(fox.split())
            else:
                fox = str(nums)


            agentName = re.findall('招标代理机构：(.*?)\n', a, re.S)
            if agentName:
                agentName = agentName[0]
                agentName = "".join(agentName.split())
            else:
                agentName = str(nums)


            agentAddr = re.findall('地址：(.*?)\n', a, re.S)
            if agentAddr:
                agentAddr = agentAddr[1]
                agentAddr = "".join(agentAddr.split())
            else:
                agentAddr = re.findall('地点：(.*?)\n联系人', a, re.S)
                if agentAddr:
                    agentAddr = agentAddr[1]
                    agentAddr = "".join(agentAddr.split())
                else:
                    agentAddr = str(nums)


            agentLinkman = re.findall('联系人：[\u3400-\u9FFF]{3}|联系人：[\u3400-\u9FFF]{2}', a, re.S)
            if agentLinkman:
                agentLinkman = agentLinkman[1]
                agentLinkman = "".join(agentLinkman.split())
            else:
                agentLinkman = re.findall('项目负责人：(.*?)\n', a, re.S)
                if agentLinkman:
                    agentLinkman = agentLinkman[1]
                    agentLinkman = "".join(agentLinkman.split())
                else:
                    agentLinkman = re.findall('联系人：(.*?)\n', a, re.S)
                    if agentLinkman:
                        agentLinkman = agentLinkman[1]
                        agentLinkman = "".join(agentLinkman.split())
                    else:
                        agentLinkman = str(nums)



            agentTel = re.findall('电话：(.*?)\n', a, re.S)
            if agentTel:
                agentTel = agentTel[1]
                agentTel = "".join(agentTel.split())
            else:
                agentTel = re.findall('联系方式：(.*?)\n', a, re.S)
                if agentTel:
                    agentTel = agentTel[1]
                    agentTel = "".join(agentTel.split())
                else:
                    agentTel = str(nums)

            agentMobile = agentTel


            agentEmail = re.findall('电子邮件：(.*?)\n', a, re.S)
            if agentEmail:
                agentEmail = agentEmail[1]
                agentEmail = "".join(agentEmail.split())
            else:
                agentEmail = str(nums)


            agentFox = re.findall('传真：(.*?)\n', a, re.S)
            if agentFox:
                agentFox = agentFox[0]
                agentFox = "".join(agentFox.split())
            else:
                agentFox = str(nums)


            bidTime = re.findall('开标时间(.*?)分', a, re.S)
            if bidTime:
                bidTime = bidTime[0]
                bidTime = "".join(bidTime.split())
            else:
                bidTime = re.findall('开标时间：(.*?)\n', a, re.S)
                if bidTime:
                    bidTime = bidTime[0]
                    bidTime = "".join(bidTime.split())
                else:
                    bidTime = re.findall('开标时间及地点\n1.时间：(.*?)\n', a, re.S)
                    if bidTime:
                        bidTime = bidTime[0]
                        bidTime = "".join(bidTime.split())
                    else:
                        bidTime = str(nums)


            bidAddr = re.findall('线上开标地点：(.*?)。', a, re.S)
            if bidAddr:
                bidAddr = bidAddr[0]
                bidAddr = "".join(bidAddr.split())
            else:
                bidAddr = re.findall('开标地点：(.*?)\n', a, re.S)
                if bidAddr:
                    bidAddr = bidAddr[0]
                    bidAddr = "".join(bidAddr.split())
                else:
                    bidAddr = re.findall('分。地点(.*?)。', a, re.S)
                    if bidAddr:
                        bidAddr = bidAddr[0]
                        bidAddr = "".join(bidAddr.split())
                    else:
                        bidAddr = re.findall('，地点(.*?)。', a, re.S)
                        if bidAddr:
                            bidAddr = bidAddr[0]
                            bidAddr = "".join(bidAddr.split())
                        else:
                            bidAddr = '线上'




            getfileStartTime = re.findall('招标文件时间：(.*?)\n', a, re.S)
            if getfileStartTime:
                getfileStartTime = getfileStartTime[0]
                getfileStartTime = "".join(getfileStartTime.split())
            else:
                getfileStartTime = re.findall('文件出售时间：(.*?)\n', a, re.S)
                if getfileStartTime:
                    getfileStartTime = getfileStartTime[0]
                    getfileStartTime = "".join(getfileStartTime.split())
                else:
                    getfileStartTime = re.findall('凡有意参加投标者，请于(.*?)日', a, re.S)
                    if getfileStartTime:
                        getfileStartTime = getfileStartTime[0]
                        getfileStartTime = "".join(getfileStartTime.split())
                    else:
                        getfileStartTime = re.findall('获取磋商文件时间：(.*?)\n', a, re.S)
                        if getfileStartTime:
                            getfileStartTime = getfileStartTime[0]
                            getfileStartTime = "".join(getfileStartTime.split())
                        else:
                            getfileStartTime = re.findall('获取招标文件及报名时间\n1.时间：(.*?)\n', a, re.S)
                            if getfileStartTime:
                                getfileStartTime = getfileStartTime[0]
                                getfileStartTime = "".join(getfileStartTime.split())
                            else:
                                getfileStartTime = re.findall('招标文件获取时间：(.*?)\n', a, re.S)
                                if getfileStartTime:
                                    getfileStartTime = getfileStartTime[0]
                                    getfileStartTime = "".join(getfileStartTime.split())
                                else:
                                    getfileStartTime = str(nums)



            getfileEndTime = re.findall('获取时间(.*?)\n', a, re.S)
            if getfileEndTime:
                 getfileEndTime = getfileEndTime[0]
                 getfileEndTime = "".join(getfileEndTime.split())
            else:
                 getfileEndTime = str(nums)



            getfileTimeDesc = re.findall('投标文件递交的截止时间（投标截止时间，下同）(.*?)，', a, re.S)
            if getfileTimeDesc:
                 getfileTimeDesc = getfileTimeDesc[0]
                 getfileTimeDesc = "".join(getfileTimeDesc.split())
            else:
                getfileTimeDesc = re.findall('标文件递交的截止时间(开标时间)：(.*?)\n', a, re.S)
                if getfileTimeDesc:
                    getfileTimeDesc = getfileTimeDesc[0]
                    getfileTimeDesc = "".join(getfileTimeDesc.split())
                else:
                    getfileTimeDesc = re.findall('递交截止时间：(.*?)\n', a, re.S)
                    if getfileTimeDesc:
                        getfileTimeDesc = getfileTimeDesc[0]
                        getfileTimeDesc = "".join(getfileTimeDesc.split())
                    else:
                        getfileTimeDesc = str(nums)



            files = str(nums)

            text = a

            print(pName)                    # 项目名称

            print(entName)                  # 项目法人

            print(pAddr)                    # 项目地址

            print(pApprovalName)            # 项目批文名称

            print(pApproveOrg)              # 审批单位

            print(pSupervision)             # 监管部门

            print(pubTime)                  # 项目建立时间

            print(pNo)                      # 项目编号

            print(pBudget)                  # 项目预算

            print(linkman)                  # 招标人

            print(tel)                      # 联系电话

            print(Mobile)                   # 联系电话

            print(email)                    # 电子邮箱

            print(fox)                      # 传真

            print(agentName)                # 代理机构名称

            print(agentAddr)                # 代理机构地址

            print(agentLinkman)             # 代理机构联系人

            print(agentTel)                 # 代理机构电话

            print(agentMobile)              # 代理机构电话

            print(agentEmail)               # 代理机构电子邮箱

            print(agentFox)                 # 代理机构传真

            print(files)                    # 附件

            print(bidTime)                  # 开标时间

            print(bidAddr)                  # 开标地点

            print(getfileStartTime)         # 获取时间

            #print(getfileEndTime)          # 获取时间

            print(getfileTimeDesc)          # 时间说明

            #print(text)                     # 招标文本




if __name__ == '__main__':
    cmdline.execute("scrapy crawl Henan".split())