import os
import sys
import json
from xml.dom import minidom
from inc.Parser import *
from inc.Request import *

usecaseDir = 'workplace\\usecase'
reportDir = 'workplace\\report'
scriptPath = sys.path[0]
parser = Parser()
request = Request()

for i, cmd in enumerate(sys.argv):
    # 指定请求ip
    if cmd == '--ip' or cmd == '-i':
        request.host = sys.argv[i + 1]
    # 指定用例路径
    if cmd == '--dir' or cmd == '-d':
        usecaseDir = 'workplace\\' + sys.argv[i + 1]
        reportDir = 'workplace\\report - ' + sys.argv[i + 1]
    # 指定报告路径
    if cmd == '--outdir' or cmd == '-o':
        reportDir = 'workplace\\' + sys.argv[i + 1]

for curPath in os.walk(scriptPath + '\\' + usecaseDir):
    for file in curPath[2]:
        # 执行一个测例文件
        fileDir = curPath[0] + '\\' + file
        reportPath = curPath[0].replace(usecaseDir, reportDir)
        reportFilePath = reportPath + '\\' + file

        # 删除原有的报告
        if os.path.exists(reportFilePath):
            os.remove(reportFilePath)

        # 创建路径
        if not os.path.exists(reportPath):
            os.makedirs(reportPath)

        reqArr = parser.parse(fileDir)
        if not reqArr:
            continue

        # 创建文本，保存结果
        with open(reportFilePath, 'a', encoding='utf-8') as f:
            for req in reqArr:
                # 发送请求
                request.reset()
                request.httpSend(req)

                # 用例有误
                if request.error:
                    f.writelines('#####\n\n' + request.error + '\n\n')
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
                    res = json.dumps(res, indent=4, sort_keys=True)
                except ValueError:
                    pass

                f.writelines('#####\n\n' + res + '\n\n')
        f.close()
