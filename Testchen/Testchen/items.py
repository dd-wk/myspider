# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class TestchenItem(scrapy.Item):
    pNo = scrapy.Field()
    pName = scrapy.Field()
    entName = scrapy.Field()
    pAddr = scrapy.Field()
    pApprovalName = scrapy.Field()
    pApproveOrg = scrapy.Field()
    pSupervision = scrapy.Field()
    pubTime = scrapy.Field()
    pBudget = scrapy.Field()
    linkman = scrapy.Field()
    tel = scrapy.Field()
    mobile = scrapy.Field()
    email = scrapy.Field()
    fax = scrapy.Field()
    bidTime = scrapy.Field()
    bidAddr = scrapy.Field()
    agentName = scrapy.Field()
    agentAddr = scrapy.Field()
    agentLinkman = scrapy.Field()
    agentTel = scrapy.Field()
    agentMobile = scrapy.Field()
    agentEmail = scrapy.Field()
    agentFax = scrapy.Field()
    prov = scrapy.Field()
    city = scrapy.Field()
    district = scrapy.Field()
    spider = scrapy.Field()
    source = scrapy.Field()
    sourceUrl = scrapy.Field()
    getfileStartTime = scrapy.Field()
    getfileEndTime = scrapy.Field()
    getfileTimeDesc = scrapy.Field()
    text = scrapy.Field()
    files = scrapy.Field()
