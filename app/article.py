"""
Author: William Blackie
Class for storing article data.
"""


class Article(object):
    def __init__(self, article, url, compression_rate, total_words, total_words_removed):
        """
        Method for creating an Article Object.
        :param article: String of an article.
        :param url: String of a URL.
        :param compression_rate: Float (0.1-1.0).
        :param total_words: Int total words in the article.
        :param total_words_removed: Int total words removed from the original article.
        """
        self.article = article
        self.url = url
        self.compression_rate = compression_rate
        self.total_words = total_words
        self.total_words_removed = total_words_removed

    def get_article(self):
        """
        method for returning article.
        :return: String of an article.
        """
        return self.article

    def get_url(self):
        """
        method for returning URL.
        :return: String of an URL.
        """
        return self.url

    def get_compression_rate(self):
        """
         method for returning the compression_rate.
        :return: Float of the compression_rate.
        """
        return self.compression_rate

    def get_total_words(self):
        """
        method for returning the total_words of an article.
        :return: Integer of the total words of the article.
        """
        return self.total_words

    def get_total_words_removed(self):
        """
        method for returning the removed_total_words of an article.
        :return: Integer of the total words removed from the article.
        """
        return self.total_words_removed
