# #!/usr/bin/env python3
# # -*- coding: utf-8 -*-

#    TODO:   数据池
#    Author: LTH
#    Date:   2023-4-26

import os
from framerwork.file.jsonTool import Json
from framerwork.config import G_DATA_POOL_PATH
from framerwork.log.log import Log


class DataPool():
    _instance = None
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(DataPool, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if not os.path.exists(G_DATA_POOL_PATH):
            # 如果不存在数据池文件,则创建
            os.makedirs(os.path.dirname(G_DATA_POOL_PATH), exist_ok=True)
            self.dataPool = {}
            Json.write_json(G_DATA_POOL_PATH, self.dataPool)
        else:
            self.readData()

    # 读取数据
    def readData(self):
        # if self.dataPool:
        #     return
        self.dataPool = Json.read_json(G_DATA_POOL_PATH)

    # 获得数据
    def getData(self, key):
        self.readData()
        if key not in self.dataPool:
            # 如果键不存在▍
            return None
        return self.dataPool[key]

    # 设置数据
    def setData(self, key, value):
        Log.info("设置数据: %s = %s" % (key, value))
        self.readData()
        self.dataPool[key] = value
        Json.write_json(G_DATA_POOL_PATH, self.dataPool)
