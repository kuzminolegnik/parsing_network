# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Lesson5Item(scrapy.Item):
    # define the fields for your item here like:
    _id = scrapy.Field()
    title = scrapy.Field()
    link = scrapy.Field()
    raw_salary = scrapy.Field()
    type = scrapy.Field()
    salary_start = scrapy.Field()
    salary_end = scrapy.Field()
    currency = scrapy.Field()
    pass
