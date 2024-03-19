# #!/usr/bin/env python3
# # -*- coding: utf-8 -*-

#    TODO:   工具管理
#    Author: LTH
#    Date:   2023-6-20

from framerwork.classes import *


class ToolBean:
    # 工具名字: name
    # 启动脚本名字: script
    def __init__(self, name, script, path, isCache):
        self.name = name
        self.script = script
        self.path = path
        self.isCache = isCache

    def getName(self):
        return self.name

    def getScript(self):
        return self.script

    def getIsCache(self):
        return self.isCache

    def getPath(self):
        return self.path

    def scriptPath(self):
        return os.path.join(self.path, self.script) + ".py"


class ToolsManage:
    def __init__(self):
        self.tools = None

    @staticmethod
    def getConfig(path):
        config = None
        for name in os.listdir(path):
            path_file = os.path.join(path, name)
            if name == "config.json":
                config = Json.read_json(path_file)
                break
        return config

    # 数据校正
    @staticmethod
    def check_data(data):
        if data is None:
            return None

        data["name"] = data.get("name", "")
        data["scriptName"] = data.get("scriptName", "")
        data["isCache"] = data.get("isCache", False)

        return data

    def get_tools(self, subdir=None):
        subDirs = Path.list_subDirs(G_TOOLS_PATH)

        self.tools = {}
        for subDir in subDirs:
            config = self.getConfig(subDir)
            # 文件名
            fileName = os.path.basename(subDir)
            if config:
                # 将 JSON 数据直接转换为类
                data = self.check_data(config)
                toolBean = ToolBean(data["name"], data["scriptName"], subDir, data["isCache"])
                self.tools[fileName] = toolBean
            else:
                Log.error("无config.json文件")
        return self.tools
