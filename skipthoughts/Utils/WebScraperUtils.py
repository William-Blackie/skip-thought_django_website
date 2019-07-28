from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup

"""
Author: William Blackie

Class for the scraping of URLs and returning the articles text.
"""


class WebScraperUtils:

    def __init__(self):
        pass

    @staticmethod
    def get_url(url, is_lists_enabled):
        """
        Attempts to get content from given URL; for best results use a bbc.co.uk or theguardian.co.uk article.
        :param url: String url of desired web page to scrape.
        :param is_lists_enabled: Boolean to enable Li elements to be included.
        :return: List where List[0] is a concatenated string of the article or None if not valid URL.
        """

        try:
            with closing(get(url, stream=True)) as resp:
                if is_good_response(resp):
                    return get_any_website_html(resp.content, is_lists_enabled)
                else:
                    return None

        except RequestException as e:
            log_error('Error during requests to {0} : {1}'.format(url, str(e)))
            return None


def is_good_response(resp):
    """
    Returns True if the response seems to be HTML, False otherwise.
    :param resp: response from request.get()
    :return: content of resp in HTML.
    """
    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200
            and content_type is not None
            and content_type.find('html') > -1)


def get_any_website_html(raw_html, is_lists_enabled):
    """
    Creates a concatenate string of the article, with or without li elements included from any URL.
    For best results use bbc.co.uk or thegaurdian.co.uk URLs.
    :param raw_html: resp.content from response.get().
    :param is_lists_enabled: Boolean to include <Li> elements.
    :return: List where List[0] is a concatenated String of the article.
    """
    article = [""]
    parsed_html = BeautifulSoup(raw_html.decode('utf-8', 'ignore'), 'html.parser')
    text_body = parsed_html.findAll('p')

    for text in text_body:
        article[0] += text.text

    if not is_lists_enabled:
        try:
            text_lists = parsed_html.ffindAll('li')
            if len(text_lists) > 0:
                for text in text_lists:
                    article[0] += text.text
        except TypeError:
            print "Article does not contain <li> elements"
    return article


def log_error(e):
    """
    Prints errors to console.
    :param e: Exception e
    :return: none
    """
    print(e)
