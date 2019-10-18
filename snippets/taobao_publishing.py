# coding=utf-8
import os
import pprint
import time
import json
import urllib
import hashlib
import urllib.parse
import urllib.request
from collections import OrderedDict
from io import BytesIO
import requests

# 这里填写你申请到的APPkey
app_key = os.getenv('app_key', None)
appSecret = os.getenv('appSecret', None)


# 排序
def ksort(d):
    return [(k, d[k]) for k in sorted(d.keys())]


# MD5加密
def md5(s, raw_output=False):
    """Calculates the md5 hash of a given string"""
    res = hashlib.md5(s.encode())
    if raw_output:
        return res.digest()
    return res.hexdigest()


# 计算sign
def createSign(paramArr):
    sign = appSecret
    paramArr = ksort(paramArr)
    paramArr = OrderedDict(paramArr)
    for k, v in paramArr.items():
        if k != '' and v != '':
            sign += k + v
    sign += appSecret
    sign = md5(sign).upper()
    return sign


# 参数排序
def createStrParam(paramArr):
    strParam = ''
    for k, v in paramArr.items():
        if k != '' and v != '':
            strParam += k + '=' + urllib.parse.quote_plus(v) + '&'
    return strParam


# 高效API调用示例
def topapi(postparm, files=None):
    # 公共参数，一般不需要修改
    paramArr = {'app_key': app_key,
                'v': '2.0',
                'sign_method': 'md5',
                'format': 'json',
                'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
                'method': 'taobao.item.add',

                }

    paramArr = {**paramArr, **postparm}

    sign = createSign(paramArr)
    strParam = createStrParam(paramArr)
    strParam += 'sign=' + sign
    url = 'http://gw.api.taobao.com/router/rest?' + strParam

    if files is None:
        resp = requests.post(url, data=postparm)
    else:
        resp = requests.post(url, data=postparm, files=files)

    # res = urllib.request.urlopen(url).read()
    print(resp.status_code)
    return resp.content


link = [
    'https://cdn1.ecpro.com/images/10016/2000189/21a86515b9cb3fd8e9215fdc1dcc5b0f.jpg?sign=f1400f35d8ce6626fe33700cd2efa054&t=1560242162',
    'https://cdn1.ecpro.com/uploads/10016/2000189/654d5fafc29122d782dfd81b7770571b.jpg?sign=b9102e14d7f1d7aac2bfa78e2c9f36f4&t=1560242099']
session = '6201e07a83e95cdfhcba488e8133c7df651bc87f753d55a647395425'

pic = {
    'session': session,
    "image": link,
    "picture_category_id": "0",
    "image_input_title": "b.jpg",
}
user_info = {
    'session': session,
    "method": "taobao.miniapp.userInfo.get"

}


# b'{"error_response":{"code":11,"msg":"Insufficient isv permissions","sub_code":"isv.permission-api-package-limit","sub_msg":"scope ids is 381 382 11430 11612 11784 11852 12138 12159 12161 12166 14894","request_id":"1493caj2uxrk0"}}'
# print(topapi(user_info))


#
#
# 添加图片
def taobao_item_pic_upload(postparm):
    postparm['method'] = 'taobao.picture.upload'

    filenames = postparm.pop('image', '')
    resps = []
    picture_paths = []

    for filename in filenames:
        bbbb = BytesIO(requests.get(filename).content)
        files = [
            ('img', ('a.jpg', bbbb, 'Content-Type: image/jpg')),
        ]
        resp = json.loads(topapi(postparm, files).decode('utf-8'))
        picture_paths.append(resp.get("picture_upload_response").get("picture").get("picture_path").lstrip(
            "https://img.alicdn.com/imgextra/"))
        resps.append(resp)
    return picture_paths


# print(taobao_item_pic_upload(pic))

# sku测试数据
"""
['乳白色', '悦色']
['我不是真正的乳白色', '斩男色']
['S', '其他尺码']
[['www ' '' '11.00' '22']
 ['www ' '' '12.00' '33']
 ['www ' '' '13.00' '44']
 ['www ' '' '14.00' '55']]
"""

# 添加单个sku输入与响应
{'session': '620161295e988f770a77ZZ4bfe50b5f37fe4df857dacee41027411018', 'num_iid': '596689247876',
 'properties': '1627207:28341;20509:28315', 'quantity': '55', 'price': '14.00'}
{'item_sku_add_response': {
    'sku': {'created': '2019-06-10 16:55:08', 'iid': '596689247876', 'num_iid': 596689247876, 'sku_id': 4316926915261},
    'request_id': '5dkicse4dclv'}}

