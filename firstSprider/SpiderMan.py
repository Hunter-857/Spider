# coding:utf-8
from firstSprider.DataOutput import DataOutput
from firstSprider.HtmlDownloader import HtmlDownloader
from firstSprider.HtmlParser import HtmlParser
from firstSprider.UrlManger import UrlManger


class SpiderMan(object):
    def __init__(self):
        self.manager = UrlManger()
        self.downloader = HtmlDownloader()
        self.urlmanage = UrlManger()
        self.parser = HtmlParser()
        self.output = DataOutput()

    def crawl(self, root_url):
        self.manager.add_new_url(root_url)

        while self.manager.has_new_url() and self.manager.old_url_size() < 100:
                new_url = self.manager.get_new_url()
                html = self.downloader.download(new_url)
                new_urls, data = self.parser.parser(new_url, html)
                self.manager.add_new_urls(new_urls)
                self.output.store_data(data)
        self.output.output_html()


if __name__ == '__main__':
    SpiderMan().crawl("https://baike.baidu.com/item/284853.html")