import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

MAX_ARTICLES = None


class Done(Exception):
    pass


class ArticleBase:
    """
    Base class for Articles scraped from the spiegel.de website
    """
    MAIN_URL = 'https://www.spiegel.de/schlagzeilen/'

    def __init__(self, date, url, title, content=None):
        self.date = date
        self.url = url
        self.title = title
        self.content = content

    @classmethod
    def get_articles(cls):
        """
        Scrape spiegel.de website to get a list of articles with their respective link and date of publication
        :return:
        """
        with requests.Session() as session:
            resp = session.get(url=ArticleBase.MAIN_URL)
            resp.raise_for_status()
        # using beautifulsoup to scrape the website.
        soup = BeautifulSoup(resp.content, 'html.parser')

        main = soup.find('main')
        assert main, "Couldn't find 'main' tag"

        # the 'section' is what we are interested in
        section = next((c for c in main.children if c.name == 'section'), None)
        assert section is not None, "Did not find the expected 'section' child"

        # that section as one section tag per day
        day_sections = [c for c in section.children if c.name == 'section']
        assert day_sections, 'Failed to find sections for the days'

        # the list of articles scraped from the website
        articles = []
        try:
            for day in day_sections:
                # each section has a header with the date
                header = day.find('header')
                assert header is not None
                date = header.text.strip()

                # paid links have something like this:
                # <span class="inline-flex align-middle leading-none mr-4" data-contains-flags="paid">
                # ...
                # </span>
                def paid(tag):
                    span_tags = tag(lambda t: t.name == 'span')
                    # is there a 'span' tag marked as 'paid'?
                    return next((s for s in span_tags if s.get('data-contains-flags') == 'paid'), None) is not None

                links = day(lambda t: t.name == 'a' and not paid(t))
                for link in links:
                    title = link['title']
                    url = link['href']
                    url = urljoin(ArticleBase.MAIN_URL, url)
                    articles.append(cls(date=date, url=url, title=title))
                    if MAX_ARTICLES and len(articles) >= MAX_ARTICLES:
                        raise Done  # poor man's "GOTO" to break out of two nested loops :-)
        except Done:
            pass
        print(f'Found {len(articles)} articles')
        return articles

    def __repr__(self):
        return f'{self.__class__.__name__}({self.date}, {self.title})'
