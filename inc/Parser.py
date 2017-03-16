import re


class Parser:
    def parse(self, file):
        allReq = []
        req = {}

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
                # 新的请求
                if self.isDivision(line):
                    allReq.append(req)
                    req = {'url': req['url']}
                    continue
                # url
                if self.isUrl(line):
                    if 'url' in req:  # 新的请求
                        allReq.append(req)
                        req = {}
                    req['url'] = line.strip()
                    continue
                # post
                req['post'] = 'post' in req and req['post'] + line.strip() or line.strip()

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
    def isComment(line):
        return line.strip().find('#') == 0

    @staticmethod
    def isDivision(line):
        return line == '<<<'
