#! python3
# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup as bs
import pandas as pd
import requests
import re

search = str(input('Please enter search: '))

urlHH = 'https://serpukhov.hh.ru/search/vacancy'
paramsHH = {
    'L_save_area': True,
    'clusters': True,
    'enable_snippets': True,
    'text': search,
    'showClusters': True,
    'page': 0
}
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36'
}
result = []


def get_sum(text):
    start_sum = None
    end_sum = None
    currency = None

    if re.findall(r'\s*([\d\s]+)\s*[\-—]+\s*([\d\s]+)\s+(\D+)', text):
        parts = re.findall(r'\s*([\d\s]+)\s*-\s*([\d\s]+)\s+(\D+)', text)
        start_sum = float(parts[0][0].replace(' ', ''))
        end_sum = float(parts[0][1].replace(' ', ''))
        currency = parts[0][2]
    elif re.findall(r'\s*от\s*([\d\s]+)\s+(\D+)', text):
        parts = re.findall(r'\s*от\s*([\d\s]+)\s+(\D+)', text)
        start_sum = float(parts[0][0].replace(' ', ''))
        currency = parts[0][1]
    elif re.findall(r'\s*до\s*([\d\s]+)\s+(\D+)', text):
        parts = re.findall(r'\s*до\s*([\d\s]+)\s+(\D+)', text)
        end_sum = float(parts[0][0].replace(' ', ''))
        currency = parts[0][1]

    return (start_sum, end_sum, currency)


while True:
    response = requests.get(urlHH, headers=headers, params=paramsHH).text
    soup = bs(response, 'html.parser')
    items = soup.find_all('div', {'class': 'vacancy-serp-item'})

    if not len(items):
        break

    for item in items:
        record = {}
        title_item = item.find('a', {'data-qa': 'vacancy-serp__vacancy-title'})
        compensation_item = item.find('span', {'data-qa': 'vacancy-serp__vacancy-compensation'})
        employer_item = item.find('a', {'data-qa': 'vacancy-serp__vacancy-employer'})
        title = title_item.getText()
        link = title_item['href']
        employer = None
        start_sum = None
        end_sum = None
        currency = None

        if employer_item:
            employer = employer_item.getText()

        if compensation_item:
            compensation_text = compensation_item.getText().replace(' ', '')
            parts = get_sum(compensation_text)
            start_sum = parts[0]
            end_sum = parts[1]
            currency = parts[2]

        record["employer"] = employer
        record["title"] = title
        record["link"] = link
        record["source"] = 'hh.ru'
        record["start_sum"] = start_sum
        record["end_sum"] = end_sum
        record["currency"] = currency

        result.append(record)

    paramsHH['page'] += 1

    print(len(result))

domainSuperJob = 'https://serpukhov.superjob.ru'
pathSuperJob = '/vacancy/search/'
paramsSuperJob = {
    'keywords': search,
    'page': 0
}

while True:
    response = requests.get('{0}{1}'.format(domainSuperJob, pathSuperJob), headers=headers, params=paramsSuperJob).text
    soup = bs(response, 'html.parser')
    items = soup.find_all('div', {'class': 'f-test-vacancy-item'})

    for item in items:
        record = {}
        title_item = item.find('div', {'class': 'acdxh'}).find('a')
        employer_item = item.find('span', {'class': 'f-test-text-vacancy-item-company-name'}).find('a')
        compensation_item = item.find('span', {'class': 'f-test-text-company-item-salary'})
        title = title_item.getText()
        link = domainSuperJob + title_item['href']
        employer = None
        start_sum = None
        end_sum = None
        currency = None

        if employer_item:
            employer = employer_item.getText()

        if compensation_item:
            compensation_text = compensation_item.getText().replace(' ', '').replace('<!-- -->', ' ')
            parts = get_sum(compensation_text)
            start_sum = parts[0]
            end_sum = parts[1]
            currency = parts[2]

        record["employer"] = employer
        record["title"] = title
        record["link"] = link
        record["source"] = 'superjob'
        record["start_sum"] = start_sum
        record["end_sum"] = end_sum
        record["currency"] = currency
        result.append(record)

    if not soup.find(attrs={'class': 'f-test-button-dalshe'}):
        break

    paramsSuperJob['page'] += 1
    print(len(result))

df = pd.DataFrame(result)
df.to_csv(r'./export_dataframe.csv', index = False, header=True)
