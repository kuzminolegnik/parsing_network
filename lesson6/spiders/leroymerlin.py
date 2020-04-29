# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse
from scrapy.loader import ItemLoader
from lesson6.items import Lesson6Item


class LeroymerlinSpider(scrapy.Spider):
    name = 'leroymerlin'
    allowed_domains = ['leroymerlin.ru']

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.start_urls = [
            f'https://leroymerlin.ru/search/?sortby=8&tab=products&q=%D0%BE%D0%B1%D0%BE%D0%B8&family=00b9b5a0-faeb-11e9-810b-878d0b27ea5b&suggest=true'
        ]

    def parse(self, response: HtmlResponse):
        next_page = response.css('a.paginator-button.next-paginator-button::attr(href)').extract_first()

        vacancy_links = response.css(
            'div.search-content-tabs div.ui-sorting-cards div.product-name a::attr(href)'
        ).extract()

        for link in vacancy_links:
            yield response.follow(link, callback=self.parse_vacancy)

        if next_page:
            yield response.follow(next_page, callback=self.parse)

    @staticmethod
    def parse_vacancy(response: HtmlResponse):
        loader = ItemLoader(item=Lesson6Item(), response=response)

        loader.add_css('title',
                       'div.product-content div.detailed-view-inner uc-pdp-card-ga-enriched h1[slot="title"]::text')

        loader.add_css('price',
                       'div.product-content div.detailed-view-inner uc-pdp-card-ga-enriched uc-pdp-price-view.primary-price span[slot="price"]::text')

        loader.add_css('currency',
                       'div.product-content div.detailed-view-inner uc-pdp-card-ga-enriched uc-pdp-price-view.primary-price span[slot="currency"]::text')

        loader.add_css('unit',
                       'div.product-content div.detailed-view-inner uc-pdp-card-ga-enriched uc-pdp-price-view.primary-price span[slot="unit"]::text')

        loader.add_css('images_urls',
                       'div.product-content div.detailed-view-inner uc-pdp-media-carousel picture[slot="pictures"] img[itemprop="image"]::attr(src)'
                       )

        loader.add_css('key_attrs',
                       'div.product-content section.pdp-section--product-characteristicks div.def-list__group dt.def-list__term::text'
                       )

        loader.add_css('value_attrs',
                       'div.product-content section.pdp-section--product-characteristicks div.def-list__group dd.def-list__definition::text'
                       )

        yield loader.load_item()
