import requests
from marshmallow.compat import urlparse

url = "https://search.jd.com/brand.php"
# ?keyword=%E5%A5%B3%E8%A3%85&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&wq=%E5%A5%B3%E8%A3%85&cid2=1343
# ret = dict(urlparse.parse_qsl(urlparse.urlsplit(url).query))
# params = {'keyword': '女装', 'enc': 'utf-8', 'qrst': '1', 'rt': '1', 'stop': '1', 'vt': '2', 'wq': '女装', 'cid2': '1343'}
# params = {'keyword': '服饰内衣', 'enc': 'utf-8', 'qrst': '1', 'rt': '1', 'stop': '1', 'vt': '2', 'wq': '服饰内衣', 'cid1': '1315'}
params = {'keyword': '服饰内衣', 'enc': 'utf-8', 'qrst': '1', 'rt': '1', 'stop': '1', 'vt': '2', 'wq': '服饰内衣',
          'cid1': '1315'}
headers = {
    "accept": "*/*",
    "accept-encoding": "gzip, deflate, br",
    "accept-language": "zh-CN,zh;q=0.9",
    "content-length": "567",
    "content-type": "application/x-www-form-urlencoded",
    # cookie: unpl=V2_ZzNtbUcEQUZxW04DKUlfB2JXGwpKVUIQJwwSA3kYXgZuUBBUclRCFX0UR11nGloUZwIZWUVcQxVFCEdkeBBVAWMDE1VGZxBFLV0CFSNGF1wjU00zQwBBQHcJFF0uSgwDYgcaDhFTQEJ2XBVQL0oMDDdRFAhyZ0AVRQhHZHsaXwJmBhFYQlJzJXI4dmR8Gl0GbwIiXHJWc1chVEZWfh1bSGcAEVpDUkAQdQ12VUsa; __jdv=76161171|baidu-pinzhuan|t_288551095_baidupinzhuan|cpc|0f3d30c8dba7459bb52f2eb5eba8ac7d_0_4b3b5b9fca234e8f9304c5ef30328b38|1566874573361; __jdu=1226042414; areaId=1; ipLoc-djd=1-2800-0-0; PCSYCityID=CN_110000_110100_110108; shshshfpa=9416a6bd-834b-7baa-b3c2-2830d1c545d4-1566874577; __jda=122270672.1226042414.1566874573.1566874573.1566874573.1; __jdc=122270672; 3AB9D23F7A4B3C9B=DDSD5RC7VTD4AOBSLUAWDZIR6V6OCSZQITFDJLIVSNZ7IISIEIPTUG567DDZDK2NRGNKNX6GUNWEXKBGKXJBIBY5WA; xtest=8246.cf6b6759; shshshfp=2d22f30ece41979b8304fb10f674035a; shshshfpb=tDiWRTkI5JuHJQjUutean%20A%3D%3D; rkv=V0200; __jdb=122270672.5.1226042414|1.1566874573; shshshsID=51e4fe6b12d3d213e115103caebd7098_3_1566874628740; qrsc=2
    "origin": "https://search.jd.com",
    "referer": "https://search.jd.com/Search?keyword=%E5%A5%B3%E8%A3%85&enc=utf-8&wq=%E5%A5%B3%E8%A3%85&pvid=0f899478d07c48748f14adb0f2a5715e",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36",
    "x-requested-with": "XMLHttpRequest",
}
data = {
    "brand-172451": "1",
    "brand-237110": "1",
    "brand-67494": "1",
    "brand-89430": "1",
    "brand-19767": "1",
    "brand-172655": "1",
    "brand-140985": "1",
    "brand-7343": "1",
    "brand-15042": "1",
    "brand-68781": "1",
    "brand-84131": "1",
    "brand-197077": "1",
    "brand-39323": "1",
    "brand-14573": "1",
    "brand-128569": "1",
    "brand-227055": "1",
    "brand-185111": "1",
    "brand-441378": "1",
    "brand-6823": "1",
    "brand-33321": "1",
    "brand-188790": "1",
    "brand-123231": "1",
    "brand-4116": "1",
    "brand-106938": "1",
    "brand-56696": "1",
    "brand-214774": "1",
    "brand-4448": "1",
    "brand-165618": "1",
    "brand-230748": "1",
    "brand-61276": "1",
    "brand-33069": "1",
    "brand-87334": "1",
    "brand-1777": "1",
    "brand-63": "1",
    "brand-19310": "1",
    "brand-79620": "1",
    "brand-19394": "1",
    "brand-355132": "1",
    "brand-340649": "1",
    "brand-7238": "1",
    "brand-71901": "1",
}


def get_all_brands():
    with open('brands.html', 'wb') as f:
        f.write(requests.post(url, params=params, headers=headers, data=data).content)


def parse_url(url):
    ret = dict(urlparse.parse_qsl(urlparse.urlsplit(url).query))
    print(ret)


if __name__ == '__main__':
    # tmall_url = "https://list.tmall.com/ajax/allBrandShowForGaiBan.htm?t=0&q=%C5%AE%D7%B0%2F%C5%AE%CA%BF%BE%AB%C6%B7&sort=s&style=g&from=.list.pc_1_searchbutton&spm=a220m.1000858.a2227oh.d100&userIDNum=&tracknick="
    # parse_url(tmall_url)
    pass
