# #!/usr/bin/env python3
# # -*- coding: utf-8 -*-

#    TODO:   配置常量
#    Author: LTH
#    Date:   2023-6-19

import os


# 获取当前脚本文件的绝对路径
script_path = os.path.abspath(__file__)

# 项目路径
G_PROJECT_PATH = os.path.dirname(os.path.dirname(script_path))

# 工具文件夹路径
G_TOOLS_PATH = os.path.join(G_PROJECT_PATH, 'toolsDir')

# 项目名称
G_PROJECT_NAME = "猫咪的工具箱"

# 用户路径
userPath = os.path.expanduser('~')

# 缓存路径
G_CACHE_PATH = os.path.join(userPath, 'catToolsCache')

# 日志路径
G_LOG_PATH = os.path.join(G_CACHE_PATH, 'log.txt')

# 数据池文件路径
G_DATA_POOL_PATH = os.path.join(G_CACHE_PATH, "data", "dataPool.json")

# 图标路径
G_ICON_PATH = os.path.join(G_PROJECT_PATH, "res", "131.ico")

# APP路径
G_APP_PATH = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(script_path))))

# 版本号
G_VERSION = "0.2.3"

# 更新文档链接(腾讯文档表格链接即可)
G_UPDATE_DOC_URL = ""
