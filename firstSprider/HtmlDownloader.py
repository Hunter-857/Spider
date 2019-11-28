# coding:utf-8
import requests as re


class HtmlDownloader(object):

    def download(self,url):
        if url is None:
            return
        user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko" \
                     ") Chrome/69.0.3497.100 Safari/537.36"
        header = {"user_agent": user_agent}
        response = re.get(url, headers=header, allow_redirects=False)
        # response = re.get(url)
        print(response.status_code)
        if response.status_code == 200 or response.status_code == 302:
            response.encoding = "utf-8"
            return response.text