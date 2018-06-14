import requests
import time
import random
import os

DOWNLOAD_URL = 'http://i3.3conline.com/images/piclib/201105/17/batch/1/94936/1305647832498diu95xjkj0.jpg'

save_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'files')
save_file = "".join([time.strftime("%Y%m%d%H%M%S"), str(random.randint(0, 100)), '.jpg'])
download_filename = DOWNLOAD_URL.split('/')[-1]

new_file = os.path.join(save_path, download_filename)

print(requests.head(url=DOWNLOAD_URL).headers['Content-Length'])

#
# headers = {
#     'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36',
#     'Range': 'bytes=0-13000'
# }


headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36',
    'Range': 'bytes=13001-528435'
}

response = requests.get(url=DOWNLOAD_URL, headers=headers)

print(response.request)
print(new_file)
#
# tempf = open(new_file, 'w')
# tempf.close()

with open(new_file, 'rb+') as f:
    print(f.tell())
    print(response.content)
    f.seek(13000)
    f.write(response.content)
