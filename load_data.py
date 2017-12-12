from bs4 import BeautifulSoup
from urllib import request as urllib
import json
import requests

BASE_URL = 'https://coinmarketcap.com/'

CURRENCY_URL = 'https://coinmarketcap.com/currencies/'
URL_OPTION = '/historical-data/?start=20130428&end=20171212'

CURRENT_PRICE_URL = 'https://api.coinmarketcap.com/v1/ticker/'

currencies = []


data_path = './data/'
currencies_file = './data/currencies.json'


def match_class(target):
    def do_match(tag):
        classes = tag.get('class', [])
        return all(c in classes for c in target)

    return do_match


def get_html(url):
    return urllib.urlopen(url)


def list_currencies():
    global currencies
    try:
        with open(currencies_file) as json_file:
            currencies = json.load(json_file)
    except:
        try:
            raw_html = get_html(BASE_URL)
            html = BeautifulSoup(raw_html, "html.parser")
            currencies_links = html.findAll(match_class(['currency-name-container']))
            for link in currencies_links:
                currency = link['href'].replace('/currencies', '').replace('/', '')
                currencies.append(currency)
            with open(currencies_file, 'w') as json_file:
                json.dump(currencies, json_file)
        except:
            print('Cannot scrap currencies')

    return currencies


def load_historical(currency):
    data = ''
    file_path = data_path+currency+'.csv'
    try:
        with open(file_path) as csv_file:
            data = csv_file.read()
    except:
        try:
            raw_html = get_html(CURRENCY_URL+currency+URL_OPTION)
            html = BeautifulSoup(raw_html, "html.parser")
            table = html.find("div", {'id': 'historical-data'}).find('tbody')
            rows = table.findAll('tr')
            data = ''
            for row in rows:
                line = ''
                for col in row.findAll('td'):
                    line += col.getText().replace(',', '')+','
                line = line[:-1] + '\n'
                data += line
            with open(file_path, 'w') as csv_file:
                csv_file.write(data)
        except:
            print('Cannot scrap historical data')
    return data


def get_current_price(currency):
    r = requests.get(CURRENT_PRICE_URL+currency)
    r = r.json()[0]
    return str(round(float(r['price_usd'])))


def get_news_articles(currency):
    r = requests.get('https://newsapi.org/v2/everything?sources=crypto-coins-news&q='+currency+'&sortBy=publishedAt&apiKey=fa39776ed35f4f0c859b0231c410ce39')
    r = r.json()
    article = r['articles'][0]
    source = article['author'].replace('By ', '')
    title = article['title']
    description = article['description']
    url = article['url']
    return source, url, description, title