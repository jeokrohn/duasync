# -*- coding: utf-8 -*-
"""
Get all Spiegel articles of the last seven days; serial
"""

import requests
import datetime
from spiegel_base import ArticleBase


class Article(ArticleBase):

    def get_content(self):
        print(f'Getting content for {self.date}, {self.title}')
        with requests.Session() as session:
            resp = session.get(self.url)
            resp.raise_for_status()
            content = resp.text
        # soup = BeautifulSoup(content, 'html.parser')
        # paragraphs = soup('p')
        # don't actually store the content (we don't want to mess up the memory footprint
        # self.content = '\n'.join((p.text for p in paragraphs))
        print(f'    Got content for {self.date}, {self.title}')


def get_spiegel_news():
    articles = Article.get_articles()

    # now that we have all articles we only need to get the content
    start = datetime.datetime.utcnow()
    for article in articles:
        article.get_content()
    diff = datetime.datetime.utcnow() - start
    print(f'Got {len(articles)} articles in {diff.total_seconds()} seconds')


if __name__ == '__main__':
    get_spiegel_news()
