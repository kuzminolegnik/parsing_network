# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import re
from pymongo import MongoClient


class Lesson5Pipeline(object):
    def __init__(self):
        client = MongoClient('mongodb://localhost:27017/')
        db_mongo = client.lesson5
        collection = db_mongo['vacations']
        collection.remove()
        self.db_collection = collection

    def process_item(self, item, spider):
        collection = self.db_collection
        text_salary = ''.join(item['raw_salary']).replace('\xa0', ' ')
        item['raw_salary'] = text_salary
        item['title'] = ' '.join(item['title'])
        item['salary_start'] = None
        item['salary_end'] = None
        item['currency'] = None

        if re.findall(r'\s*от\s*([\d\s]+)\s+до\s+([\d\s]+)\s+(\S+)[\s\w]*', text_salary):
            parts = re.findall(r'\s*от\s*([\d\s]+)\s+до\s+([\d\s]+)\s+(\S+)[\s\w]*', text_salary)
            item['salary_start'] = float(parts[0][0].replace(' ', ''))
            item['salary_end'] = float(parts[0][1].replace(' ', ''))
            item['currency'] = parts[0][2]
        elif re.findall(r"\s*от\s*([\d\s]+)\s+(\S+)", text_salary):
            parts = re.findall(r'\s*от\s*([\d\s]+)\s+(\S+)', text_salary)
            item['salary_start'] = float(parts[0][0].replace(' ', ''))
            item['currency'] = parts[0][1]
        elif re.findall(r'\s*до\s*([\d\s]+)\s+(\S+)', text_salary):
            parts = re.findall(r'\s*до\s*([\d\s]+)\s+(\S+)', text_salary)
            item['salary_end'] = float(parts[0][0].replace(' ', ''))
            item['currency'] = parts[0][1]

        item['type'] = spider.name
        collection.insert_one(item)
        return item
