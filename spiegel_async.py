# -*- coding: utf-8 -*-
"""
Get all Spiegel articles of the last seven days; using asyncio
"""

from bs4 import BeautifulSoup
import asyncio
import aiohttp
import datetime

from spiegel_base import ArticleBase


class Article(ArticleBase):

    async def get_content(self, session):
        print(f'Getting content for {self.date}, {self.title}')
        try:
            async with session.get(self.url) as resp:
                resp.raise_for_status()
                content = await resp.text()
        except (aiohttp.ClientResponseError, aiohttp.ClientConnectionError) as e:
            print(f'!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!GET on {self.url} failed: {e}')
        # soup = BeautifulSoup(content, 'html.parser')
        # paragraphs = soup('p')
        # don't actually store the content (we don't want to mess up the memory footprint
        # self.content = '\n'.join((p.text for p in paragraphs))
        print(f'    Got content for {self.date}, {self.title}')


async def get_spiegel_news():
    articles = Article.get_articles()

    # now that we have all articles we only need to get the content
    async with aiohttp.ClientSession() as session:
        tasks = [article.get_content(session) for article in articles]
        start = datetime.datetime.utcnow()
        await asyncio.gather(*tasks)
        diff = datetime.datetime.utcnow() - start
    print(f'Got {len(articles)} articles in {diff.total_seconds()} seconds')


if __name__ == '__main__':
    asyncio.run(get_spiegel_news())
