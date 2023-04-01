## https://vd6.l.qq.com/proxyhttp


import requests as re
import json
import re as  regex
from tqdm import tqdm


def get_qq_videos(url,json_body=None):
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
    response = re.request("Post", url=url, headers=headers, json=json_body)
    json_data = response.content
    json_object = json.load(json_data)
    print(json_object)

# video = info['vl']['vi'][0]['ul']['m3u8'] 解析 m3u8
def reading_m3u8_file():
    with open("m3u8", "rb") as file:
        lines = file.read().decode('utf-8')
        info_list = lines.split("\n")
        url_result = []
        for item in info_list:
            if not item.startswith("#"):
                url_result.append(item)
        # url_list = regex.findall(r'index(.*?).ts', info_list)
        # print(url_result)
        return url_result
def merge_ts_to_videos_url(url_list, file_name):
    assert url_list[0].startswith("http"), 'please check url'
    headers = {
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Connection": "keep-alive",
        "Host": "ltsbjty.gtimg.com",
        "Origin": "https: // v.qq.com",
        "Referer":"https: // v.qq.com" ,
        "sec-ch-ua": "\" Not;A Brand\";v=\"99\", \"Google Chrome\";v=\"97\", \"Chromium\";v=\"97\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "cross-site",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
    }
    for i in tqdm(range(0, len(url_list)-1)):
        print("start read ulr:{}".format(url_list[i]))
        response = re.request("GET", url_list[i], headers=headers)
        data = response.content
        with open(file_name, 'ab+') as f:
            print("writeing file {}".format(str(i)))
            f.write(data)
            f.flush()
            print("写入第{}文件成功".format(i))


if __name__ == '__main__':
    # params = {"buid":"vinfoad","vinfoparam":"charge=0&otype=ojson&defnpayver=3&spau=1&spaudio=0&spwm=1&sphls=2&host=v.qq.com&refer=https%3A%2F%2Fv.qq.com%2Ftxp%2Fiframe%2Fplayer.html&ehost=https%3A%2F%2Fv.qq.com%2Ftxp%2Fiframe%2Fplayer.html&sphttps=1&encryptVer=8.1&cKey=5E050731A729C24559DBBD3344E1E376777BE4DBCD54063376C3EEEBD70201B22515487851F6668DEB0CB5935901B071E647334CC4875DF23F1DA1F7E3575FEDEBE0644881EA87C7A70146634BD6E9249B58FBE7CD8CC18A1B65E9A795C4600EA67D4FD252CB1AF20B852BB3DA406FD92515ED50F7340D2B275FD694326C3D42F88596222A4ADBC9D915D1A54115F455040B4A96CBFA4C6079DF9AC41F5DF563A7B15065ED651223984F1A18E0D373E4585C40AB291A2B78E57208D2D7367321523898F2B2CC396937C0A3783A85BBFD&clip=4&guid=4c597115ed95d91e&flowid=c1c659f5e303eb3790af144a74255716&platform=10201&sdtfrom=v1010&appVer=3.5.57&unid=&auth_from=&auth_ext=&vid=p3363s20y8r&defn=&fhdswitch=0&dtype=3&spsrt=2&tm=1680187277&lang_code=0&logintoken=&spvvpay=1&spadseg=3&spav1=15&hevclv=28&spsfrhdr=0&spvideo=0&spm3u8tag=67&spmasterm3u8=3&drm=40","sspAdParam":"{\"ad_scene\":1,\"pre_ad_params\":{\"ad_scene\":1,\"user_type\":-1,\"video\":{\"base\":{\"vid\":\"p3363s20y8r\"},\"is_live\":false,\"type_id\":0,\"referer\":\"\",\"url\":\"https://v.qq.com/txp/iframe/player.html?origin=https%3A%2F%2Fmp.weixin.qq.com&containerId=js_tx_video_container_0.6411197454683779&vid=p3363s20y8r&width=677&height=380.8125&autoplay=false&allowFullScreen=true&chid=17&full=true&show1080p=false&isDebugIframe=false\",\"flow_id\":\"c1c659f5e303eb3790af144a74255716\",\"refresh_id\":\"d809ba91a003fc027335918e1c96fede_1680186498\"},\"platform\":{\"guid\":\"4c597115ed95d91e\",\"channel_id\":0,\"site\":\"web\",\"platform\":\"in\",\"from\":0,\"device\":\"pc\",\"play_platform\":10201,\"pv_tag\":\"\"},\"player\":{\"version\":\"1.17.2\",\"plugin\":\"1.16.1\",\"switch\":1,\"play_type\":\"0\"},\"token\":{\"type\":0,\"vuid\":0,\"vuser_session\":\"\",\"app_id\":\"\",\"open_id\":\"\",\"access_token\":\"\"}}}","adparam":"pf=in&pf_ex=pc&pu=-1&pt=0&platform=10201&from=0&flowid=c1c659f5e303eb3790af144a74255716&guid=4c597115ed95d91e&coverid=&vid=p3363s20y8r&chid=0&tpid=&refer=&url=https%3A%2F%2Fv.qq.com%2Ftxp%2Fiframe%2Fplayer.html%3Forigin%3Dhttps%253A%252F%252Fmp.weixin.qq.com%26containerId%3Djs_tx_video_container_0.6411197454683779%26vid%3Dp3363s20y8r%26width%3D677%26height%3D380.8125%26autoplay%3Dfalse%26allowFullScreen%3Dtrue%26chid%3D17%26full%3Dtrue%26show1080p%3Dfalse%26isDebugIframe%3Dfalse&lt=&opid=&atkn=&appid=&uid=&tkn=&rfid=d809ba91a003fc027335918e1c96fede_1680186498&v=1.17.2&vptag=&ad_type=LD%7CKB%7CPVL&live=0&appversion=3.2.30&ty=web&adaptor=1&dtype=1&resp_type=json"}
    # target_url = "https://vd6.l.qq.com/proxyhttp"
    # json_body = json.dumps(params)
    # get_qq_videos(target_url, json_body)
    url_list = reading_m3u8_file()
    new_list = []
    for item in url_list:
        tmp = "https://ltsbjty.gtimg.com/UdM68O-Yud8n0c-KrcuE-9jSL_qVh7DDYTLj19vy7zCjK77eeHSfk2kscseFhX2Qz_CJ37_lq_aHLSUey0vcJXzBJS2ggHlf8Hg-e9enobFQI1W602-cA1Tbbpo2s5Co4vO9rFB4LpNlxbxYO_woLunABoLxDESe8vXALBBH7aE/"+item
        # print(tmp)
        new_list.append(tmp)
    merge_ts_to_videos_url(new_list, "out/first.mp4")