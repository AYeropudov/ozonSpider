# -*- coding: utf-8 -*-
from concurrent import futures
from lxml import html
from bs4 import BeautifulSoup
import urllib3
from tqdm import tqdm
import collections
import xls_reader
import re


# фУНКЦИЯ ЧТЕНИЯ ИЗ ФАЙЛОВ
def read_file(filename):
    with open(filename) as input_file:
        text = input_file.read()
    return text


# СКРАППИНГ СТРАНИЦ
def parse_www(uri):
    art = uri[0].encode('cp1251')
    url = url_parse.format(art)
    r = http.request('GET', url)
    data = r.data.decode('cp1251').encode('utf8')
    text_file = open(u"/home/alex/spider/html/{}.html".format(art.encode('utf8')), "w")
    text_file.write(data)
    text_file.close()
    return


# Парстинг HTML соохранение результатов
def parse_html(uri):
    art = uri[0]
    text = read_file(u"/home/alex/spider/html/{}.html".format(art))
    soup = BeautifulSoup(text, "html.parser")
    results = soup.find_all('div', {'class': 'eItemProperties_text'})
    price_div = soup.find('div', {'class': 'bSaleColumn'})
    price = None
    if price_div is not None:
        price = price_div.find("span", {"itemprop": "price"})
    description = ''
    price_str = ''
    for res in results:
        description = description + res.text
    if len(description) > 0 and price is not None:
        price_str = price_str + price.text
    re_w = re.compile(' ')
    price_str = re_w.sub('', price_str)
    sqls.append((uri[1], u"{}".format(description), price_str))

# Парстинг HTML соохранение результатов
def parse_html2(uri):
    art = uri[0]
    text = read_file(u"/home/alex/spider/html/{}.html".format(art))
    root = html.fromstring(text)
    results = root.xpath('//div[@class = "eItemProperties_text"]/text()')
    price_div = root.xpath('.//*[@class="bSaleBlocksContainer"]/noscript/span/text()')
    description = ''
    price_str = ''
    for res in results:
        description = description + res
    for price in price_div:
        price_str = price_str + price
    re_w = re.compile(' ')
    price_str = re_w.sub('', price_str)
    sqls.append((uri[1], u"{}".format(description), price_str))

# очередь
def task_queue(task, iterator, pool):
    counter = collections.Counter()
    with pool as executor:
        to_do_map = {}
        for uri in iterator:
            future = executor.submit(task, uri)
            to_do_map[future] = uri
        done_iter = futures.as_completed(to_do_map)
        done_iter = tqdm(done_iter, total=len(iterator))
        for future in done_iter:
            counter['status'] += 1
    return counter

# шаблон URL
url_parse = u"http://www.ozon.ru/?context=search&text={}"
sqls = []
data_from_xls = xls_reader.get_arts_from_xls()
arts_unique = data_from_xls[:]
http = urllib3.PoolManager(10, headers=None, timeout=5, retries=1)

def start_process():
    executor = futures.ThreadPoolExecutor(max_workers=10)
    results_www = task_queue(parse_www, arts_unique, executor)

    executor = futures.ThreadPoolExecutor(max_workers=2)
    results_html = task_queue(parse_html2, arts_unique, executor)

    xls_reader.put_stat_toxls(sqls)
start_process()


# https://www.wildberries.ru/catalog/0/search.aspx?search=Valliant&sort=popular
# div class=pager
# div class=pageToInsert
# a class=around-active GET ALL PAGES
# div class=dtList
# a class=ref_goods_n_p get href