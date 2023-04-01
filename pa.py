# -*- coding: utf-8 -*-
'''

从target_url 爬取m3u8，视频的index，之后在下载对应的 ts 文件，合并到一个文件。电脑直接可以打开看

http://dh5.cntv.lxdns.com/asp/h5e/hls/1200/0303000a/3/default/f384aab231ba4178af291833f0c45a85/3.ts
'''
import requests
import re

target_url = "https://v.kuaishouvod.com/m3u8/1/1904"
def ts_long():
    #url = target_url+"/index.m3u8"
    url = "http://dh5.cntv.lxdns.com/asp/h5e/hls/main/0303000a/3/default/f384aab231ba4178af291833f0c45a85/main.m3u8?maxbr=2048&amp;contentid=15120519184043"
    resp = requests.get(url)
    data = resp.text
    print(data)
    indexs_list = re.findall(r'index(.*?).ts', data)
    print(indexs_list)
    number = int(indexs_list[-1])
    return number

# http://dh5.cntv.myalicdn.com/asp/h5e/hls/1200/0303000a/3/default/f384aab231ba4178af291833f0c45a85/3.ts
# http://dh5.cntv.myalicdn.com/asp/h5e/hls/1200/0303000a/3/default/f384aab231ba4178af291833f0c45a85/4.ts
def start_read_ts(number, file_name):
    for i in range(0, number):
        # https://v.kuaishouvod.com/m3u8/1/1905/index.m3u8
        cctv_target_url = " http://dh5.cntv.myalicdn.com/asp/h5e/hls/1200/0303000a/3/default/f384aab231ba4178af291833f0c45a85"
        url = cctv_target_url+"/{}".format(i)+".ts"
        print(url)
        headers = {
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Connection": "keep-alive",
            "Host": "bf1.aikan-jx.com",
            "sec-ch-ua": "\" Not;A Brand\";v=\"99\", \"Google Chrome\";v=\"97\", \"Chromium\";v=\"97\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"Windows\"",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "cross-site",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36"
        }
        response = requests.request("GET", url, headers=headers)
        print("write" + str(i))
        data = response.content
        # with open(file_name, 'ab+') as f:
        #     f.write(data)
        #     f.flush()
        #     print("写入第{}文件成功".format(i))
        with open("out/video_{}".format(i)+".ts", 'ab+') as f:
            f.write(data)
            f.flush()
            print("写入第{}文件成功".format(i))


if __name__ == '__main__':
    ##number = ts_long()
    start_read_ts(25, "video.ts")
