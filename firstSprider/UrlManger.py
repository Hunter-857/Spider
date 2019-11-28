# coding:utf-8


class UrlManger(object):

    def __init__(self):
        self.new_urls = set()   # 未爬取的url
        self.old_urls = set()   # 爬取过的url

    def new_url_size(self):
            return len(self.new_urls)

    def old_url_size(self):
            return len(self.old_urls)

    def has_new_url(self):
        return self.new_url_size() != 0

    def add_new_url(self, url):
        if url is None:
            return
        if url not in self.new_urls and url not in self.old_urls:
            self.new_urls.add(url)

    def add_new_urls(self, urls):
        if urls is None or len(urls) ==0:
            return
        for url in urls:
            self.add_new_url(url)

    def get_new_url(self):
        new_url = self.new_urls.pop()
        self.old_urls.add(new_url)
        return  new_url
