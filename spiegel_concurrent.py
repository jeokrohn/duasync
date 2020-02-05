# -*- coding: utf-8 -*-
"""
Get all Spiegel articles of the last seven days; serial
"""

import requests
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor, as_completed
import datetime

from spiegel_base import ArticleBase

# maximum workers in executor pool.
# "play" w/ this value...
MAX_WORKERS = 20


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
    # either use ProcessPoolExecutor or ThreadPoolExecutor instance
    use_process_pool_executor = False
    if use_process_pool_executor:
        pool_executor = ProcessPoolExecutor
    else:
        pool_executor = ThreadPoolExecutor

    with pool_executor(max_workers=MAX_WORKERS) as executor:
        # assign all tasks to executors and wait for results
        # as_completed is an iterator and takes an iterable of futures and returns each result as they become available
        start = datetime.datetime.utcnow()
        if use_process_pool_executor:
            # as_completed is an iterator and takes an iterable of futures and returns each result as they become
            # available
            list(as_completed([executor.submit(article.get_content()) for article in articles]))
        else:
            list(executor.map(lambda article: article.get_content(), articles))
        diff = datetime.datetime.utcnow() - start
        print(f'Got {len(articles)} articles in {diff.total_seconds()} seconds')


if __name__ == '__main__':
    get_spiegel_news()
