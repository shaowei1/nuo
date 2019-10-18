# width, height = 500, 500
import base64
from io import BytesIO

import PIL

import PIL.Image

body = {"transform": {"scale": 1, "rotate": 0, "quality": 1, "crop": [204, 181, 335, 335]}, "image_id": 1005638}

transform = body.get("transform")
scale = transform.get("scale")
crop = transform.get("crop")
rotate = transform.get("rotate")
quality = int(transform.get("quality") * 100)

x1, y1, width, height = crop

_im = BytesIO(open('1.jpg', 'rb').read())
im = PIL.Image.open(_im)
old_w, old_h = im.size
_format = im.format
print(str(len(im.fp.read())))

im = im.resize((int(old_w * scale), int(old_h * scale)))

res_im = im.crop((x1, y1, x1 + width, y1 + height))
file_path = './tes.png'
# res_im.save('./tes.png')
#

# with open('base64.txt', 'wb') as f:
#     f.write()
# file_size = str(len(res_im.fp.read()))
imgByteArr = BytesIO()
print(rotate)
print(quality)
res_im.rotate(rotate).save(imgByteArr, format=_format, quality=quality)
imgByteArr = imgByteArr.getvalue()
res_im.save(file_path)
with open('a.jpg', 'wb') as f:
    f.write(imgByteArr)
ret = '{}'.format(base64.b64encode(imgByteArr).decode('ascii'))
print(ret)
file_size = len(imgByteArr)
