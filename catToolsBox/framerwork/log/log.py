# #!/usr/bin/env python3
# # -*- coding: utf-8 -*-

#    TODO:   日志文件
#    Author: LTH
#    Date:   2023-6-19


import os
import time

from framerwork.config import G_LOG_PATH
from framerwork.config import G_CACHE_PATH
from framerwork.file.pathTool import Path

# 获取当前脚本文件的绝对路径
script_path = os.path.abspath(__file__)
isAppOpen = False
# 是否带.app
if '.app' in script_path:
    isAppOpen = True

class Log:

    # 清空日志文件
    @staticmethod
    def clear():
        if os.path.exists(G_LOG_PATH):
            os.remove(G_LOG_PATH)

    @staticmethod
    def __console(level, message):
        message = str(message)
        if not isAppOpen:
            print(message)
        if not os.path.exists(G_CACHE_PATH):
            Path().mkdir(G_CACHE_PATH)
        # 续写
        f = open(G_LOG_PATH, 'a', encoding='utf-8')
        now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
        string = now + " " + level + " " + message + '\n'
        f.write(string)
        f.close()

    @staticmethod
    def debug(message):
        Log.__console('debug', message)

    @staticmethod
    def info(message):
        Log.__console('info', message)

    @staticmethod
    def warning(message):
        Log.__console('warning', message)

    @staticmethod
    def error(message):
        Log.__console('error', message)
