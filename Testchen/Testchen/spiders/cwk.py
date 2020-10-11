from Testchen.items import TestchenItem
import scrapy
import re
from scrapy import cmdline, selector


class CwkSpider(scrapy.Spider):
    name = 'cwk'
    allowed_domains = ['ggzy.hefei.gov.cn']
    start_urls = ['http://ggzy.hefei.gov.cn/jyxx/002001/002001001/moreinfo_jyxxgg2.html']
    # start_urls = ['http://ggzy.hefei.gov.cn/jyxx/002001/002001001/36.html']



    def parse(self, response):

        a = response.xpath('//ul[@class="ewb-right-item"]')
        for node in a:
            title = node.xpath('./li/a/@title').extract()
            url = node.xpath('./li/a/@href').extract()
            for c in url:
                sourceUrl = "http://ggzy.hefei.gov.cn" + c
                yield scrapy.Request("http://ggzy.hefei.gov.cn" + c, meta={'title': title,'sourceUrl':sourceUrl}, callback=self.parse2)


        new_links = response.xpath( '//li[@class="wb-page-li wb-page-item wb-page-next wb-page-family wb-page-fs12"][2]/a/@href').extract()
        if new_links and len(new_links) > 0:
            num = re.findall('002001001/(.*?).html', new_links[0])[0]
            if int(num) <= 100:
                # 获取下一页的链接
                new_link = new_links[0]
                # 再次发送请求获取下一页数据
                yield scrapy.Request("http://ggzy.hefei.gov.cn" + new_link, callback=self.parse)




    def parse2(self, response):
      item = TestchenItem()
      sourceUrl = response.request.meta['sourceUrl']
      item['sourceUrl'] = sourceUrl
      nums = '无'
      content_list0 = response.xpath('//div[@class="ewb-info-main clearfix"]//text()').extract()

      #去除掉列表中的所有的'',即空元素，并返回为一个列表
      content_list0 = [i for i in content_list0 if i != ' ']
      content_list0 = [e for e in content_list0 if e != '']

      #将列表连接为一个字符串
      content_list0 = "".join(content_list0)


      #将字符串中的空格全部替换掉
      content_list0 = content_list0.replace("\xa0", "")
      content_list0 = content_list0.replace(" ", "")
      content_list0 = content_list0.replace("&nbsp", "")
      content_list0 = content_list0.replace("\t", "")
      content_list0 = content_list0.replace("\r", "")


      pName = response.xpath('//div[@class="jxTenderObjMain"]/table/tbody/tr[1]/td[2]/text()').extract()
      if pName:
         pName = pName[0]
         pName = "".join(pName.split())
      else:
         pName = re.findall('项目名称：(.*?)3、', content_list0, re.S)
         if pName:
            pName = pName[0]
            pName = "".join(pName.split())
         else:
            pName = str(nums)


      entName = response.xpath('//div[@class="jxTenderObjMain"]/table/tbody/tr[2]/td[2]/text()').extract_first()
      pAddr = response.xpath('//div[@class="jxTenderObjMain"]/table/tbody/tr[2]/td[4]/text()').extract_first()
      pApprovalName = response.xpath('//div[@class="jxTenderObjMain"]/table/tbody/tr[3]/td[2]/text()').extract_first()
      pApproveOrg = response.xpath('//div[@class="jxTenderObjMain"]/table/tbody/tr[3]/td[4]/text()').extract_first()
      pSupervision = response.xpath('//div[@class="jxTenderObjMain"]/table/tbody/tr[4]/td[2]/text()').extract_first()
      pubTime = response.xpath('//div[@class="jxTenderObjMain"]/table/tbody/tr[5]/td[4]/text()').extract_first()

      pNo = re.findall('2[0-9A-Z]{13}|2[0-9A-Z]{11}', content_list0, re.S)
      if pNo:
         pNo = pNo[0]
         pNo = "".join(pNo.split())
      else:
         pNo = str(nums)


      linkman = re.findall('联系人：(.*?)电', content_list0, re.S)
      if linkman:
         linkman = linkman[0]
         linkman = "".join(linkman.split())
      else:
         linkman = str(nums)


      agentLinkman = re.findall('联系人：(.*?)电', content_list0, re.S)
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


      pBudget = re.findall('合同估算价：(.*?)元', content_list0, re.S)
      if pBudget:
         pBudget = pBudget[0]
         pBudget = "".join(pBudget.split())
      else:
         pBudget = re.findall('项目投资估算：(.*?)元2', content_list0, re.S)
         if pBudget:
            pBudget = pBudget[0]
            pBudget = "".join(pBudget.split())
         else:
            pBudget = re.findall('项目概算：(.*?)无\n', content_list0, re.S)
            if pBudget:
                pBudget = pBudget[0]
                pBudget = "".join(pBudget.split())
            else:
                pBudget = re.findall('项目概算：(.*?)元\n', content_list0, re.S)
                if pBudget:
                   pBudget = pBudget[0]
                   pBudget = "".join(pBudget.split())
                else:
                   pBudget = re.findall('概算投资额：(.*?)元\n', content_list0, re.S)
                   if pBudget:
                      pBudget = pBudget[0]
                      pBudget = "".join(pBudget.split())
                   else:
                      pBudget = re.findall('工程概况：(.*?)元\n', content_list0, re.S)
                      if pBudget:
                         pBudget = pBudget[0]
                         pBudget = "".join(pBudget.split())
                      else:
                         pBudget = str(nums)


      pattern ="(?s){}[\s]+电话：(.*?)\s".format(linkman)
      tel = re.findall(pattern, content_list0, re.S)
      if tel:
         tel = tel[0]
         tel = "".join(tel.split())
      else:
         tel = str(nums)

      mobile = tel


      email = re.findall('邮箱：(.*?)邮编：', content_list0, re.S)
      if email:
         email = email[0]
         email = "".join(email.split())
      else:
         email = str(nums)


      fox = re.findall('传真：(.*?)邮箱：', content_list0, re.S)
      if fox:
         fox = fox[0]
         fox = "".join(fox.split())
      else:
         fox = str(nums)


      agentName = response.xpath('//div[@class="jxTenderObjMain"]/table/tbody/tr[4]/td[4]/text()').extract_first()
      if agentName:
         #agentName = "".join(agentName.split())
         agentName = agentName
      else:
         agentName = re.findall('四、联系方式：\r\n单位：(.*?)地址：', content_list0, re.S)
         print(agentName)
         if agentName:
            agentName = agentName[0]
            agentName = "".join(agentName.split())
         else:
             agentName = re.findall('招标代理机构：(.*?)\n', content_list0, re.S)
             if agentName:
                 agentName = agentName[0]
                 agentName = "".join(agentName.split())
             else:
                 agentName = str(nums)



      agentAddr = re.findall('地址：(.*?)邮编：', content_list0, re.S)
      if agentAddr:
          try:
              agentAddr = agentAddr[1]
              agentAddr = "".join(agentAddr.split())
          except Exception as e:
               print('无', e)
               agentAddr = agentAddr[0]
          pass
      else:
         agentAddr = re.findall('地址：(.*?)联系人：', content_list0, re.S)
         if agentAddr:
            agentAddr = agentAddr[0]
            agentAddr = "".join(agentAddr.split())
         else:
            agentAddr = re.findall('地址：(.*?)本项目', content_list0, re.S)
            if agentAddr:
               agentAddr = agentAddr[0]
               agentAddr = "".join(agentAddr.split())
            else:
               agentAddr = str(nums)


      pattern ="(?s){}[\s]+电话：(.*?)\s".format(agentLinkman)
      agentTel = re.findall(pattern, content_list0, re.S)
      if agentTel:
         agentTel = agentTel[0]
         agentTel = "".join(agentTel.split())
      else:
         agentTel = str(nums)


      bidTime = re.findall('开标时间：(.*?)分', content_list0, re.S)
      if bidTime:
         bidTime = bidTime[0]
         bidTime = "".join(bidTime.split())
      else:
          bidTime = re.findall('磋商时间：(.*?)分', content_list0, re.S)
          if bidTime:
              bidTime = bidTime[0]
              bidTime = "".join(bidTime.split())
          else:
              bidTime = str(nums)


      bidAddr = re.findall('开标地点：(.*?)\n', content_list0, re.S)
      if bidAddr:
         bidAddr = bidAddr[0]
         bidAddr = "".join(bidAddr.split())
      else:
         bidAddr = re.findall('磋商地点：(.*?)\n', content_list0, re.S)
         if bidAddr:
            bidAddr = bidAddr[0]
            bidAddr = "".join(bidAddr.split())
         else:
            bidAddr = str(nums)


      getfileStartTime = re.findall('获取时间：(.*?)\n', content_list0, re.S)
      if getfileStartTime:
         getfileStartTime = getfileStartTime[0]
         getfileStartTime = "".join(getfileStartTime.split())
      else:
         getfileStartTime = str(nums)


      getfileEndTime = re.findall('获取时间：(.*?)\n', content_list0, re.S)
      if getfileEndTime:
         getfileEndTime = getfileEndTime[0]
         getfileEndTime = "".join(getfileEndTime.split())
      else:
         getfileEndTime = str(nums)


      getfileTimeDesc = re.findall('5.投标文件的递交\n(.*?)\n', content_list0, re.S)
      if getfileTimeDesc:
         getfileTimeDesc = getfileTimeDesc[0]
         getfileTimeDesc = "".join(getfileTimeDesc.split())
      else:
          getfileTimeDesc = re.findall('五、响应文件提交截止时间\n(.*?)\n', content_list0, re.S)
          if getfileTimeDesc:
              getfileTimeDesc = getfileTimeDesc[0]
              getfileTimeDesc = "".join(getfileTimeDesc.split())
          else:
              getfileTimeDesc = re.findall('1、报名时间：(.*?)\n', content_list0, re.S)
              if getfileTimeDesc:
                 getfileTimeDesc = getfileTimeDesc[0]
                 getfileTimeDesc = "".join(getfileTimeDesc.split())
              else:
                 getfileTimeDesc = str(nums)


      agentMobile = agentTel

      agentEmail = str(nums)

      agentFox = str(nums)

      files = str(nums)

      text = content_list0



      item['pName'] = pName
      item['entName'] = entName
      item['pAddr'] = pAddr
      item['pApprovalName'] = pApprovalName
      item['pApproveOrg'] = pApproveOrg
      item['pSupervision'] = pSupervision
      item['pubTime'] = pubTime
      item['pNo'] = pNo
      item['pBudget'] = pBudget
      item['linkman'] = linkman
      item['tel'] = tel
      item['mobile'] = mobile
      item['email'] = email
      item['fox'] = fox
      item['agentName'] = agentName
      item['agentAddr'] = agentAddr
      item['agentLinkman'] = agentLinkman
      item['agentTel'] = agentTel
      item['agentMobile'] = agentMobile
      item['agentEmail'] = agentEmail
      item['agentFox'] = agentFox
      item['files'] = files
      item['bidTime'] = bidTime
      item['bidAddr'] = bidAddr
      item['getfileStartTime'] = getfileStartTime
      item['text'] = text


      yield item






      # print(pName)                    # 项目名称
      #
      # print(entName)                  # 项目法人
      #
      # print(pAddr)                    # 项目地址
      #
      # print(pApprovalName)            # 项目批文名称
      #
      # print(pApproveOrg)              # 审批单位
      #
      # print(pSupervision)             # 监管部门
      #
      # print(pubTime)                  # 项目建立时间
      #
      # print(pNo)                      # 项目编号
      #
      # print(pBudget)                  # 项目预算
      #
      # print(linkman)                  # 招标人
      #
      # print(tel)                      # 联系电话
      #
      # print(mobile)                   # 联系电话
      #
      # print(email)                    # 电子邮箱
      #
      # print(fox)                      # 传真
      #
      # print(agentName)                # 代理机构名称
      #
      # print(agentAddr)                # 代理机构地址
      #
      # print(agentLinkman)             # 代理机构联系人
      #
      # print(agentTel)                 # 代理机构电话
      #
      # print(agentMobile)              # 代理机构电话
      #
      # print(agentEmail)               # 代理机构电子邮箱
      #
      # print(agentFox)                 # 代理机构传真
      #
      # print(files)                    # 附件
      #
      # print(bidTime)                  # 开标时间
      #
      # print(bidAddr)                  # 开标地点
      #
      # print(getfileStartTime)         # 获取时间
      #
      # #print(getfileEndTime)          # 获取时间
      #
      # print(getfileTimeDesc)          # 时间说明
      #
      # #print(text)                     # 招标文本







if __name__ == '__main__':
    cmdline.execute("scrapy crawl cwk".split())