import json
from Testchen.items import TestchenItem
import scrapy
import re
from scrapy import cmdline, selector

class ShandongSpider(scrapy.Spider):
    name = 'Shandong'
    # allowed_domains = ['ccgp-shandong.gov.cn']
    # start_urls = ['http://www.ccgp-shandong.gov.cn/sdgp2017/site/listnew.jsp']

    def start_requests(self):
        url = 'http://www.ccgp-shandong.gov.cn/sdgp2017/site/listnew.jsp'
        # FormRequest 是Scrapy发送POST请求的方法
        yield scrapy.FormRequest(
            url = url,
            formdata={'subject':'', 'pdate':'','kindof':'','unitname':'', 'projectname':'', 'projectcode':'','colcode':'0301','curpage':'1', 'grade':'province','firstpage':'1'},
            callback = self.parse
        )

    def parse(self, response, **kwargs):
        print(response.text)
        a = response.xpath('//ul[@class="news_list2"]/li')
        for node in a:
            url = node.xpath('./span/span/a/@href').extract()
            for c in url:
                sourceUrl = 'http://www.ccgp-shandong.gov.cn'+c
                yield scrapy.Request(sourceUrl, meta={'sourceUrl': sourceUrl}, callback=self.parse2)


        if 'num' in response.meta:
            x = int(response.meta['num'])
        else:
            x = 1
        if x < 2:
            x = x + 1

            url = 'http://www.ccgp-shandong.gov.cn/sdgp2017/site/listnew.jsp'
            # FormRequest 是Scrapy发送POST请求的方法
            yield scrapy.FormRequest(
                url=url,
                formdata={'subject': '', 'pdate': '', 'kindof': '', 'unitname': '', 'projectname': '',
                          'projectcode': '', 'colcode': '0301', 'curpage': str(x), 'grade': 'province', 'firstpage': '1'},
                callback=self.parse,meta={'num': str(x)}
            )


    def parse2(self, response):
        item = TestchenItem()
        sourceUrl = response.request.meta['sourceUrl']
        print(sourceUrl)






    # def parse2(self, response):
    #     item = TestchenItem()
    #     sourceUrl = response.request.meta['sourceUrl']
    #     a = ''
    #     nums = '无'
    #
    #     content = response.xpath('//div[@id="textarea"]/table')
    #     for node in content:
    #         p = node.xpath('.//tr')
    #         for d in p:
    #             text = d.xpath('./td//text()').getall()
    #             text_str = "".join(text).replace("\n", "")
    #             a += text_str + '\n'
    #
    #     a = a.replace("\xa0", "")
    #     a = a.replace(" ", "")
    #     a = a.replace("&nbsp", "")
    #     a = a.replace("\t", "")
    #     a = a.replace("\r", "")
    #     a = a.replace("项目编号：", "\n项目编号：")
    #     a = a.replace("地址：", "\n地址：")
    #     a = a.replace("联系方式：", "\n联系方式：")
    #     a = a.replace("联系电话：", "\n联系电话：")
    #     a = a.replace("传真：", "\n传真：")
    #     a = a.replace("谈判地点：", "\n谈判地点：")
    #     a = a.replace("开标地点：", "\n谈开标地点：")
    #
    #
    #     pName = re.findall('项目名称：(.*?)\n', a, re.S)
    #     if pName:
    #         pName = pName[0]
    #         pName = "".join(pName.split())
    #     else:
    #         pName = str(nums)
    #
    #
    #     # entName = str(nums)
    #
    #
    #     pAddr = re.findall('地址：(.*?)\n', a, re.S)
    #     if pAddr:
    #         pAddr = pAddr[0]
    #         pAddr = "".join(pAddr.split())
    #     else:
    #         pAddr = str(nums)
    #
    #
    #     pApprovalName = str(nums)
    #
    #     pApproveOrg = str(nums)
    #
    #     pSupervision = str(nums)
    #
    #     pubTime = str(nums)
    #
    #
    #     pNo = re.findall('采购项目编号（采购计划编号）：(.*?)\n', a, re.S)
    #     if pNo:
    #         pNo = pNo[0]
    #         pNo = "".join(pNo.split())
    #     else:
    #         pNo = re.findall('项目编号：(.*?)\n', a, re.S)
    #         if pNo:
    #             pNo = pNo[0]
    #             pNo = "".join(pNo.split())
    #         else:
    #             pNo = str(nums)
    #
    #
    #
    #     pBudget = re.findall('[0-9]{1,3}\.[0-9]{1,6}\n', a, re.S)
    #     if pBudget:
    #         pBudget = pBudget[0]
    #         pBudget = "".join(pBudget.split())
    #     else:
    #         pBudget = str(nums)
    #
    #
    #
    #     linkman = re.findall('联系人：(.*?)\n', a, re.S)
    #     if linkman:
    #         linkman = linkman[0]
    #         linkman = "".join(linkman.split())
    #     else:
    #         linkman = str(nums)
    #
    #
    #
    #     pattern = "(?s){}[\s]+联系电话：(.*?)\s".format(linkman.replace("(","\(").replace(")","\)"))
    #     tel = re.findall(pattern, a, re.S)
    #     if tel:
    #         tel = tel[0]
    #         tel = "".join(tel.split())
    #     else:
    #         pattern = "(?s){}[\s]+联系方式：(.*?)\s".format(linkman.replace("(","\(").replace(")","\)"))
    #         tel = re.findall(pattern, a, re.S)
    #         if tel:
    #             tel = tel[0]
    #             tel = "".join(tel.split())
    #         else:
    #             tel = str(nums)
    #
    #
    #
    #
    #     mobile = str(nums)
    #
    #
    #     email = re.findall('邮箱：(.*?)\n', a, re.S)
    #     if email:
    #         email = email[0]
    #         email = "".join(email.split())
    #     else:
    #         email = str(nums)
    #
    #
    #
    #     fox = re.findall('传真：(.*?)\n', a, re.S)
    #     if fox:
    #         fox = fox[0]
    #         fox = "".join(fox.split())
    #     else:
    #         fox = str(nums)
    #
    #
    #     agentName = re.findall('代理机构：(.*?)\n', a, re.S)
    #     if agentName:
    #         agentName = agentName[0]
    #         agentName = "".join(agentName.split())
    #     else:
    #         agentName = str(nums)
    #
    #
    #     parent = "(?s){}[\n]+地址：(.*?)\n".format(agentName)
    #     agentAddr = re.findall(parent, a, re.S)
    #     if agentAddr:
    #         agentAddr = agentAddr[0]
    #         agentAddr = "".join(agentAddr.split())
    #     else:
    #         agentAddr = str(nums)
    #
    #
    #
    #     lx = "(?s){}[\s]+联系人：(.*?)\s".format(agentAddr)
    #     agentLinkman = re.findall(lx, a, re.S)
    #     if agentLinkman:
    #             agentLinkman = agentLinkman[0]
    #             agentLinkman = "".join(agentLinkman.split())
    #     else:
    #         lx = "(?s){}[\s]+联系方式：(.*?)\s".format(agentAddr)
    #         mid = re.findall(lx, a, re.S)
    #         if mid:
    #             mid = mid[0]
    #             mid = "".join(mid.split())
    #             agentLinkman= re.findall(r'[\u4e00-\u9fa5]+',mid, re.S)
    #             if agentLinkman:
    #                 agentLinkman = agentLinkman[0]
    #                 agentLinkman = "".join(agentLinkman.split())
    #             else:
    #                 agentLinkman = str(nums)
    #         else:
    #            agentLinkman = str(nums)
    #
    #
    #
    #     pll = "(?s){}[\s]+联系电话：(.*?)\s".format(agentAddr)
    #     agentTel = re.findall(pll, a, re.S)
    #     if agentTel:
    #         agentTel = agentTel[0]
    #         agentTel = "".join(agentTel.split())
    #     else:
    #         pll = "(?s){}[\s]+联系方式：(.*?)\s".format(agentAddr)
    #         agentTel = re.findall(pll, a, re.S)
    #         if agentTel:
    #             agentTel = agentTel[0]
    #             agentTel = "".join(agentTel.split())
    #             agentTel = agentTel.replace(agentLinkman,"")
    #         else:
    #             pll = "(?s){}[\s]+联系方式：(.*?)\s".format(agentLinkman.replace("(","\(").replace(")","\)"))
    #             agentTel = re.findall(pll, a, re.S)
    #             if agentTel:
    #                 agentTel = agentTel[0]
    #                 agentTel = "".join(agentTel.split())
    #                 agentTel = agentTel.replace(agentLinkman, "")
    #             else:
    #                     agentTel = str(nums)
    #
    #
    #     agentMobile = str(nums)
    #     agentEmail = str(nums)
    #     agentFox = str(nums)
    #
    #
    #     bidTime = re.findall("磋商时间及地点\n1.时间：(.*?)2.地点：", a, re.S)
    #     if bidTime:
    #         bidTime = bidTime[0]
    #         bidTime = "".join(bidTime.split())
    #     else:
    #         bidTime = re.findall("开标时间及地点\n1.时间：(.*?)2.地点：", a, re.S)
    #         if bidTime:
    #             bidTime = bidTime[0]
    #             bidTime = "".join(bidTime.split())
    #         else:
    #             bidTime = re.findall("谈判（开启）时间及地点\n1.时间：(.*?)2.地点：", a, re.S)
    #             if bidTime:
    #                 bidTime = bidTime[0]
    #                 bidTime = "".join(bidTime.split())
    #             else:
    #                 bidTime = re.findall("公开报价时间：(.*?)谈判地点：", a, re.S)
    #                 if bidTime:
    #                     bidTime = bidTime[0]
    #                     bidTime = "".join(bidTime.split())
    #                 else:
    #                     bidTime = re.findall("开标日期：(.*?)开标地点：", a, re.S)
    #                     if bidTime:
    #                         bidTime = bidTime[0]
    #                         bidTime = "".join(bidTime.split())
    #                     else:
    #                         bidTime = str(nums)
    #
    #
    #
    #     kbtime = "(?s){}[\s]+2.地点：(.*?)\s".format(bidTime.replace("(","\(").replace(")","\)"))
    #     bidAddr = re.findall(kbtime ,a, re.S)
    #     if bidAddr:
    #         bidAddr = bidAddr[0]
    #         bidAddr = "".join(bidAddr.split())
    #     else:
    #         kbtime = "(?s){}[\s]+开标地点：(.*?)\s".format(bidTime.replace("(", "\(").replace(")", "\)"))
    #         bidAddr = re.findall(kbtime, a, re.S)
    #         if bidAddr:
    #             bidAddr = bidAddr[0]
    #             bidAddr = "".join(bidAddr.split())
    #         else:
    #             kbtime = "(?s){}[\s]+谈判地点：(.*?)\s".format(bidTime.replace("(", "\(").replace(")", "\)"))
    #             bidAddr = re.findall(kbtime, a, re.S)
    #             if bidAddr:
    #                 bidAddr = bidAddr[0]
    #                 bidAddr = "".join(bidAddr.split())
    #             else:
    #                 bidAddr = re.findall('开标地点：(.*?)\s', a, re.S)
    #                 if bidAddr:
    #                     bidAddr = bidAddr[0]
    #                     bidAddr = "".join(bidAddr.split())
    #
    #
    #
    #     getfileStartTime = re.findall('获取磋商文件\n1.时间：(.*?)\n', a, re.S)
    #     if getfileStartTime:
    #         getfileStartTime = getfileStartTime[0]
    #         getfileStartTime = "".join(getfileStartTime.split())
    #     else:
    #         getfileStartTime = re.findall('获取招标文件\n1.时间：(.*?)\n', a, re.S)
    #         if getfileStartTime:
    #             getfileStartTime = getfileStartTime[0]
    #             getfileStartTime = "".join(getfileStartTime.split())
    #         else:
    #             getfileStartTime = re.findall('获取谈判文件\n1.时间：(.*?)\n', a, re.S)
    #             if getfileStartTime:
    #                 getfileStartTime = getfileStartTime[0]
    #                 getfileStartTime = "".join(getfileStartTime.split())
    #             else:
    #                 getfileStartTime = re.findall('接受报价起止时间：(.*?)\n', a, re.S)
    #                 if getfileStartTime:
    #                     getfileStartTime = getfileStartTime[0]
    #                     getfileStartTime = "".join(getfileStartTime.split())
    #                 else:
    #                     getfileStartTime = re.findall('时间：(.*?)方式', a, re.S)
    #                     if getfileStartTime:
    #                         getfileStartTime = getfileStartTime[0]
    #                         getfileStartTime = "".join(getfileStartTime.split())
    #                     else:
    #                         getfileStartTime = str(nums)
    #
    #
    #
    #
    #     getfileEndTime = str(nums)
    #
    #     getfileTimeDesc = str(nums)
    #
    #     text = a
    #
    #
    #     print(sourceUrl)               # url
    #
    #     print(pName)                   # 项目名称
    #
    #     print(pAddr)                   # 项目地址
    #
    #     print(pNo)                     # 项目编号
    #
    #     print(pBudget)                 # 项目预算
    #
    #     print(linkman)                 # 招标人
    #
    #     print(tel)                     # 联系电话
    #
    #     print(email)                 # 电子邮箱
    #
    #     print(fox)                     # 传真
    #
    #     print(agentName)               # 代理机构名称
    #
    #     print(agentAddr)               # 代理机构地址
    #
    #     print(agentLinkman)            # 代理机构联系人
    #
    #     print(agentTel)                # 代理机构电话
    #
    #     print(bidTime)                 # 开标时间
    #
    #     print(bidAddr)                 # 开标地点
    #
    #     print(getfileStartTime)        # 获取时间
    #
    #     print(text)                    # 招标文本
    #
    #
    #     item['sourceUrl'] = sourceUrl                  #url
    #
    #     item['pName'] = pName                          #项目名称
    #
    #     item['pAddr'] = pAddr                          #项目地址
    #
    #     item['pNo'] = pNo                              #项目编号
    #
    #     item['pBudget'] = pBudget                      #项目预算
    #
    #     item['linkman'] = linkman                      #招标人
    #
    #     item['tel'] = tel                              #联系电话
    #
    #     # item['mobile'] = mobile                        #联系电话
    #
    #     item['email'] = email                          # 邮箱
    #
    #     item['fox'] = fox                              #传真
    #
    #     item['agentName'] = agentName                  #代理机构名称
    #
    #     item['agentAddr'] = agentAddr                  #代理机构地址
    #
    #     item['agentLinkman'] = agentLinkman            #代理机构联系人
    #
    #     item['agentTel'] = agentTel                    #代理机构电话
    #
    #     # item['agentMobile'] = agentMobile              #代理机构电话
    #
    #     item['bidTime'] = bidTime                      #开标时间
    #
    #     item['bidAddr'] = bidAddr                      #开标地点
    #
    #     item['getfileStartTime'] = getfileStartTime    #获取时间
    #
    #     # item['getfileEndTime'] = getfileEndTime        #获取时间
    #
    #     # item['getfileTimeDesc'] = getfileTimeDesc      #时间说明
    #
    #     item['text'] = text                            #招标文本







if __name__ == '__main__':
    cmdline.execute("scrapy crawl Shandong".split())



