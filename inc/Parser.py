import re


class Parser:
    def parse(self, file):
        allReq = []
        req = {}
        post = ''
        with open(file, 'r') as f:
            while True:
                line = f.readline()
                if line:
                    # 折行
                    if self.isWordwrap(line):
                        continue
                    # url
                    if self.isUrl(line):
                        req['url'] = line.strip()
                        continue
                    # post
                    post += line.strip()
                else:
                    req['post'] = self.parsePost(post)
                    allReq.append(req)
                    break
        f.close()
        return allReq

    @staticmethod
    def isWordwrap(line):
        return line == '\r' or line == '\n' or line == '\r\n'

    @staticmethod
    def isUrl(line):
        return re.match('.?/thsft/', line) is not None

    @staticmethod
    def parsePost(params):
        if not params:
            return None

        post = {}
        paramsArr = params.split('&')
        for rq in paramsArr:
            poz = rq.find('=')
            name = rq[0:poz]
            content = rq[poz + 1:]
            post[name] = content

        return post
