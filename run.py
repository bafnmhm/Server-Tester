import os
import sys
import json
from xml.dom import minidom
from inc.Parser import *
from inc.Request import *

usecaseDir = 'usecase'
scriptPath = sys.path[0]
parser = Parser()
request = Request()

for i, cmd in enumerate(sys.argv):
    # 指定请求ip
    if cmd == '-ip':
        request.host = sys.argv[i + 1]

for curPath in os.walk(scriptPath + '\\' + usecaseDir):
    for file in curPath[2]:
        # 执行一个测例文件
        fileDir = curPath[0] + '\\' + file
        reportPath = curPath[0].replace(usecaseDir, 'report')
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
            request.reset()
            request.httpSend(req)

            # 请求结束，保存结果
            with open(reportFilePath, 'a', encoding='utf-8') as f:
                if request.error:
                    f.writelines(request.error)
                    break

                res = request.getContent()
                res = res.decode(encoding='utf-8')

                # 美化xml格式
                if res.find('<?xml') >= 0:
                    dom = minidom.parseString(res)
                    res = dom.toprettyxml(indent=' ' * 4)

                # 美化json格式
                try:
                    res = json.loads(res)
                    res = json.dumps(res, indent=4)
                except ValueError:
                    pass

                f.writelines(res)
            f.close()
