from Testchen.items import TestchenItem
import scrapy
import re
from scrapy import cmdline, selector,Request

class HebeiSpider(scrapy.Spider):
    name = 'Hebei'
    # allowed_domains = ['ccgp-hebei.gov.cn']
    # start_urls = ['http://search.hebcz.cn:8080/was5/web/search?page=1&channelid=240117&perpage=50&outlinepage=10&lanmu=zbgg']


    def start_requests(self):
        start_urls = 'http://search.hebcz.cn:8080/was5/web/search?page=2001&channelid=240117&perpage=50&outlinepage=10&lanmu=zbgg'
        yield Request(
            url=start_urls,
            callback=self.parse,
            dont_filter=True
        )



    def parse(self, response):
        a = response.xpath('//div[@class="outline"]/table')
        for node in a:
            url = node.xpath('.//tr/td[2]/a/@href').extract()
            for c in url:
                sourceUrl = c
                yield scrapy.Request(sourceUrl, meta={'sourceUrl':sourceUrl}, callback=self.parse2)


        if 'num' in response.meta:
            x = int(response.meta['num'])
        else:
            x = 2001

        # if x<2:
        if x<5085:
            x = x + 1
            # print(x)
            url ="http://search.hebcz.cn:8080/was5/web/search?page="+str(x)+"&channelid=240117&perpage=50&outlinepage=10&lanmu=zbgg"
            # print(url)
            yield scrapy.Request(url,meta={'num':str(x)},callback=self.parse)



    def parse2(self, response):
        item = TestchenItem()
        sourceUrl = response.request.meta['sourceUrl']
        item['sourceUrl'] = sourceUrl
        nums = ''

        content = response.xpath('/html//table//tr/td/table//tr[4]/td/table//text()').extract()

        # 去除掉列表中的所有的'',即空元素，并返回为一个列表
        content = [i for i in content if i != ' ']
        content = [e for e in content if e != '']#print(content)

        # 将列表连接为一个字符串
        content = "".join(content)

        # 将字符串中的空格全部替换掉
        content = content.replace("\xa0", "")
        content = content.replace(" ", "")
        content = content.replace("&nbsp", "")
        content = content.replace("\t", "")
        content = content.replace("\r", "")


        pName = re.findall('项目名称：\n(.*?)\n', content, re.S)
        if pName:
            pName = pName[0]
            pName = "".join(pName.split())
        else:
            pName = str(nums)


        entName = re.findall('采购人名称：(.*?)\s', content, re.S)
        if entName:
            entName = entName[0]
            entName = "".join(entName.split())
        else:
            entName = str(nums)


        pAddr = re.findall('项目实施地点：(.*?)\n', content, re.S)
        if pAddr:
            pAddr = pAddr[0]
            pAddr = "".join(pAddr.split())
        else:
            pAddr = str(nums)


        pApprovalName = str(nums)

        pApproveOrg = str(nums)

        pSupervision = str(nums)

        pubTime = str(nums)


        pNo = re.findall('采购项目编号：(.*?)\n', content, re.S)
        if pNo:
            pNo = pNo[0]
            pNo = "".join(pNo.split())
        else:
            pNo = str(nums)


        pBudget = re.findall('采购预算金额：(.*?)\n', content, re.S)
        if pBudget:
            pBudget = pBudget[0]
            pBudget = "".join(pBudget.split())
        else:
            pBudget = str(nums)



        linkman = re.findall('采购人联系方式：([\u3400-\u9FFF]{2,3})', content, re.S)
        if linkman:
            linkman = linkman[0]
            linkman = "".join(linkman.split())
        else:
            linkman = str(nums)


        pattern = "(?s){}(.*?)\n".format(linkman)
        tel = re.findall(pattern, content, re.S)
        if tel:
            tel = tel[0]
            tel = "".join(tel.split())
        else:
            tel = str(nums)


        pattern ="(?s){}(.*?)\n".format(linkman)
        mobile = re.findall(pattern, content, re.S)
        if mobile:
            mobile = mobile[0]
            mobile = "".join(mobile.split())
        else:
            mobile = str(nums)


        email = str(nums)


        fax = re.findall('传真电话：(.*?)\n', content, re.S)
        if fax:
            fax = fax[0]
            fax = "".join(fax.split())
        else:
            fax = str(nums)


        agentName = re.findall('代理机构：\n(.*?)\n', content, re.S)
        if agentName:
            agentName = agentName[0]
            agentName = "".join(agentName.split())
        else:
            agentName = str(nums)


        agentAddr = re.findall('采购代理机构地址：(.*?)\n', content, re.S)
        if agentAddr:
            agentAddr = agentAddr[0]
            agentAddr = "".join(agentAddr.split())
        else:
            agentAddr = str(nums)

        agentLinkman = re.findall('采购代理机构联系方式：(.*?)\n', content, re.S)
        if agentLinkman:
            agentLinkman = agentLinkman[0]
            agentLinkman = "".join(agentLinkman.split())
        else:
            agentLinkman = str(nums)


        midagentTel = "(?s){}[\s](.*?)\s采购预算金额：".format('采购代理机构联系方式：' + agentLinkman)
        agentTel = re.findall(midagentTel, content, re.S)
        if agentTel:
            agentTel = agentTel[0]
            agentTel = "".join(agentTel.split())
        else:
            agentTel = str(nums)


        agentMobile = agentTel


        agentEmail = str(nums)


        agentFax = str(nums)


        files = str(nums)


        bidTime = re.findall('开标时间：(.*?)\n', content, re.S)
        if bidTime:
            bidTime = bidTime[0]
            bidTime = "".join(bidTime.split())
        else:
            bidTime = str(nums)


        bidAddr = re.findall('开标地点：(.*?)\n', content, re.S)
        if bidAddr:
            bidAddr = bidAddr[0]
            bidAddr = "".join(bidAddr.split())
        else:
            bidAddr = str(nums)


        getfileStartTime = re.findall('获取文件开始时间：(.*?)\n', content, re.S)
        if getfileStartTime:
            getfileStartTime = getfileStartTime[0]
            getfileStartTime = "".join(getfileStartTime.split())
        else:
            getfileStartTime = str(nums)


        getfileEndTime = re.findall('获取文件结束时间：(.*?)\n', content, re.S)
        if getfileEndTime:
            getfileEndTime = getfileEndTime[0]
            getfileEndTime = "".join(getfileEndTime.split())
        else:
            getfileEndTime = str(nums)


        getfileTimeDesc = re.findall('时刻说明：(.*?)\n', content, re.S)
        if getfileTimeDesc:
            getfileTimeDesc = getfileTimeDesc[0]
            getfileTimeDesc = "".join(getfileTimeDesc.split())
        else:
            getfileTimeDesc = str(nums)


        text = content


        # item['pName'] = pName                          #项目名称
        #
        # item['pAddr'] = pAddr                          #项目地址
        #
        # item['pNo'] = pNo                              #项目编号
        #
        # item['pBudget'] = pBudget                      #项目预算
        #
        # item['linkman'] = linkman                      #招标人
        #
        # item['tel'] = tel                              #联系电话
        #
        # item['mobile'] = mobile                        #联系电话
        #
        # item['fax'] = fax                              #传真
        #
        # item['agentName'] = agentName                  #代理机构名称
        #
        # item['agentAddr'] = agentAddr                  #代理机构地址
        #
        # item['agentLinkman'] = agentLinkman            #代理机构联系人
        #
        # item['agentTel'] = agentTel                    #代理机构电话
        #
        # item['agentMobile'] = agentMobile              #代理机构电话
        #
        # item['bidTime'] = bidTime                      #开标时间
        #
        # item['bidAddr'] = bidAddr                      #开标地点
        #
        # item['getfileStartTime'] = getfileStartTime    #获取时间
        #
        # item['getfileEndTime'] = getfileEndTime        #获取时间
        #
        # item['getfileTimeDesc'] = getfileTimeDesc      #时间说明
        #
        # item['text'] = text                            #招标文本
        #
        # yield item

        agentFax = ''

        prov = ''

        city = ''

        district = ''

        spider = 'hebei'

        source = '中国河北政府采购网'

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


        yield item





if __name__ == '__main__':
    cmdline.execute("scrapy crawl Hebei".split())