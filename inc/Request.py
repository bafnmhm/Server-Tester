import http.client
import urllib.parse


class Request:
    content = ''
    status = ''
    reason = ''
    host = '172.20.204.65:81'
    headers = {'Content-type': 'application/x-www-form-urlencoded',
               'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
               'Upgrade-Insecure-Requests': '1',
               'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko)',
               }

    def httpSend(self, url, post=None):
        print(url, post)
        coon = http.client.HTTPConnection(self.host)
        if post:
            params = urllib.parse.urlencode(post)
            coon.request('POST', url, params, headers=self.headers)
        else:
            coon.request('GET', url, headers=self.headers)
        response = coon.getresponse()
        self.status = response.status
        self.reason = response.reason
        self.content = response.read()
        print(self.content)
        coon.close()

    def isConnectSuccess(self):
        return self.status == 200

    def getContent(self):
        return self.content