# 详情页模板
"""
<p data-spm-anchor-id="a2126o.11854294.0.i5.1d004831z2PxkG"><img align="absmiddle" src="https://img.alicdn.com/imgextra/i2/1027411018/O1CN01JIY1hc1JOHiIjWyRP_!!1027411018.jpg" style="max-width:750px" /></p>
# 横向排列
<p data-spm-anchor-id="a2126o.11854294.0.i5.1d004831z2PxkG"><img align="absmiddle" src="https://img.alicdn.com/imgextra/i3/1027411018/O1CN01ga8yfL1JOHh2OHEGe_!!1027411018.jpg" style="max-width:750px" /><img align="absmiddle" src="https://img.alicdn.com/imgextra/i4/1027411018/O1CN01S2qKxf1JOHhiZJN46_!!1027411018.jpg" style="max-width:750px" /></p>

# 纵向组合
<p data-spm-anchor-id="a2126o.11854294.0.i5.1d004831z2PxkG"><img align="absmiddle" src="https://img.alicdn.com/imgextra/i2/1027411018/O1CN01JIY1hc1JOHiIjWyRP_!!1027411018.jpg" style="max-width:750px" /></p>

<p data-spm-anchor-id="a2126o.11854294.0.i5.1d004831z2PxkG"><img align="absmiddle" src="https://img.alicdn.com/imgextra/i3/1027411018/O1CN01ga8yfL1JOHh2OHEGe_!!1027411018.jpg" style="max-width:750px" /></p>

<p data-spm-anchor-id="a2126o.11854294.0.i5.1d004831z2PxkG"><img align="absmiddle" src="https://img.alicdn.com/imgextra/i4/1027411018/O1CN01bPA7sW1JOHjNJsnsT_!!1027411018.jpg" style="max-width:750px" /></p>

# date-spm-anchor-id可以改变
<p data-spm-anchor-id="a2126o.11854294.0.i1.33b04831SR9py4"><img align="absmiddle" src="https://img.alicdn.com/imgextra/i4/1027411018/O1CN01s6vfXr1JOHh2VSbcl_!!1027411018.jpg" style="max-width:750px" /></p>

# 真实成功
<p><img align="absmiddle" src="https://img.alicdn.com/imgextra/i3/1027411018/O1CN010HM21c1JOHiF3uXmj_!!1027411018.jpg" style="max-width: 750.0px;" /><img align="absmiddle" src="https://img.alicdn.com/imgextra/i3/1027411018/O1CN01ga8yfL1JOHh2OHEGe_!!1027411018.jpg" style="max-width: 750.0px;" /></p>
"""

# 上货
# image_urls: [] 最大长度5, 主图
# cpv_memo: 备注
# freight_payer: 运费承担方式
# has_invoice
# express_fee 快递费
# 5次
session = '62007228409e52dcb526da35736274ZZf06f0b361e77f071027411018'

d = {'method': 'taobao.item.add', 'session': '6202826b52878389142fa67584aa6a8250ZZ7843a07c57c1027411018',
     'location.state': '北京', 'location.city': '北京', 'num': '154', 'price': '11.00', 'type': 'fixed',
     'stuff_status': 'new', 'title': 'shaowei', 'desc': '这是一个特别好的商品', 'cid': '50000671', 'approve_status': 'instock',
     'input_custom_cpv': '1627207:-2:悦色:美女;20509:-2:其他尺码;', 'input_str': '6931111111111', 'input_pids': '13021751',
     'props': '13328588:145656296;20021:28352;20603:3222243;1627207:28321;1627207:-2;20509:28314;20509:-2;',
     'sku_properties': '1627207:28321;20509:28314,1627207:28321;20509:-2,1627207:-2;20509:28314,1627207:-2;20509:-2',
     'cpv_memo': "1627207:28321:美女;1627207:-2:真黑",
     # "features":"sizeGroupType:women_bottoms;tags:25282,52290,50370,61890,104514;sizeGroupName:中国码;sizeGroupId:27013",
     "features": "sizeGroupType:men_tops;tags:36610,52290,50370,104514;sizeGroupName:中国码;sizeGroupId:27013",
     'sku_quantities': '22,33,44,55', 'sku_prices': '11.00,12.00,13.00,14.00', 'sku_barcode': ',,,',
     'sku_outer_ids': 'www ,www ,www ,www ', 'outer_id': '2000143', 'barcode': '9771671216014',
     'pic_path': 'https://img.alicdn.com/imgextra/i2/1027411018/O1CN01JIY1hc1JOHiIjWyRP_!!1027411018.jpg'}
# print(','.join(d.keys()))
# 男装，T恤，材质成分
d1 = {'method': 'taobao.item.add', 'session': '6202903e70fhj5fdc930628c2ce5aa84be6bf832adbb3c01027411018',
      'location.state': '北京', 'location.city': '北京', 'num': '22', 'price': '11.0', 'type': 'fixed',
      'stuff_status': 'new', 'title': '1111111', 'desc': 'sssss', 'cid': '50011123', 'approve_status': 'instock',
      'input_str': '11111,木棉80% 亚麻20%', 'input_pids': '13021751,149422948',
      "features": "sizeGroupName:中国码;",
      'props': '20663:3267194;122216345:29937;122216515:3302158;122216348:29445;122216507:3226292;42722636:248572013;122216586:3267162;20000:20578;1627207:28332;1627207:28341;20509:28316;',
      'sku_properties': '1627207:28332;20509:28316,1627207:28341;20509:28316', 'sku_quantities': '11,11',
      'sku_prices': '11.00,11.00', 'sku_barcode': ',', 'sku_outer_ids': ',', 'outer_id': '2000211'}

