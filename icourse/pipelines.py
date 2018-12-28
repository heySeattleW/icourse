# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json


class IcoursePipeline(object):

    # 构造函数（创建文件）
    def __init__(self):
        # 打开文件
        self.file = open('data.json', 'w', encoding='utf-8')

    # 处理数据
    def process_item(self, item, spider):
        line = json.dumps(dict(item), ensure_ascii=False) + "\n"
        # 写入文件
        self.file.write(line)
        return item

    # 该方法会在spider开启的时候被调用
    def open_spider(self, spider):
        pass

    # 该方法在spider被关闭时被调用。
    def close_spider(self, spider):
        pass
