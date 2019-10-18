# import requests
#
# url = 'https://api.ecpro.com/storage/upload_tasks'
#
# headers = {"Authorization": "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJoNUl0SGU3UGJUbmk2dzQ1emU3VWZpYzhocXVXajhRaSIsInVzZXJfaWQiOjEwMDE2LCJ1c2VyX3JvbGVzIjpbInJvb3QiXSwidXNlcl9zdGF0dXMiOiJlbmFibGVkIn0.5EPP6qqA81gapdVZDKikkoGZLYI4tn4Ea2rGg3dqW7I"}
# payload = {"upload_type": "package", "filename": "shaowei.zip", "size": 6485636}
# response = requests.post(url=url, json=payload, headers=headers)
# print(response)
# print(response.content)
import requests
from zipfile import ZipFile
import io

file_path = 'http://ecpro-upload-public-1258059231.cos.ap-beijing.myqcloud.com/tmp/aa714d14-1047-4860-b45d-95b97dc95c91.zip'
input_zip = io.BytesIO(requests.get(file_path).content)
x = ZipFile(input_zip)
print(x)