# 日本尺码
d = {'method': 'taobao.item.add', 'session': '6202903e70fhj5fdc930628c2ce5aa84be6bf832adbb3c01027411018',
     'location.state': '北京', 'location.city': '北京', 'num': '300', 'price': '11.0', 'type': 'fixed',
     'stuff_status': 'new', 'title': 'demo001', 'desc': 'sssss', 'cid': '50011123', 'approve_status': 'instock',
     'input_str': 'demo001', 'input_pids': '13021751',
     'props': '20663:29541;122216345:29937;122216515:3302158;122216608:101181;122216348:29446;122216507:3226292;20603:3222243;42718685:178914558;42722636:20213;20021:28352;20551:28343;124108695:20316299;122216589:81044;122216588:29957;122216586:4043538;6209522:41036269;8560225:10285019;20000:20578;1627207:28321;1627207:28332;1627207:28341;20509:28316;',
     'sku_properties': '1627207:28321;20509:28316,1627207:28332;20509:28316,1627207:28341;20509:28316',
     'sku_quantities': '100,100,100', 'sku_prices': '11.00,11.00,11.00', 'sku_barcode': ',,', 'sku_outer_ids': ',,',
     'features': 'sizeGroupName:中国码;', 'outer_id': '2000214'}

d3 = {'method': 'taobao.item.add', 'session': '6202903e70fhj5fdc930628c2ce5aa84be6bf832adbb3c01027411018',
      'location.state': '北京', 'location.city': '北京', 'num': '300', 'price': '11.0', 'type': 'fixed',
      'stuff_status': 'new', 'title': 'demo001', 'desc': 'sssss', 'cid': '50011123', 'approve_status': 'instock',
      'input_custom_cpv': '1627207:-1:1:;1627207:-2:2;1627207:-3:3;20509:-1:L;', 'input_str': 'demo001',
      'input_pids': '13021751',
      'props': '20663:29541;122216345:29937;122216515:3302158;122216608:101181;122216348:29446;122216507:3226292;20603:3222243;42718685:178914558;42722636:20213;20021:28352;20551:28343;124108695:20316299;122216589:81044;122216588:29957;122216586:4043538;6209522:41036269;8560225:10285019;20000:20578;1627207:-1;1627207:-2;1627207:-3;20509:-1;',
      'sku_properties': '1627207:-1;20509:-1,1627207:-2;20509:-1,1627207:-3;20509:-1', 'sku_quantities': '100,100,100',
      'sku_prices': '11.00,11.00,11.00', 'sku_barcode': ',,', 'sku_outer_ids': ',,',
      "features": "sizeGroupType:men_tops;tags:36610,52290,50370,104514;sizeGroupName:中国码;sizeGroupId:27013",
      'outer_id': '2000214',

      "wireless_desc": "<wapDesc><img>https://img.alicdn.com/imgextra/i4/1027411018/O1CN01FIONGV1JOHjQ1Gv9Z_!!1027411018.jpg</img><img>https://img.alicdn.com/imgextra/i2/1027411018/O1CN01rduaWT1JOHjQh2ZJU_!!1027411018.jpg</img><img>https://img.alicdn.com/imgextra/i4/1027411018/O1CN01WNjPsi1JOHjOAX0PA_!!1027411018.jpg</img></wapDesc>"
      }

product_one = {'method': 'taobao.item.add', 'session': '62007228409e52dcb526da35736274ZZf06f0b361e77f071027411018',
               'location.state': '北京', 'location.city': '北京', 'num': '444',
               'price': '333.00',
               'type': 'fixed',
               'stuff_status': 'new',
               'sub_stock': '1',
               'title': '111', 'desc': '此处需要详情页', 'cid': '162201',
               'approve_status': 'instock', 'has_invoice': 'false', 'has_warranty': 'false', 'sell_promise': 'false',
               'input_custom_cpv': '1627207:-1:浅灰色;20509:-1:S;20509:-2:M;',
               'input_str': '111,demo',
               'input_pids': '13021751,20000',
               'props': '20017:494072160;122276111:30465;20677:29954;13328588:492838735;122216507:3226292;122216347:828914351;20608:20213;20021:3267653;20551:28398;34272:7642045;122216588:130845;122276315:3925131;1627207:-1;20509:-1;20509:-2;',
               'sku_properties': '1627207:-1;20509:-1,1627207:-1;20509:-2',
               'sku_quantities': '222,222',
               'sku_prices': '333.00,333.00',
               'sku_barcode': ',',
               'sku_outer_ids': ',',
               'cpv_memo': '1627207:-1:;',
               'features': 'sizeGroupType:women_bottoms;tags:52290,50370,104514;sizeGroupName:中国码;sizeGroupId:27013'}
