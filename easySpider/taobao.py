from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


def open_broswers(browser, url):
    urls_inpage = []
    browser.get(url)
    for i in range(1, 45):
        xpath1 = "//div[contains(@data-index,'" + str(i) + "')]/div/div/div/a"
        elements = browser.find_element(by=By.XPATH, value=xpath1)
        urls_inpage.append(elements.get_attribute('href'))
    return urls_inpage


def open_next_page(browser, items):
    for i in range(0, len(items)):
        browser.get(items[i])
        xpath = '/html/body/div[8]'
        try:
            login_in_ele = browser.find_element(by=By.XPATH, value=xpath)
            browser.find_element(by=By.XPATH, value="//*[@id='sufei-dialog-close']").click()
        except Exception:
            pass
        ## print("商品Url:"+items[i])
        get_page_video_url(browser, items[i])


def get_page_video_url(browser, items):
    if not (get_page_video_common_model_url(browser, items)):
        if not (get_page_video_other_model_url(browser, items)):
            print(items + "没有video")


def get_page_video_common_model_url(browser, items):
    try:
        browser.find_element(By.XPATH, value="//*[contains(@class, 'tb-booth tb-pic tb-main-pic tb-video-mode')]")
        browser.find_element(By.XPATH, value="//*[contains(@class, 'vjs-center-start vjs-button')]").click()
        video_element = browser.find_element(By.XPATH, value="//*[contains(@class,'lib-video')]/video")
        print(video_element.get_attribute("src"))
        return True
    except Exception:
        return False


def get_page_video_other_model_url(browser, items):
    try:
        WebDriverWait(browser, 20, 0.5).until(
            EC.presence_of_element_located((By.XPATH, "//*[contains(@class, 'tm-video-box')]/div/video")))
        print(browser.find_element(By.XPATH,
                                   value="//*[contains(@class, 'tm-video-box')]/div/video").get_attribute('src'))
        return True
    except Exception:
        return False



if __name__ == '__main__':
    browser = webdriver.Firefox()
    options = webdriver.FirefoxOptions()
    options.add_argument('proxy-server=' + "61.182.88.133:40087")
    url = "https://kxuan.taobao.com/search.htm?kxuan_swyt_item=30380&ruletype=2&searchtype=item&uniq=pid&navigator=all&id=3895&is_spu=0&enginetype=0"
    items = open_broswers(browser, url)
    open_next_page(browser, items)
