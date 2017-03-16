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
    error = ''

    def httpSend(self, req):
        if not self.checkReq(req):
            return False

        url = req['url']
        post = 'post' in req and req['post'] or ''

        coon = http.client.HTTPConnection(self.host)
        if post:
            post = self.parsePost(post)
            params = urllib.parse.urlencode(post)
            coon.request('POST', url, params, headers=self.headers)
        else:
            coon.request('GET', url, headers=self.headers)
        response = coon.getresponse()
        self.status = response.status
        self.reason = response.reason
        self.content = response.read()
        coon.close()

    def isConnectSuccess(self):
        return self.status == 200

    def getContent(self):
        return self.content

    def checkReq(self, req):
        if 'url' not in req:
            self.error = '请求url错误'
            return False
        else:
            return True

    def reset(self):
        self.content = ''
        self.status = ''
        self.reason = ''
        self.error = ''

    @staticmethod
    def parsePost(params):
        if not params:
            return None

        if isinstance(params, dict):
            return params

        post = {}
        paramsArr = params.split('&')
        for rq in paramsArr:
            poz = rq.find('=')
            name = rq[0:poz]
            content = rq[poz + 1:]
            post[name] = content

        return post

