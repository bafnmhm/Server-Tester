import re


class Parser:
    def parse(self, file):
        allReq = []
        req = {}
        post = ''

        with open(file, 'rb') as f:
            for line in f:
                try:
                    line = line.decode('utf-8', 'ignore')
                except ValueError:
                    line = line.decode('gbk', 'ignore')
                except:
                    print('不支持的文本编码')
                    return False

                # 折行
                if self.isWordwrap(line):
                    continue
                # 注释
                if self.isComment(line):
                    continue
                # url
                if self.isUrl(line):
                    req['url'] = line.strip()
                    continue
                # post
                post += line.strip()

            req['post'] = self.parsePost(post)
            allReq.append(req)

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

    @staticmethod
    def isComment(line):
        return line.strip().find('#') == 0