product_one1 = {'method': 'taobao.item.add', 'session': '62007228409e52dcb526da35736274ZZf06f0b361e77f071027411018',
                'location.state': '北京', 'location.city': '北京', 'num': '444', 'price': '333.00', 'type': 'fixed',
                'stuff_status': 'new', 'sub_stock': '1', 'title': '111', 'desc': '此处需要详情页', 'cid': '162201',
                'approve_status': 'instock', 'has_invoice': 'false', 'has_warranty': 'false', 'sell_promise': 'false',
                'input_custom_cpv': '1627207:-1:乳白色;20509:-1:S;20509:-2:M;', 'input_str': '111,other/其他',
                'input_pids': '13021751,20000',
                'props': '20017:494072160;122276111:30465;20677:29954;13328588:492838735;122216507:3226292;122216347:828914351;20608:20213;20021:3267653;20551:28398;34272:7642045;122216588:130845;122276315:3925131;1627207:-1;20509:-1;20509:-2;',
                'sku_properties': '1627207:-1;20509:-1,1627207:-1;20509:-2', 'sku_quantities': '222,222',
                'sku_prices': '333.00,333.00', 'sku_barcode': ',', 'sku_outer_ids': ',',
                'cpv_memo': '1627207:-1:222;',
                'features': 'sizeGroupType:women_bottoms;tags:25282,52290,50370,61890,104514;sizeGroupName:中国码;sizeGroupId:27013'}

product_one = {'method': 'taobao.item.add',
               'session': '62007228409e52dcb526da35736274ZZf06f0b361e77f071027411018',
               'location.state': '北京',
               'location.city': '北京',
               'num': '11111',
               'price': '11111.00',
               'type': 'fixed',
               'stuff_status': 'new',
               'sub_stock': '1',
               'title': '11- 休闲裤',
               'desc': '此处需要详情页',
               'cid': '162104',
               'approve_status': 'instock',
               'has_invoice': 'false',
               'has_warranty': 'false',
               'sell_promise': 'false',
               # 'input_custom_cpv': '1627207:-1:乳白色;20509:-1:M;',
               'input_str': '11111,other/其他',
               'input_pids': '13021751,20000',
               'props': '20663:57658638;20017:494072162;2917380:7216758;122216562:44597;122216348:3216779;31611:20754689;13328588:492838735;122216507:29430173;122216347:728066917;20603:14031880;10142888:3386071;20608:29921;20021:112399;20551:112997;122216588:115777;122216588:115772;122216588:7573005;122216588:148585996;122216588:27436000;122216586:27295811;1627207:28332;20509:28314;',
               'sku_properties': '1627207:28332;20509:28314',
               'sku_quantities': '11111',
               'sku_prices': '11111.00',
               # 'cpv_memo': '1627207:-1:;',
               'features': 'sizeGroupType:women_bottoms;tags:25282,52290,50370,61890,104514;sizeGroupName:中国码;sizeGroupId:27013'}

product_one_three = {'method': 'taobao.item.add',
                     'session': '62007228409e52dcb526da35736274ZZf06f0b361e77f071027411018',
                     'location.state': '北京',
                     'location.city': '北京',
                     'num': '11',
                     'price': '111.00',
                     'type': 'fixed',
                     'stuff_status': 'new',
                     'sub_stock': '1',
                     'title': '11- 休闲裤',
                     'desc': '此处需要详情页',
                     'cid': '162205',
                     'approve_status': 'instock',
                     'has_invoice': 'false',
                     'has_warranty': 'false',
                     'sell_promise': 'false',
                     'input_custom_cpv': '1627207:28341:黑色;20509:28314:S;',
                     'input_str': '11- 休闲裤,other/其他',
                     'input_pids': '13021751,20000',
                     'props': '20017:494072162;122276111:72202018;20677:29952;13328588:492838731;122216507:103133;122216347:728146012;20608:29934;18073248:3325552;20021:105255;20551:28399;34272:7642045;122216588:130138;122276315:29947;1627207:28341;20509:28314;',
                     'sku_properties': '1627207:28341;20509:28314',
                     'sku_quantities': '11',
                     'sku_prices': '111.00',
                     'cpv_memo': '1627207:28341:;',
                     # 2000495, 1004682, 1004683
                     # sizeGroupType:women_bottoms;tags:52290,50370,104514;sizeGroupName:中国码;sizeGroupId:27013
                     #            sizeGroupType:women_bottoms;tags:52290,50370,104514;sizeGroupName:中国码;sizeGroupId:27013
                     'features': 'sizeGroupType:women_bottoms;tags:52290,50370,104514;sizeGroupName:中国码;sizeGroupId:27013'}
# print(topapi(product_one_three))

product = {"method": 'taobao.product.get ', "session": '6202903e70fhj5fdc930628c2ce5aa84be6bf832adbb3c01027411018',
           "fields": "product_id,outer_id",
           "product_id": "596627622518",
           "cid": "50000436",
           }

product_all = {"method": 'taobao.items.onsale.get ',
               "session": '6202903e70fhj5fdc930628c2ce5aa84be6bf832adbb3c01027411018',
               "fields": "method,session,location.state,location.city,num,price,type,stuff_status,title,desc,cid,approve_status,input_custom_cpv,input_str,input_pids,props,sku_properties,cpv_memo,sku_quantities,sku_prices,sku_barcode,sku_outer_ids,outer_id,barcode,pic_path",
               "num_iids": "596627622518",
               }

#
product_one = {'method': 'taobao.item.seller.get ',
               'session': '6202624c3d828cbae09b803082d49019ZZf023e0ab5b2a91027411018', 'fields': 'props',
               'num_iid': '597526648210'}
