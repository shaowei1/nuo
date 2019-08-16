import requests

# PySocks
proxies = {
    "http": "socks5h://127.0.0.1:1080",
    "https": "socks5h://127.0.0.1:1080",
}

proxies = {}


# bar

def download_file(url, local_filename=None):
    if local_filename is None:
        local_filename = url.split('/')[-1]
        print(local_filename)
    # NOTE the stream=True parameter below
    with requests.get(url, stream=True, proxies=proxies) as r:
        r.raise_for_status()
        with open(local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                if chunk:  # filter out keep-alive new chunks
                    f.write(chunk)
                    # f.flush()
    return local_filename


#
# try:
#     for index, i in enumerate(list(range(4, 23)) + ["23E24"]):
#         print("start download the {} movie".format(i))
#         if isinstance(i, int) and i < 10:
#             i = '0' + str(i)
#         download_file(
#             'http://tj-download.weiyun.com/%E7%A0%B4%E4%BA%A7%E5%A7%90%E5%A6%B9S01E{}.mp4?ver=6100&rkey=2cc2b96d0877cd360541e809490b6f9b5f7d814a522e35d55dbaf79390b0502b83810f5ec5acc8e0623a3819bfa61e20e4f93d536c3128013ae3bcc4719e5476'.format(
#                 i), '/home/www/part3/Video/破产姐妹S01E{}.mp4'.format(i))
#         print("end download the {} movie".format(i))
#
# except Exception as e:
#     print(e)
#     print("failed download the {} movie".format(i))
# download_file()

for i in """20190703-AI标签.pdf
data.xml
package(1).json
process.png
Untitled.csv
update.json
WechatIMG48.png
WechatIMG49.png
产品更新规则schame.txt
修改商品的传参
入参(4).txt
商品发布xml.xml
天猫发布接口问题-青木txt文件.rar
""".split('\n'):
    tmp = i.strip()
    # download_file('http://192.168.15.33:8000/{}'.format(tmp))
