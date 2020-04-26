# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse
from lesson5.items import Lesson5Item


class SuperjobSpider(scrapy.Spider):
    name = 'superjob'
    allowed_domains = ['superjob.ru']

    def __init__(self, search, **kwargs):
        super().__init__(**kwargs)
        self.start_urls = [
            f'https://www.superjob.ru/vacancy/search/?keywords={search}&geo%5Bt%5D%5B0%5D=4'
        ]

    def parse(self, response: HtmlResponse):
        next_page = response.css('a.f-test-button-dalshe::attr(href)').extract_first()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

        vacancy_links = response.css('.f-test-vacancy-item div.acdxh.GPKTZ._1tH7S a::attr(href)').extract()
        for link in vacancy_links:
            yield response.follow(link, callback=self.parse_vacancy)

    @staticmethod
    def parse_vacancy(response: HtmlResponse):
        title = response.css('div.f-test-vacancy-base-info div._3MVeX h1::text').extract()
        raw_salary = response.css('div.f-test-vacancy-base-info div._3MVeX span.ZON4b::text').extract()
        link = response.request.url
        yield Lesson5Item(title=title, raw_salary=raw_salary, link=link)