session = '6202624c3d828cbae09b803082d49019ZZf023e0ab5b2a91027411018'
brand = {'method': 'taobao.itemcats.authorize.get ',
         'session': session, 'fields': """brand.vid, brand.name, item_cat.cid, item_cat.name, item_cat.status,item_cat.sort_order,item_cat.parent_cid,item_cat.is_parent,xinpin_item_cat.cid, 


xinpin_item_cat.name, 
xinpin_item_cat.status,
xinpin_item_cat.sort_order,
xinpin_item_cat.parent_cid,
xinpin_item_cat.is_parent"""}
category_brand = {'method': 'taobao.itempropvalues.get ',
                  'session': session,
                  'fields': 'cid,pid,prop_name,vid,name,name_alias,status,sort_order',
                  'cid': "1624"}

# print(topapi(category_brand).decode())

taobao_add_info = {

    'method': "taobao.item.add.schema.get", 'session': session,
    "category_id": "50000436",
}


# 添加图片
def taobao_sku_pic_upload(postparm):
    postparm['method'] = 'taobao.item.propimg.upload'

    filenames = postparm.pop('image', '')
    resps = []

    for filename in filenames:
        bbbb = BytesIO(requests.get(filename).content)
        files = [
            ('image', ('a.jpg', bbbb, 'Content-Type: image/jpg')),
        ]
        resp = json.loads(topapi(postparm, files).decode('utf-8'))
        resps.append(resp)
    return resps


# 添加图片
def taobao_sku_pic_upload_list(postparm):
    """
    https://cdn1.ecpro.com/uploads/10016/2000226/d640c8dc448a5a3bf0d4e7f47546bee0.jpg?sign=2d4f77d8e5bc62bb40580ed3541b2fc8&t=1560572150
{'session': '6201522d00610558c208c72c70b2f8ZZ4c7789f78d7b62e1027411018', 'num_iid': '596878867676', 'method': 'taobao.item.propimg.upload', 'properties': '1627207:4464174'}
    :param postparm:
    :return:
    """
    postparm['method'] = 'taobao.item.propimg.upload'

    image_links = postparm.pop('image', '')
    properties = postparm.pop('properties', '')
    assert len(image_links) == len(properties)
    resps = []

    for i, link in enumerate(image_links):
        postparm["properties"] = properties[i]
        bbbb = BytesIO(requests.get(link).content)
        files = [
            ('image', ('a.jpg', bbbb, 'Content-Type: image/jpg')),
        ]
        resp = json.loads(topapi(postparm, files).decode('utf-8'))
        resps.append(resp)
    return resps


pic_relate = ['i1/1027411018/O1CN01oOQxZT1JOHjOD2snu_!!1027411018.jpg']

joint_pic = {

    'session': session,
    "properties": "1627207:-1",
    "num_iid": "596871251147",
    "pic_paths": pic_relate,
}


def taobao_joint_sku_pic(postparm):
    postparm['method'] = 'taobao.item.joint.propimg'

    filenames = postparm.pop('pic_paths', '')

    resps = []
    for i in filenames:
        postparm["pic_path"] = i
        resps.append(json.loads(topapi(postparm).decode()))

    return resps


# link = './1.jpg'
add_sku_pic = {

    'session': session,
    "properties": "1627207:4464174",  # 4654410370, 3234441, 269534635
    "num_iid": "596795886233",
    "image": link[:1],
}
add_sku_pic = {'session': '6201f13dce5c2c9ae3ba6ZZ6e0382b6262fb2336afc7d2b1027411018',
               'properties': ['1627207:3232478', '1627207:28332'], 'num_iid': '597106567538', 'image': [
        'https://cdn1.ecpro.com/uploads/10016/2000239/20d3962a6bf5faa2c1266694525b2253.jpg?sign=3abd6ce70a27c2434be4094000b77080&t=1560596011']}


# TODO
# print(taobao_sku_pic_upload_list(add_sku_pic))


# print(taobao_sku_pic_upload(add_sku_pic))


def taobao_item_propimg_upload(postparm):
    postparm['method'] = 'taobao.item.propimg.upload'
    files = {'image': open(postparm.pop('image', ''), 'rb')}

    resp = json.loads(topapi(postparm, files).decode('utf-8'))
    return resp


# get all sku
sku = {'method': 'taobao.item.skus.get', 'session': session,
       "fields": "sku_id,iid,properties,quantity,price,outer_id,created,modified,status",
       "num_iids": "596878867676",
       }

# print(taobao_item_propimg_upload(add_sku_pic))
# print(taobao_sku_pic_upload(add_sku_pic))
# print(taobao_joint_sku_pic(joint_pic))
# [{'item_propimg_upload_response': {'prop_img': {'created': '2019-06-13 15:27:26', 'id': 0, 'url': 'https://img.alicdn.com/bao/uploaded/i1/1027411018/O1CN01oOQxZT1JOHjOD2snu_!!1027411018.jpg'}, 'request_id': 'dzqy47clj7y2'}}, {'item_propimg_upload_response': {'prop_img': {'created': '2019-06-13 15:27:27', 'id': 0, 'url': 'https://img.alicdn.com/bao/uploaded/i2/1027411018/O1CN01lpLh461JOHjT0q9q9_!!1027411018.jpg'}, 'request_id': '8baeqdoebssb'}}]

