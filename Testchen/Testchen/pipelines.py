# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import json


class TestchenPipeline:
    def process_item(self, item, spider):
        with open('F:/语言练习/data/guizhou.json', 'a+', encoding='utf-8') as f:
            lines = json.dumps(dict(item), ensure_ascii=False) + '\n'
            f.write(lines)
        return item






#
# class BookstorePipeline(object):
#     def process_item(self, item, spider):
#         with open('E:/study/python/pycodes/bookstore/book.json','a+',encoding='utf-8') as f:
#             lines = json.dumps(dict(item),ensure_ascii=False) + '\n'
#             f.write(lines)
#         return item

