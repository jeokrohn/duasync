# -*- coding: utf-8 -*-
"""
Get all Spiegel articles of the last seven days; serial
"""

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor, as_completed
import datetime

MAIN_URL = 'https://www.spiegel.de/schlagzeilen/index-siebentage.html'


class Article:
    def __init__(self, date, url, title, content=None):
        self.date = date
        self.url = url
        self.title = title
        self.content = content

    def get_content(self):
        print(f'Getting content for {self.date}, {self.title}')
        with requests.Session() as session:
            resp = session.get(self.url)
            resp.raise_for_status()
            content = resp.text
        soup = BeautifulSoup(content, 'html.parser')
        paragraphs = soup('p')
        self.content = '\n'.join((p.text for p in paragraphs))
        print(f'    Got content for {self.date}, {self.title}')


def get_spiegel_news():
    with requests.Session() as session:
        resp = session.get(url=MAIN_URL)
        resp.raise_for_status()
    soup = BeautifulSoup(resp.content, 'html.parser')
    days = soup('div', {'data-sponlytics-area': 'seg-list'})

    articles = []
    for day in days:
        # all links (ignore Spiegel Plus
        date = day.find(class_='schlagzeilen-date-headline')
        assert date, "Date headline not found"
        date = date.text
        links = day(lambda tag: tag.name == 'a' and tag.get('class') is None)
        for link in links:
            title = link['title']
            url = link['href']
            url = urljoin(MAIN_URL, url)
            articles.append(Article(date=date, url=url, title=title))

    # now that we have all articles we only need to get the content
    # either use ProcessPoolExecutor or ThreadPoolExecutor instance
    pool_executor = ProcessPoolExecutor
    # pool_executor = ThreadPoolExecutor

    with pool_executor(max_workers=10) as executor:
        # assign all tasks to executors and wait for results
        # as_completed is an iterator and takes an iterable of futures and returns each result as they become available
        start = datetime.datetime.utcnow()
        list(executor.map(lambda article:article.get_content(), articles))
        #list(as_completed([executor.submit(article.get_content()) for article in articles]))
        diff = datetime.datetime.utcnow() - start
        print(f'Got {len(articles)} articles in {diff.total_seconds()} seconds')


if __name__ == '__main__':
    get_spiegel_news()