# TODO

d3 = {
    "method": "taobao.item.add",
    "session": "620010485de9ZZb846410fac21671b272ec1886820470801027411018",
    "location.state": "北京",
    "location.city": "北京",
    "num": "330",
    "price": "12.0",
    "type": "fixed",
    "stuff_status": "new",
    "title": "呵呵",
    "desc": '<p><img align="absmiddle" src="https://img.alicdn.com/imgextra/i3/1027411018/O1CN01UZftQz1JOHjVsyrDV_!!1027411018.jpg" style="max-width:750px" /></p><p><img align="absmiddle" src="https://img.alicdn.com/imgextra/i4/1027411018/O1CN01Z22Nf41JOHjYi5CXG_!!1027411018.jpg" style="max-width:750px" /></p><p><img align="absmiddle" src="https://img.alicdn.com/imgextra/i3/1027411018/O1CN01MKTkhH1JOHjVxSo7E_!!1027411018.jpg" style="max-width:750px" /></p><p><img align="absmiddle" src="https://img.alicdn.com/imgextra/i1/1027411018/O1CN010pSWkS1JOHjVGl5Ut_!!1027411018.jpg" style="max-width:750px" /></p><p><img align="absmiddle" src="https://img.alicdn.com/imgextra/i4/1027411018/O1CN01feFyjF1JOHjXoGDNa_!!1027411018.jpg" style="max-width:750px" /></p><p><img align="absmiddle" src="https://img.alicdn.com/imgextra/i4/1027411018/O1CN01K6Ta9X1JOHjVswqUx_!!1027411018.jpg" style="max-width:750px" /></p><p><img align="absmiddle" src="https://img.alicdn.com/imgextra/i1/1027411018/O1CN01LqXKRU1JOHjUJLxAY_!!1027411018.jpg" style="max-width:750px" /></p><p><img align="absmiddle" src="https://img.alicdn.com/imgextra/i1/1027411018/O1CN01Y1auWW1JOHjZBhnge_!!1027411018.jpg" style="max-width:750px" /></p><p><img align="absmiddle" src="https://img.alicdn.com/imgextra/i4/1027411018/O1CN01nq2yWS1JOHjYW4CeG_!!1027411018.jpg" style="max-width:750px" /></p><p><img align="absmiddle" src="https://img.alicdn.com/imgextra/i4/1027411018/O1CN01OnA1h01JOHjOTVJUS_!!1027411018.jpg" style="max-width:750px" /></p><p><img align="absmiddle" src="https://img.alicdn.com/imgextra/i1/1027411018/O1CN01t0QKqQ1JOHjX7uVmW_!!1027411018.jpg" style="max-width:750px" /></p><p><img align="absmiddle" src="https://img.alicdn.com/imgextra/i2/1027411018/O1CN01XFQTvG1JOHjX8ZjrI_!!1027411018.jpg" style="max-width:750px" /></p><p><img align="absmiddle" src="https://img.alicdn.com/imgextra/i4/1027411018/O1CN01HKEk3W1JOHjT1iTv0_!!1027411018.jpg" style="max-width:750px" /></p><p><img align="absmiddle" src="https://img.alicdn.com/imgextra/i4/1027411018/O1CN01oJtrt71JOHjVGnpyK_!!1027411018.jpg" style="max-width:750px" /></p><p><img align="absmiddle" src="https://img.alicdn.com/imgextra/i3/1027411018/O1CN01uASr8c1JOHjYi89Vp_!!1027411018.jpg" style="max-width:750px" /></p><p><img align="absmiddle" src="https://img.alicdn.com/imgextra/i1/1027411018/O1CN01mG4GbP1JOHjX8abyC_!!1027411018.jpg" style="max-width:750px" /></p><p><img align="absmiddle" src="https://img.alicdn.com/imgextra/i2/1027411018/O1CN01mWE78f1JOHjVxTPZi_!!1027411018.jpg" style="max-width:750px" /></p><p><img align="absmiddle" src="https://img.alicdn.com/imgextra/i3/1027411018/O1CN01hyMIJA1JOHjYi7kZm_!!1027411018.jpg" style="max-width:750px" /></p><p><img align="absmiddle" src="https://img.alicdn.com/imgextra/i3/1027411018/O1CN0170x6NW1JOHjVxUDTq_!!1027411018.jpg" style="max-width:750px" /></p><p><img align="absmiddle" src="https://img.alicdn.com/imgextra/i4/1027411018/O1CN01QCrGvI1JOHjW0V7cO_!!1027411018.jpg" style="max-width:750px" /></p><p><img align="absmiddle" src="https://img.alicdn.com/imgextra/i1/1027411018/O1CN01B6PIqD1JOHjYW4o78_!!1027411018.jpg" style="max-width:750px" /></p><p><img align="absmiddle" src="https://img.alicdn.com/imgextra/i1/1027411018/O1CN01HaLRra1JOHjYW3GV9_!!1027411018.jpg" style="max-width:750px" /></p>',
    "cid": "50000671",
    "approve_status": "instock",
    "has_invoice": "false",
    "has_warranty": "false",
    "sell_promise": "false",
    "input_custom_cpv": "1627207:-1:柠檬黄;1627207:-2:白色;1627207:-3:深蓝色;1627207:-4:荧光绿;1627207:-5:金色;20509:-1:XXS;20509:-2:L;20509:-3:XL;",
    "input_str": "3434,fa",
    "input_pids": "13021751,20000",
    "props": "20608:29934;18073248:29931;122216347:854168429;20017:494072158;13328588:492838734;20603:107622;20021:3267653;1627207:-1;1627207:-2;1627207:-3;1627207:-4;1627207:-5;20509:-1;20509:-2;20509:-3;",
    "sku_properties": "1627207:-1;20509:-1,1627207:-1;20509:-2,1627207:-1;20509:-3,1627207:-2;20509:-1,1627207:-2;20509:-2,1627207:-2;20509:-3,1627207:-3;20509:-1,1627207:-3;20509:-2,1627207:-3;20509:-3,1627207:-4;20509:-1,1627207:-4;20509:-2,1627207:-4;20509:-3,1627207:-5;20509:-1,1627207:-5;20509:-2,1627207:-5;20509:-3",
    "sku_quantities": "22,22,22,22,22,22,22,22,22,22,22,22,22,22,22",
    "sku_prices": "12.00,12.00,12.00,12.00,12.00,12.00,12.00,12.00,12.00,12.00,12.00,12.00,12.00,12.00,12.00",
    "sku_barcode": ",,,,,,,,,,,,,,",
    "sku_outer_ids": ",,,,,,,,,,,,,,",
    "cpv_memo": "1627207:-1:浅灰色备注;1627207:-2:白色备注;1627207:-3:深蓝色备注;1627207:-4:;1627207:-5:111;",
    "features": "sizeGroupType:women_bottoms;tags:25282,52290,50370,61890,104514;sizeGroupName:中国码;sizeGroupId:27013",
    "outer_id": "2000257"
}


