# coding=utf-8

import datetime
import hashlib
import re
import os
from qcloud_cos import CosConfig
from qcloud_cos import CosS3Client

# 腾讯对象存储参数
secret_id = os.getenv('secret_id', None)
secret_key = os.getenv('secret_key', None)
region = 'ap-beijing'
token = None  # 使用临时密钥需要传入 Token，默认为空，可不填
scheme = 'https'
bucket = 'ecpro-draw-upload-1258059231'

config = CosConfig(Region=region, SecretId=secret_id, SecretKey=secret_key, Token=token, Scheme=scheme)
client = CosS3Client(config)


def upload_cos(key, bs):
    resp = client.put_object(
        Bucket=bucket,
        Body=bs,
        Key=key,
        EnableMD5=False
    )
    return resp


def upload_cos_without_sign(key, bs):
    resp = client.put_object(
        Bucket="ecpro-upload-public-1258059231",
        Body=bs,
        Key=key,
        EnableMD5=False
    )
    return resp


import hashlib
import json
import os
from io import BytesIO, StringIO
from zipfile import ZipFile
from PIL import Image
import PIL

MAX_SINGLE_PICTURE_SIZE = 3 * 1024 * 1024
MAX_SINGLE_PICTURE_WIDTH = 6000
MIN_SINGLE_PICTURE_WIDTH = 100


def extract_zip(input_zip):
    fd = open(input_zip)
    zip_data = fd.read()
    fio = StringIO(zip_data)

    file_contents = []
    error_dict = {1: "单张大于4M: ", 2: "单张宽度超出范围[{}, {}]: ".format(MIN_SINGLE_PICTURE_WIDTH, MAX_SINGLE_PICTURE_WIDTH)}
    error_message = []

    input_zip = ZipFile(file=fio)
    for name in input_zip.namelist():
        file = input_zip.read(name)
        image_file = Image.open(BytesIO(file))
        width, height = image_file.size
        file_length, image_name, file_content = (len(file), input_zip.filename + name, file)

        if file_length > MAX_SINGLE_PICTURE_SIZE:
            error_message.append(error_dict[1] + image_name)
        if width <= MIN_SINGLE_PICTURE_WIDTH or width >= MAX_SINGLE_PICTURE_SIZE:
            error_message.append(error_dict[2] + image_name)
        if file_content not in file_contents:
            file_contents.append(file_content)

    if error_message != []:
        return error_message
    user_id = '111'
    product_id = '111'
    storage_keys = []
    for file_content in file_contents:
        file_ext = '.jpg'

        md5_hash = hashlib.md5(file_content).hexdigest()
        storage_key = '{}/{}/{}/{}{}'.format('uploads', user_id, product_id, md5_hash, file_ext)

        resp = upload_cos_without_sign(md5_hash, bs=file_content)
        if resp.get('ETag') is not None:
            # result['code'] = 300
            # result['message'] = '上传失败'
            # return jsonify(result)
            pass
            print(1)
        else:
            storage_keys.append('https://cdn1.ecpro1.com/resources/{}'.format(storage_key))
    return storage_keys
    # return {name: input_zip.read(name) for name in input_zip.namelist()}


print(extract_zip('test.zip'))
