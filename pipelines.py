# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from acfun.items import ArticleItem, CommentItem
import json
from scrapy import signals
from scrapy.exporters import JsonItemExporter, CsvItemExporter
from collections import defaultdict


#
# class ArticlePipeline(object):
#     def process_item(self, item, spider):
#         if isinstance(item, ArticleItem):
#             article = open('article.json', 'wb')
#             article.write(json.dumps(item))
#             article.close()
#         return item
#
#
# class CommentPipeline(object):
#     def process_item(self, item, spider):
#         if isinstance(item, CommentItem):
#             comment = open('comment.json', 'wb')
#             comment.write(json.dumps(item))
#             comment.close()
#         return item


class JsonExportPipeline(object):

    def __init__(self):
        self.article = open('article.json', 'w',encoding='UTF-8')
        self.comment = open('comment.json', 'w',encoding='UTF-8')

    # @classmethod
    # def from_crawler(cls, crawler):
    #     pipeline = cls()
    #     crawler.signals.connect(pipeline.spider_opened, signals.spider_opened)
    #     crawler.signals.connect(pipeline.spider_closed, signals.spider_closed)
    #     return pipeline
    #
    # def spider_opened(self, spider):
    #     article = open('article.json', 'w+b')
    #     comment = open('comment.json', 'w+b')
    #     self.files[spider].append(article)
    #     self.files[spider].append(comment)
    #     self.exporters = [
    #         JsonItemExporter(article, encoding='UTF-8'),
    #         JsonItemExporter(comment, encoding='UTF-8'),
    #     ]
    #     for exporter in self.exporters:
    #         exporter.start_exporting()
    #
    # def spider_closed(self, spider):
    #     for exporter in self.exporters:
    #         exporter.finish_exporting()
    #     files = self.files.pop(spider)
    #     for file in files:
    #         file.close()

    # def process_item(self, item, spider):
    #     if isinstance(item,ArticleItem):
    #         self.exporters[0].export_item(item)
    #     elif isinstance(item,CommentItem):
    #         self.exporters[1].export_item(item)
    #     return item
    def process_item(self, item, spider):
        if isinstance(item, ArticleItem):
            self.article.write((json.dumps(dict(item),ensure_ascii=False)+'\n'))
        elif isinstance(item, CommentItem):
            self.comment.write((json.dumps(dict(item),ensure_ascii=False)+'\n'))
        return item