# print(str(topapi(d3).decode()))


# props = "20021:105255;20509:28313;1627207:28332;1627207:28341;13328588:145656297"
# taobao_sku_vids = list(filter(lambda sku_pvid: sku_pvid.startswith(("1627207",)), props.split(";")))
# print(taobao_sku_vids)

# print(topapi(sku).decode())

# 上传主图
def taobao_item_img_upload(postparm):
    postparm['method'] = 'taobao.item.img.upload'

    filenames = postparm.pop('image', '')
    resps = []

    for filename in filenames:
        bbbb = BytesIO(requests.get(filename).content)
        files = [
            ('image', ('a.jpg', bbbb, 'Content-Type: image/jpg')),
        ]
        resp = json.loads(topapi(postparm, files).decode('utf-8'))
        resps.append(resp)
    return resps


num_iid = '596916342844'
vertical__map_pictures = [
    'https://cdn1.ecpro.com/uploads/10016/2000239/f2870cf9742a8ec0fe00b930dbb7ed9f.jpg?sign=fd4295f4d4a6a6df599a6ae4e09c9554&t=1560767360', ]

item_vertical_pics = {'session': '620201853d4af3991591f95293ZZ040e397783779263eb91027411018', 'num_iid': '598071391944',
                      'image': [
                          'https://img.alicdn.com/imgextra/i3/1027411018/O1CN01ynRBg21JOHjPfgWNd_!!1027411018.jpg'],
                      # 'is_rectangle': 'true'
                      "position": "4",
                      # "is_major": "false"
                      }


# item_vertical_pics_resp = taobao_item_img_upload(item_vertical_pics)
#
# print("item_vertical_pics_resp", item_vertical_pics_resp)


# 添加图片
def taobao_item_pic_upload(postparm):
    postparm['method'] = 'taobao.picture.upload'

    filenames = postparm.pop('image', '')
    resps = []
    picture_paths = []

    for filename in filenames:
        bbbb = BytesIO(requests.get(filename).content)
        files = [
            ('img', ('a.jpg', bbbb, 'Content-Type: image/jpg')),
        ]
        resp = json.loads(topapi(postparm, files).decode('utf-8'))
        picture_paths.append(resp.get("picture_upload_response").get("picture").get("picture_path").lstrip(
            "https://img.alicdn.com/imgextra/"))
        resps.append(resp)
    return picture_paths


# print(taobao_item_pic_upload(pic))


def get_all_features(filename, product_one):
    s = topapi(product_one).decode()
    resp = json.loads(s)
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(resp)

    if resp.get("item_seller_get_response"):
        item = resp.get("item_seller_get_response").get("item")
        if isinstance(item, dict):
            features = item.get("features")
            cid = item.get("cid")
            result[cid] = features

            with open('./schema/' + str(filename) + '.json', 'w') as outfile:
                json.dump(resp, outfile, indent=4)


