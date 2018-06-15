import threading
import time
import requests


class MulThreadDownload(threading.Thread):
    def __init__(self, url, startpos, endpos, f):
        super(MulThreadDownload, self).__init__()

        self.url = url
        self.startpos = startpos
        self.endpos = endpos
        self.fd = f

    def download(self):
        print('start thread: {} at {}'.format(self.getName(), time.time()))
        headers = {
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36',
            "Range": "bytes={}-{}".format(self.startpos, self.endpos)
        }
        print(headers)
        print(self.startpos)
        print('-----------------------')

        response = requests.get(self.url, headers=headers)
        self.fd.seek(self.startpos)
        self.fd.write(response.content)

        print('stop thread: {} at {}'.format(self.getName(), time.time()))

    def run(self):
        self.download()
