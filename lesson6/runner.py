from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
from lesson6 import settings
from lesson6.spiders.leroymerlin import LeroymerlinSpider

if __name__ == '__main__':
    search = 'Python'
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)
    process = CrawlerProcess(settings=crawler_settings)
    process.crawl(LeroymerlinSpider, search=search)
    process.start()