def read_csv():
    product_one = {"method": 'taobao.item.seller.get',
                   "session": session,
                   "fields": "verticalImage,sku_spec_ids,sku_delivery_times,sku_hd_length,sku_hd_height,sku_hd_lamp_quantity,input_str,input_pids,sku_properties,sku_quantities,sku_prices,sku_outer_ids,sku_barcode,delivery_time.need_delivery_time,delivery_time.delivery_time_type,delivery_time.delivery_time,ms_payment.reference_price,ms_payment.voucher_price,ms_payment.price,locality_life.obs,locality_life.version,locality_life.packageid,food_security.prd_license_no,food_security.design_code,food_security.factory,food_security.factory_site,food_security.contact,food_security.mix,food_security.plan_storage,food_security.period,food_security.food_additive,food_security.supplier,food_security.product_date_start,food_security.product_date_end,food_security.stock_date_start,food_security.stock_date_end,food_security.health_product_no,location.state,location.city,num,price,type,stuff_status,title,desc,approve_status,cid,props,freight_payer,valid_thru,has_invoice,has_warranty,has_showcase,seller_cids,has_discount,post_fee,express_fee,ems_fee,list_time,increment,image,,postage_id,auction_point,property_alias,lang,outer_id,product_id,pic_path,auto_fill,is_taobao,is_ex,is_3D,sell_promise,cod_postage_id,is_lightning_consignment,weight,is_xinpin,sub_stock,scenic_ticket_pay_way,scenic_ticket_book_cost,item_size,item_weight,sell_point,barcode,newprepay,qualification,o2o_bind_service,features,ignorewarning,after_sale_id,change_prop,desc_modules,is_offline,wireless_desc,spu_confirm,video_id,interactive_id,lease_extends_info,brokerage,biz_code,image_urls,locality_life.choose_logis,locality_life.expirydate,locality_life.network_id,locality_life.merchant,locality_life.verification,locality_life.refund_ratio,locality_life.onsale_auto_refund_ratio,locality_life.refundmafee,locality_life.eticket,paimai_info.mode,paimai_info.deposit,paimai_info.interval,paimai_info.reserve,paimai_info.valid_hour,paimai_info.valid_minute,global_stock_type,global_stock_country,support_custom_made,custom_made_type_id,global_stock_delivery_place,global_stock_tax_free_promise,input_custom_cpv,cpv_memo,",
                   "num_iid": "599003875427",
                   }
    result = dict()

    with open('./product_link.csv', 'r') as f:
        line = f.readline()
        while line:
            if line.startswith("https://item.taobao.com/item.htm?ft=t&id="):
                num_iid = line.strip().strip("https://item.taobao.com/item.htm?ft=t&id=")
                product_one["num_iid"] = num_iid

                get_all_features(num_iid, product_one)

            line = f.readline()

    with open("1.json", 'w') as f:
        json.dump(result, f, indent=4)


if __name__ == '__main__':
    num_iid = 599003875427
    product_one = {"method": 'taobao.item.seller.get',
                   "session": session,
                   "fields": "verticalImage,sku_spec_ids,sku_delivery_times,sku_hd_length,sku_hd_height,sku_hd_lamp_quantity,input_str,input_pids,sku_properties,sku_quantities,sku_prices,sku_outer_ids,sku_barcode,delivery_time.need_delivery_time,delivery_time.delivery_time_type,delivery_time.delivery_time,ms_payment.reference_price,ms_payment.voucher_price,ms_payment.price,locality_life.obs,locality_life.version,locality_life.packageid,food_security.prd_license_no,food_security.design_code,food_security.factory,food_security.factory_site,food_security.contact,food_security.mix,food_security.plan_storage,food_security.period,food_security.food_additive,food_security.supplier,food_security.product_date_start,food_security.product_date_end,food_security.stock_date_start,food_security.stock_date_end,food_security.health_product_no,location.state,location.city,num,price,type,stuff_status,title,desc,approve_status,cid,props,freight_payer,valid_thru,has_invoice,has_warranty,has_showcase,seller_cids,has_discount,post_fee,express_fee,ems_fee,list_time,increment,image,,postage_id,auction_point,property_alias,lang,outer_id,product_id,pic_path,auto_fill,is_taobao,is_ex,is_3D,sell_promise,cod_postage_id,is_lightning_consignment,weight,is_xinpin,sub_stock,scenic_ticket_pay_way,scenic_ticket_book_cost,item_size,item_weight,sell_point,barcode,newprepay,qualification,o2o_bind_service,features,ignorewarning,after_sale_id,change_prop,desc_modules,is_offline,wireless_desc,spu_confirm,video_id,interactive_id,lease_extends_info,brokerage,biz_code,image_urls,locality_life.choose_logis,locality_life.expirydate,locality_life.network_id,locality_life.merchant,locality_life.verification,locality_life.refund_ratio,locality_life.onsale_auto_refund_ratio,locality_life.refundmafee,locality_life.eticket,paimai_info.mode,paimai_info.deposit,paimai_info.interval,paimai_info.reserve,paimai_info.valid_hour,paimai_info.valid_minute,global_stock_type,global_stock_country,support_custom_made,custom_made_type_id,global_stock_delivery_place,global_stock_tax_free_promise,input_custom_cpv,cpv_memo,",
                   "num_iid": str(num_iid),
                   }
    result = dict()
    get_all_features(filename=num_iid, product_one=product_one)
