import json
from Testchen.items import TestchenItem
import scrapy
import re
from scrapy import cmdline, selector

class GuangdongSpider(scrapy.Spider):
    name = 'guangdong'

    def start_requests(self):
        url = 'http://www.gdgpo.gov.cn/queryMoreInfoList.do'
        # FormRequest 是Scrapy发送POST请求的方法
        yield scrapy.FormRequest(
            url = url,
            formdata={'channelCode':'000501',
                      'issueOrgan':'',
                      'operateDateFrom':'2016-10-01',
                      'operateDateTo':'2020-10-01',
                      'performOrgName':'',
                      'pointPageIndexId':'1',
                      'poor':'',
                      'purchaserOrgName':'',
                      'regionIds':'',
                      'sitewebId':'4028889705bebb510105bec068b00003',
                      'sitewebName':'省直',
                      'stockIndexName':'',
                      'stockNum': '',
                      'stockTypes': '',
                      'title': '',
                      'pageIndex': '1',
                      'pageSize':'30',
                      'pointPageIndexId':''
                      },
            callback = self.parse
        )

    def parse(self, response, **kwargs):
        # print(response.text)
        a = response.xpath('//div[@class="m_m_cont"]/ul')
        for node in a:
            url = node.xpath('./li/a/@href').extract()
            for c in url:
                sourceUrl = 'http://www.gdgpo.gov.cn'+c
                yield scrapy.Request(sourceUrl, meta={'sourceUrl': sourceUrl}, callback=self.parse2)


        if 'num' in response.meta:
            x = int(response.meta['num'])
        else:
            x = 1
        if x < 36:
            x = x + 1

            url = 'http://www.gdgpo.gov.cn/queryMoreInfoList.do'
            # FormRequest 是Scrapy发送POST请求的方法
            yield scrapy.FormRequest(
                url=url,
                formdata={'channelCode': '000501',
                          'issueOrgan': '',
                          'operateDateFrom': '2016-10-01',
                          'operateDateTo': '2020-10-01',
                          'performOrgName': '',
                          'pointPageIndexId': '1',
                          'poor': '',
                          'purchaserOrgName': '',
                          'regionIds': '',
                          'sitewebId': '4028889705bebb510105bec068b00003',
                          'sitewebName': '省直',
                          'stockIndexName': '',
                          'stockNum': '',
                          'stockTypes': '',
                          'title': '',
                          'pageIndex': str(x),
                          'pageSize': '30',
                          'pointPageIndexId': ''
                          },
                callback=self.parse,meta={'num': str(x)}
            )

    def parse2(self, response):
        item = TestchenItem()
        sourceUrl = response.request.meta['sourceUrl']
        item['sourceUrl'] = sourceUrl
        print(item)

    # def parse2(self, response):
    #     item = TestchenItem()
    #     sourceUrl = response.request.meta['sourceUrl']
    #     a = ''
    #     nums = ''
    #
    #     content = response.xpath('//div[@class="zw_c_c_cont"]')
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
    #         entName = str(nums)
    #
    #     midpAddr = "(?s){}[\s]+地址：(.*?)\s".format(entName)
    #     pAddr = re.findall(midpAddr, a, re.S)
    #     if pAddr:
    #         pAddr = pAddr[0]
    #         pAddr = "".join(pAddr.split())
    #     else:
    #         pAddr = str(nums)
    #
    #
    #     pNo = re.findall('项目编号：(.*?)\s', a, re.S)
    #     if pNo:
    #         pNo = pNo[0]
    #         pNo = "".join(pNo.split())
    #     else:
    #         pNo = str(nums)
    #
    #
    #     pBudget = re.findall('预算金额：(.*?)\s', a, re.S)
    #     if pBudget:
    #         pBudget = pBudget[0]
    #         pBudget = "".join(pBudget.split())
    #         pBudget = pBudget + '元'
    #     else:
    #         pBudget = str(nums)
    #
    #
    #     linkman = re.findall('项目联系人：(.*?)\s', a, re.S)
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
    #
    #     midtel = "(?s){}[\s]+联系方式：(.*?)\s".format(pAddr)
    #     tel = re.findall(midtel, a, re.S)
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
    #
    #     agentName = re.findall('采购代理机构信息\s名称：(.*?)\s', a, re.S)
    #     if agentName:
    #         agentName = agentName[0]
    #         agentName = "".join(agentName.split())
    #     else:
    #         agentName = str(nums)
    #
    #
    #     midagentAddr = "(?s){}[\s]+地址：(.*?)\s".format(agentName)
    #     agentAddr = re.findall(midagentAddr, a, re.S)
    #     if agentAddr:
    #             agentAddr = agentAddr[0]
    #             agentAddr = "".join(agentAddr.split())
    #     else:
    #         agentAddr = str(nums)
    #
    #     if len(agentAddr) > 50:
    #         agentAddr = str(nums)
    #     else:
    #         agentAddr = agentAddr
    #
    #
    #     agentLinkman = re.findall('项目联系人：(.*?)\s', a, re.S)
    #     if agentLinkman:
    #             agentLinkman = agentLinkman[0]
    #             agentLinkman = "".join(agentLinkman.split())
    #     else:
    #         agentLinkman = str(nums)
    #
    #     if len(agentLinkman) > 10:
    #         agentLinkman = str(nums)
    #     else:
    #         agentLinkman = agentLinkman
    #
    #
    #     midagentTel = "(?s){}[\s]+联系方式：(.*?)\s".format(agentAddr)
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
    #     bidTime = re.findall('提交投标文件截止时间、开标时间和地点\s(.*?)\s', a, re.S)
    #     if bidTime:
    #         bidTime = bidTime[0]
    #         bidTime = "".join(bidTime.split())
    #     else:
    #         bidTime = str(nums)
    #
    #
    #     midtel = "(?s){}[\s]+地点：(.*?)\s".format(bidTime)
    #     bidAddr = re.findall(midtel, a, re.S)
    #     if bidAddr:
    #         bidAddr = bidAddr[0]
    #         bidAddr = "".join(bidAddr.split())
    #     else:
    #         bidAddr = str(nums)
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
    #         getfileStartTime = str(nums)
    #
    #
    #     getfileTimeDesc = re.findall('公告期限\s(.*?)\s', a, re.S)
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
    #     email = ''
    #
    #     fax = ''
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
    #     spider = 'guangdong'
    #
    #     source = '广东省政府采购网'
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
    cmdline.execute("scrapy crawl guangdong".split())