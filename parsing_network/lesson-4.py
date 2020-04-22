from datetime import datetime
from pymongo import MongoClient
from lxml import html
import requests
import time

header = {
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1'
}

client = MongoClient('localhost', 27017)
db = client['lesson_4']

items = db.items

def get_news_from_mail():
    main_link = 'https://news.mail.ru'
    response = requests.get(main_link, headers=header)
    root = html.fromstring(response.text)
    links = root.xpath("//a[contains(@class, 'item_side_left')]/@href")
    result = []
    for link in links[:10]:
        try:
            dict = {}
            response = requests.get(main_link + link, headers=header)
            root = html.fromstring(response.text)
            container = root.xpath("//div[contains(@class, 'article-swipe-content__viewport')]/div[1]")
            print(main_link + link)
            article = container[0].xpath(".//h1[contains(@class, 'article__title')]/text()")
            date = container[0].xpath(".//div[contains(@class, 'article__params')]//time/@datetime")
            source = container[0].xpath(
                ".//div[contains(@class, 'article__params')]//a[contains(@class, 'article__param')]/text()")
            dict['link'] = main_link + link
            dict['date'] = date[0]
            dict['source'] = source[0]
            dict['article'] = article[0]
            result.append(dict)
            time.sleep(1)
        except Exception as e:
            print(e)

    return result


def get_news_from_lenta():
    main_link = 'https://m.lenta.ru'
    main_link_path = '/parts/news/'
    response = requests.get(main_link + main_link_path, headers=header)
    root = html.fromstring(response.text)
    items = root.xpath("//div[contains(@class, 'parts-page__body')]//div[contains(@class, 'parts-page__item')]")
    result = []
    dateTime = datetime.now()

    for item in items[:10]:
        try:
            dict = {}
            link = item.xpath(".//a[contains(@class, 'card-mini')]/@href")[0]
            article = item.xpath(".//div[contains(@class, 'card-mini__title')]/text()")[0]
            date = item.xpath(".//time/text()")[0]
            dict['link'] = main_link + link
            dict['date'] = dateTime.strftime("%Y-%m-%d") + " " + date
            dict['source'] = 'Lenta.ru'
            dict['article'] = article
            result.append(dict)
        except Exception as e:
            print(e)

    return result


def get_news_from_yandex():
    main_link = 'https://yandex.ru'
    main_link_path = '/news/'
    response = requests.get(main_link + main_link_path, headers=header)
    root = html.fromstring(response.text)
    items = root.xpath("//div[contains(@class, 'news-container')]//span[@data-reactroot]")
    result = []
    dateTime = datetime.now()

    for item in items[:10]:
        try:
            dict = {}
            link = item.xpath(".//h2/a/@href")[0]
            article = item.xpath(".//h2/a[contains(@class, 'card__link')]/text()")[0]
            date = item.xpath(".//footer//span[contains(@class, 'card__source-date')]/text()")[0]
            source = item.xpath(".//footer//span[contains(@class, 'card__source-name')]/text()")[0]
            print(link, article, date, source)
            dict['link'] = link
            dict['date'] = dateTime.strftime("%Y-%m-%d") + " " + date
            dict['source'] = source
            dict['article'] = article
            result.append(dict)
        except Exception as e:
            print(e)

    return result


items.insert_many(get_news_from_yandex())
items.insert_many(get_news_from_lenta())
items.insert_many(get_news_from_mail())