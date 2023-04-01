
video_list = [
    "https://www.bilibili.com/video/BV1a24y1S7Nw/",  # 熟悉包
    "https://www.bilibili.com/video/BV1Lb411Q7HT/"
    "https://www.bilibili.com/video/BV1ED4y1M71A/",
    "https://www.bilibili.com/video/BV17v4y1a75T/"
]

# 以下ip使用自己可使用的代理IP
proxy_arr = [
    '--proxy-server=http://47.101.44.122:80',
    '--proxy-server=http://180.97.34.35:80',
    '--proxy-server=http://219.239.142.253:3128',
    '--proxy-server=http://47.92.234.75:80	',
    '--proxy-server=http://60.205.132.71:80',
    '--proxy-server=https://60.255.151.82:80',
    '--proxy-server=https://116.196.85.150:3128'
]

user_agent_MacOS  = (
  "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_4) " +
  "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.57 Safari/537.36"
  )

# https://registry.npmmirror.com/binary.html?path=chromedriver/

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import random
import time

MAX_TRY = 10
TIME_TRY = 0
def find_time_txt(driver,videotime_xpath, video_controller_xpath):
    driver.execute_script(
        "document.getElementsByClassName('bpx-player-container')[0].setAttribute('data-ctrl-hidden', false)") # 显示
    video_time_i = driver.find_element_by_xpath(videotime_xpath)
    video_time_controller_i = driver.find_element_by_xpath(video_controller_xpath)
    show = video_time_controller_i.get_attribute("data-shadow-show")
    if not show:
        driver.execute_script(
            "document.getElementsByClassName('bpx-player-container')[0].setAttribute('data-ctrl-hidden' ,false)")
    driver.execute_script(
        "document.getElementsByClassName('bpx-player-container')[0].setAttribute('data-ctrl-hidden',true)")
    return video_time_i.text

def open_browser_and_watch_video():
    global TIME_TRY
    global MAX_TRY
    total = 380
    video_time = "//*[@id=\"bilibili-player\"]//span[starts-with(@class,'bpx-player-ctrl-time-duration')]"
    video_time_controller = "//*[@id=\"bilibili-player\"]/div/div/div[1]/div[1]/div[10]/div[2]"

    for i in range(0, total):
        print("总共:" + str(total))
        chrome_options = Options()
        proxy = random.choice(proxy_arr)  # 随机选择一个代理
        chrome_options.add_argument(proxy)  # 添加代理
        browser = webdriver.Chrome("D:\\workspeace\\chromedriver.exe")
        random_one = random.randint(0, len(video_list) - 1)
        browser.get(video_list[random_one])
        time.sleep(5) # 等一下页面加载
        time_txt = ''
        try:
            time_txt = find_time_txt(browser, video_time, video_time_controller)
        except Exception as e:
            print(e)
            time.sleep(2)
            print("TRY again")
            if TIME_TRY < MAX_TRY or time_txt == '':
                TIME_TRY = TIME_TRY + 1
                time_txt = find_time_txt(browser, video_time, video_time_controller)
        print("视频时间长:"+time_txt)
        duration = time_txt.split(":")
        total_sec = 60 * float(duration[0]) + float(duration[1])
        print("total_need_seed:" + str(total_sec))
        wait_time = random.randrange(0, int(total_sec), 1)
        print("窗口等待时间:"+str(wait_time))
        time.sleep(wait_time)
        browser.close()


xiguan_list = [
    "https://www.ixigua.com/6867768295156613635",
    "https://www.ixigua.com/6877156396606063111",
    "https://www.ixigua.com/6868244549928649228",

]
class BiBiAuto:
    def __init__(self,  driver_path):
        self.driver_path = driver_path
        self.video_time = "//*[@id=\"bilibili-player\"]//span[starts-with(@class,'bpx-player-ctrl-time-duration')]"
        self.video_time_controller = "//*[@id=\"bilibili-player\"]/div/div/div[1]/div[1]/div[10]/div[2]"


    def open_browser_and_watch_video(self):pass

if __name__ == '__main__':
    open_browser_and_watch_video()