# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import scrapy
import os
from urllib.parse import urlparse
from scrapy.pipelines.images import ImagesPipeline
from pymongo import MongoClient


class Lesson6Pipeline(object):
    def __init__(self):
        client = MongoClient('mongodb://localhost:27017/')
        db_mongo = client.lesson6
        collection = db_mongo['leroymerlin']
        collection.remove()
        self.db_collection = collection

    def process_item(self, item, spider):
        collection = self.db_collection
        attrs = []
        for i in range(len(item['key_attrs'])):
            attrs.append({
                'key': item['key_attrs'][i],
                'value': item['value_attrs'][i]
            })
        item['attrs'] = attrs
        collection.insert_one(item)
        return item


class Lesson6ImagesPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        if item['images_urls']:
            for image in item['images_urls']:
                try:
                    yield scrapy.Request(image)
                except Exception as e:
                    print(e)
        return item

    def item_completed(self, results, item, info):
        if results[0]:
            item['images'] = [itm[1]['path'] for itm in results if itm[0]]

        return item
