import requests
import os, sys
import time
import random
import threading
import ssl

from MulThreadDownload import MulThreadDownload

ssl._create_default_https_context = ssl._create_unverified_context

print(time.strftime("%Y-%m-%d %H:%M:%S"))

# 需要下载的文件
DOWNLOAD_URL = 'http://zealervideo-1254235226.file.myqcloud.com/ZEALER-MEDIA/VIVO%20NEX/vivo%20NEX%E4%B8%8A%E6%89%8B0612_x264.mp4.f40.mp4'

# 保存文件的路径
save_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'files')
# 保存文件的文件名
save_file = "".join([time.strftime("%Y%m%d%H%M%S"), str(random.randint(0, 100)), '.', DOWNLOAD_URL.split('.')[-1]])

# 获取下载文件的文件名和文件大小
download_filename = DOWNLOAD_URL.split('/')[-1]

new_file = os.path.join(save_path, download_filename)

download_file_size = int(requests.head(DOWNLOAD_URL, headers={
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'
}).headers['Content-Length'])

print('download filename: {}'.format(download_filename))
print('download filename: {}'.format(download_file_size))
print('save filename: {}'.format(save_file))

# 线程数
thread_num = 3
# 信号量, 同时只允许3个线程
threading.BoundedSemaphore(thread_num)

mtd_list = []
start = 0
end = -1
step = download_file_size // thread_num

# 生成空文件
tmpf = open(new_file, 'w')
tmpf.close()

# rb+, 二进制打开文件, 可任意读写
with open(new_file, 'rb+') as f:
    fileno = f.fileno()
    # print(fileno)

    # 如果大小为11字节, 那就是获取文件0-10的位置的数据
    # 如果 end = 10, 说明文件读取完成

    while end < download_file_size - 1:
        start = end + 1
        end = start + step - 1

        if end > download_file_size:
            end = download_file_size

        # print("start: {}, end: {}".format(start, end))

        # 复制文件句柄
        dup = os.dup(fileno)
        fd = os.fdopen(dup, 'rb+', -1)

        t = MulThreadDownload(DOWNLOAD_URL, start, end, fd)
        t.start()

        mtd_list.append(t)

    for i in mtd_list:
        i.join()

print(time.strftime("%Y-%m-%d %H:%M:%S"))

# 2018-06-15 00:03:07
# 2018-06-15 00:03:54
# 47

# 2018-06-15 00:04:31
# 2018-06-15 00:05:18
# 48


# 31 35
# 30

# 15:30 16:29
#
