# -*- coding: utf-8 -*-
"""
Get all Spiegel articles of the last seven days; using asyncio
"""

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import asyncio
import aiohttp
import datetime

MAIN_URL = 'https://www.spiegel.de/schlagzeilen/index-siebentage.html'


class Article:

    def __init__(self, date, url, title, content=None):
        self.date = date
        self.url = url
        self.title = title
        self.content = content

    async def get_content(self):
        print(f'Getting content for {self.date}, {self.title}')
        async with aiohttp.ClientSession() as session:
            async with session.get(self.url) as resp:
                resp.raise_for_status()
                content = await resp.text()
        soup = BeautifulSoup(content, 'html.parser')
        paragraphs = soup('p')
        # don't actually store the content (we don't want to mess up the memory footprint
        # self.content = '\n'.join((p.text for p in paragraphs))
        print(f'    Got content for {self.date}, {self.title}')


async def get_spiegel_news():
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
    tasks = [article.get_content() for article in articles]
    start = datetime.datetime.utcnow()
    await asyncio.gather(*tasks)
    diff = datetime.datetime.utcnow() - start
    print(f'Got {len(articles)} articles in {diff.total_seconds()} seconds')

if __name__ == '__main__':
    asyncio.run(get_spiegel_news())
