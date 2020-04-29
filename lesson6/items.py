# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import re
import scrapy
from scrapy.loader.processors import TakeFirst, MapCompose


def value_strip(value: str):
    return value.strip()


def value_int(value: str):
    if not value:
        return 0
    price = re.sub(r'[^\w\s]', '', value)
    price = re.sub(r'\s+', '', price)
    return float(price)


class Lesson6Item(scrapy.Item):
    # define the fields for your item here like:
    _id = scrapy.Field()
    title = scrapy.Field(output_processor=TakeFirst())
    unit = scrapy.Field(output_processor=TakeFirst())
    currency = scrapy.Field(output_processor=TakeFirst())
    price = scrapy.Field(output_processor=TakeFirst(), input_processor=MapCompose(value_int))
    key_attrs = scrapy.Field(input_processor=MapCompose(value_strip))
    value_attrs = scrapy.Field(input_processor=MapCompose(value_strip))
    images_urls = scrapy.Field(input_processor=MapCompose(value_strip))
    images = scrapy.Field()
    attrs = scrapy.Field()
    pass
