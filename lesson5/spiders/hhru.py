# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse
from lesson5.items import Lesson5Item


class HhruSpider(scrapy.Spider):
    name = 'hhru'
    allowed_domains = ['hh.ru']

    def __init__(self, search, **kwargs):
        super().__init__(**kwargs)
        self.start_urls = [
            f'https://hh.ru/search/vacancy?area=0&st=searchVacancy&text={search}&from=suggest_post&customDomain=1'
        ]

    def parse(self, response: HtmlResponse):
        next_page = response.css('a.HH-Pager-Controls-Next::attr(href)').extract_first()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

        vacancy_links = response.css('div.vacancy-serp-item a.HH-LinkModifier::attr(href)').extract()
        for link in vacancy_links:
            yield response.follow(link, callback=self.parse_vacancy)

    @staticmethod
    def parse_vacancy(response: HtmlResponse):
        title = response.css('div.vacancy-title h1 *::text').extract()
        raw_salary = response.css('p.vacancy-salary *::text').extract()
        link = response.request.url
        yield Lesson5Item(title=title, raw_salary=raw_salary, link=link)
