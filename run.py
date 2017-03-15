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
        if not reqArr:
            print(fileDir + ' : 测试用例有误，请检查')
            continue

        for req in reqArr:
            # 发送请求
            request.httpSend(req['url'], req['post'])

            # 请求结束，保存结果
            print(reportFilePath)
            with open(reportFilePath, 'a', encoding='utf-8') as f:
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
