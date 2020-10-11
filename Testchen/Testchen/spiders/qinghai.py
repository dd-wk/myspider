import json
import scrapy
from Testchen.items import TestchenItem
import re
from scrapy import cmdline, selector

class QinghaiSpider(scrapy.Spider):
    name = 'qinghai'

    # def start_requests(self):
    #     url = 'http://www.qhggzyjy.gov.cn/inteligentsearch/rest/inteligentSearch/getFullTextData'
    #     # FormRequest 是Scrapy发送POST请求的方法
    #     yield scrapy.Request(
    #         method="POST",
    #         url=url,
    #         body='{"token":"","pn":490,"rn":10,"sdt":"","edt":"","wd":"","inc_wd":"","exc_wd":"","fields":"title","cnum":"001;002;003;004;005;006;007;008;009;010","sort":"{\\"showdate\\":\\"0\\"}","ssort":"title","cl":200,"terminal":"","condition":[{"fieldName":"categorynum","isLike":true,"likeType":2,"equal":"001001001"}],"time":null,"highlights":"title","statistics":null,"unionCondition":null,"accuracy":"100","noParticiple":"0","searchRange":null,"isBusiness":1}',
    #         callback=self.parse
    #     )
    #
    # def parse(self, response, **kwargs):
    #     # print(response.text)
    #     paydata = json.loads(response.text)
    #     data = paydata['result']
    #     data1 = data['records']
    #     for i in data1:
    #         sourceUrl = "http://www.qhggzyjy.gov.cn" + i['linkurl']
    #         yield scrapy.Request(sourceUrl, meta={'sourceUrl': sourceUrl}, callback=self.parse2)
    #
    #     # if 'num' in response.meta:
    #     #     x = int(response.meta['num'])
    #     # else:
    #     #     x = 1
    #     # if x < 100:
    #     #     x = x + 1
    #     #     c = 10*(x-1)
    #     #     url = 'http://www.qhggzyjy.gov.cn/inteligentsearch/rest/inteligentSearch/getFullTextData'
    #     #     # FormRequest 是Scrapy发送POST请求的方法
    #     #     yield scrapy.Request(
    #     #         method="POST",
    #     #         url=url,
    #     #         body='{"token":"","pn":%s,"rn":10,"sdt":"","edt":"","wd":"","inc_wd":"","exc_wd":"","fields":"title","cnum":"001;002;003;004;005;006;007;008;009;010","sort":"{\\"showdate\\":\\"0\\"}","ssort":"title","cl":200,"terminal":"","condition":[{"fieldName":"categorynum","isLike":true,"likeType":2,"equal":"001001001"}],"time":null,"highlights":"title","statistics":null,"unionCondition":null,"accuracy":"100","noParticiple":"0","searchRange":null,"isBusiness":1}'%str(c),
    #     #         callback=self.parse,meta={'num': str(c)}
    #     #     )

    def start_requests(self):
        url = 'http://www.qhggzyjy.gov.cn/wzds/CustomSearchInfoShow.action?cmd=Custom_Search_InfoShow'
        # FormRequest 是Scrapy发送POST请求的方法
        yield scrapy.FormRequest(
            url = url,
            formdata={'cnum':'001;002;003;004;005;006;007;008;009;010',
                      'front':'/ggzy',
                      'area':'0',
                      'categoryNum':'001001001',
                      'pageIndex': '2700',
                      'pageSize': '10',
                      'xiaquCode': '',
                      'titleInfo':''
                      },
            callback = self.parse
        )

    def parse(self, response, **kwargs):
        # print(response.text)
        paydata = json.loads(response.text)
        data = paydata['custom']
        data_json = json.loads(data)
        data1 = data_json['records']
        for i in data1:
            sourceUrl = "http://www.qhggzyjy.gov.cn" + i['linkurl']
            # print(sourceUrl)
            yield scrapy.Request(sourceUrl, meta={'sourceUrl': sourceUrl}, callback=self.parse2)

        if 'num' in response.meta:
            x = int(response.meta['num'])
        else:
            x = 50
        if x < 70:
            x = x + 1
            url = 'http://www.qhggzyjy.gov.cn/wzds/CustomSearchInfoShow.action?cmd=Custom_Search_InfoShow'
            # FormRequest 是Scrapy发送POST请求的方法
            yield scrapy.FormRequest(
                url=url,
                formdata={'cnum': '001;002;003;004;005;006;007;008;009;010',
                          'front': '/ggzy',
                          'area': '0',
                          'categoryNum': '001001001',
                          'pageIndex': str(x),
                          'pageSize': '10',
                          'xiaquCode': '',
                          'titleInfo': ''
                          },
                callback=self.parse,meta={'num': str(x)}
            )



    def parse2(self, response):
        item = TestchenItem()
        # print(response.text)
        sourceUrl = response.request.meta['sourceUrl']
        a = ''
        nums = ''
        content = response.xpath('//div')
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

        if pName == str(nums):
            pName = re.findall('本招标项目(.*?)工程', a, re.S)
            if pName:
                pName = pName[0]
                pName = "".join(pName.split())
                pName = pName + '项目'
            else:
                pName = str(nums)
        else:
            pName = pName

        if len(pName) > 50:
            pName = str(nums)
        else:
            pName = pName



        entName = re.findall('招标人：(.*?)\s', a, re.S)
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
            pBudget = re.findall('合同估算价(.*?)\s', a, re.S)
            if pBudget:
                pBudget = pBudget[0]
                pBudget = "".join(pBudget.split())
            else:
                pBudget = str(nums)

        if len(pBudget)>20:
            pBudget = str(nums)
        else:
            pBudget = pBudget


        linkman = re.findall('联系人：(.*?)\s', a, re.S)
        if linkman:
            linkman = linkman[0]
            linkman = "".join(linkman.split())
        else:
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
                linkman = str(nums)

        if len(linkman) > 8:
            linkman = str(nums)
        else:
            linkman = linkman


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
                agentName = re.findall('代理机构：(.*?)\s', a, re.S)
                if agentName:
                    agentName = agentName[0]
                    agentName = "".join(agentName.split())
                else:
                    agentName = str(nums)


        agentAddr = re.findall('联系地址：(.*?)\s', a, re.S)
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
                pass
            else:
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
                    print('无', e)
                    agentLinkman = str(nums)
                pass
            else:
                agentLinkman = str(nums)

        if len(agentLinkman) > 10:
            agentLinkman = str(nums)
        else:
            agentLinkman = agentLinkman


        agentTel = re.findall('电话：(.*?)\s', a, re.S)
        if agentTel:
            try:
                agentTel = agentTel[1]
                agentTel = "".join(agentTel.split())
            except Exception as e:
                print('无', e)
                agentTel = str(nums)
            pass
        else:
            agentTel = re.findall('联系方式：(.*?)\s', a, re.S)
            if agentTel:
                agentTel = agentTel[0]
                agentTel = "".join(agentTel.split())
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


        bidTime = re.findall('（投标截止时间，下同）为(.*?)分', a, re.S)
        if bidTime:
            bidTime = bidTime[0]
            bidTime = "".join(bidTime.split())
            bidTime = bidTime + '分'
        else:
            bidTime = re.findall('开标时间:(.*?)\s', a, re.S)
            if bidTime:
                bidTime = bidTime[0]
                bidTime = "".join(bidTime.split())
            else:
                bidTime = re.findall('截止时间：(.*?)\s', a, re.S)
                if bidTime:
                    bidTime = bidTime[0]
                    bidTime = "".join(bidTime.split())
                else:
                    bidTime = re.findall('截止时间（申请截止时间，下同）为(.*?)分', a, re.S)
                    if bidTime:
                        bidTime = bidTime[0]
                        bidTime = "".join(bidTime.split())
                        bidTime = bidTime + '分'
                    else:
                        bidTime = str(nums)


        bidAddr = re.findall('由招标人\（代理机构\）在(.*?)\（地址：', a, re.S)
        if bidAddr:
            bidAddr = bidAddr[0]
            bidAddr = "".join(bidAddr.split())
        else:
            bidAddr = re.findall('开标地点:(.*?)\s', a, re.S)
            if bidAddr:
                bidAddr = bidAddr[0]
                bidAddr = "".join(bidAddr.split())
            else:
                bidAddr = re.findall('\（地址：(.*?)\）', a, re.S)
                if bidAddr:
                    bidAddr = bidAddr[0]
                    bidAddr = "".join(bidAddr.split())
                else:
                    bidAddr = re.findall('地点为(.*?)。', a, re.S)
                    if bidAddr:
                        bidAddr = bidAddr[0]
                        bidAddr = "".join(bidAddr.split())
                    else:
                        bidAddr = str(nums)

        if len(bidAddr) > 70:
            bidAddr = str(nums)
        else:
            bidAddr = bidAddr


        getfileStartTime = re.findall('获取方式自(.*?)止', a, re.S)
        if getfileStartTime:
            getfileStartTime = getfileStartTime[0]
            getfileStartTime = "".join(getfileStartTime.split())
        else:
            getfileStartTime = re.findall('获取招标文件的时间：(.*?)\s', a, re.S)
            if getfileStartTime:
                getfileStartTime = getfileStartTime[0]
                getfileStartTime = "".join(getfileStartTime.split())
            else:
                getfileStartTime = re.findall('获取竞争性磋商文件的时间：(.*?)\s', a, re.S)
                if getfileStartTime:
                    getfileStartTime = getfileStartTime[0]
                    getfileStartTime = "".join(getfileStartTime.split())
                else:
                    getfileStartTime = re.findall('凡有意参加投标者，请于(.*?)，', a, re.S)
                    if getfileStartTime:
                        getfileStartTime = getfileStartTime[0]
                        getfileStartTime = "".join(getfileStartTime.split())
                    else:
                        getfileStartTime = str(nums)



        if len(getfileStartTime) > 50:
            getfileStartTime = str(nums)
        else:
            getfileStartTime = getfileStartTime



        getfileTimeDesc = re.findall('公告期限\s(.*?)\s', a, re.S)
        if getfileTimeDesc:
            getfileTimeDesc = getfileTimeDesc[0]
            getfileTimeDesc = "".join(getfileTimeDesc.split())
        else:
            getfileTimeDesc = re.findall('\（地址：(.*?)\）', a, re.S)
            if getfileTimeDesc:
                getfileTimeDesc = getfileTimeDesc[0]
                getfileTimeDesc = "".join(getfileTimeDesc.split())
            else:
                getfileTimeDesc = re.findall('截止时间（申请截止时间，下同）为(.*?)分', a, re.S)
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

        spider = 'qinghai'

        source = '青海省公共资源交易网'

        pApprovalName = ''

        pApproveOrg = ''

        pSupervision = ''

        pubTime = ''

        files = ''


        # item['pNo'] = pNo
        #
        # item['pName'] = pName
        #
        # item['entName'] = entName
        #
        # item['pAddr'] = pAddr
        #
        # item['pApprovalName'] = pApprovalName
        #
        # item['pApproveOrg'] = pApproveOrg
        #
        # item['pSupervision'] = pSupervision
        #
        # item['pubTime'] = pubTime
        #
        # item['pBudget'] = pBudget
        #
        # item['linkman'] = linkman
        #
        # item['tel'] = tel
        #
        # item['mobile'] = mobile
        #
        # item['email'] = email
        #
        # item['fax'] = fax
        #
        # item['bidTime'] = bidTime
        #
        # item['bidAddr'] = bidAddr
        #
        # item['agentName'] = agentName
        #
        # item['agentAddr'] = agentAddr
        #
        # item['agentLinkman'] = agentLinkman
        #
        # item['agentTel'] = agentTel
        #
        # item['agentMobile'] = agentMobile
        #
        # item['agentEmail'] = agentEmail
        #
        # item['agentFax'] = agentFax
        #
        # item['prov'] = prov
        #
        # item['city'] = city
        #
        # item['district'] = district
        #
        # item['spider'] = spider
        #
        # item['source'] = source
        #
        item['sourceUrl'] = sourceUrl
        #
        # item['getfileStartTime'] = getfileStartTime
        #
        # item['getfileEndTime'] = getfileEndTime
        #
        # item['getfileTimeDesc'] = getfileTimeDesc
        #
        # item['text'] = text
        #
        # item['files'] = files

        print(item)

        # yield item


if __name__ == '__main__':
    cmdline.execute("scrapy crawl qinghai".split())