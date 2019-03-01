
class Article(object):
    def __init__(self, article, url, compression_rate):
        self.article = article
        self.url = url
        self.compression_rate = compression_rate

    def get_article(self):
        return self.article

    def get_url(self):
        return self.url

    def get_compression_rate(self):
        return self.compression_rate
