#!/usr/bin/python
# -*- coding: utf-8 -*-
import os

from framerwork.config import G_CACHE_PATH
from framerwork.data.dataPool import DataPool


# @Time    : 2023/6/30 8:33 AM
# @Author  : LTH
# @File    : appData.py


class AppData:
    _instance = None

    def __init__(self):
        self.toolsName = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(AppData, cls).__new__(cls)
        return cls._instance

    # 设置当前工具
    def set_current_tool(self, tool):
        self.toolsName = tool

    # 获取当前工具
    def get_current_tool(self):
        return self.toolsName

    # 获取缓存路径
    def get_cache_path(self, toolName=None):
        toolName = self.toolsName if not toolName else toolName
        if not toolName:
            return G_CACHE_PATH
        key = toolName + "cache"
        if DataPool().getData(key):
            return DataPool().getData(key)
        else:
            return os.path.join(G_CACHE_PATH, key)
