import os
import sys
from inc.Parser import *
from inc.Request import *

path = 'usecase'
parser = Parser()
request = Request()
for curPath in os.walk(path):
    for file in curPath[2]:
        fileDir = sys.path[0] + '\\' + curPath[0] + '\\' + file
        reqArr = parser.parse(fileDir)
        for req in reqArr:
            post = 'post' in req and req['post'] or None
            request.httpSend(req['url'], post)
