import os
import sys
from inc.Parser import *
from inc.Request import *

path = 'usecase'
scriptPath = sys.path[0]
parser = Parser()
request = Request()
for curPath in os.walk(path):
    for file in curPath[2]:
        fileDir = scriptPath + '\\' + curPath[0] + '\\' + file
        reportPath = scriptPath + '\\' + curPath[0].replace(path, 'report')
        reportFilePath = reportPath + '\\' + file

        # 删除原有的报告
        if os.path.exists(reportFilePath):
            os.remove(reportFilePath)

        # 创建路径
        if not os.path.exists(reportPath):
            os.makedirs(reportPath)

        reqArr = parser.parse(fileDir)
        for req in reqArr:

            # 发送请求
            request.httpSend(req['url'], req['post'])
            if request.isConnectSuccess():
                # 请求成功，保存结果
                with open(reportFilePath, 'a', encoding='utf-8') as f:
                    res = request.getContent()
                    res = res.decode(encoding='utf-8')
                    f.writelines(res)
                f.close()
