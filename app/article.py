
class Article(object):
    def __init__(self, article, url, compression_rate, total_words, total_words_removed):
        self.article = article
        self.url = url
        self.compression_rate = compression_rate
        self.total_words = total_words
        self.total_words_removed = total_words_removed

    def get_article(self):
        return self.article

    def get_url(self):
        return self.url

    def get_compression_rate(self):
        return self.compression_rate

    def get_total_words(self):
        return self.total_words

    def get_total_words_removed(self):
        return self.total_words_removed
