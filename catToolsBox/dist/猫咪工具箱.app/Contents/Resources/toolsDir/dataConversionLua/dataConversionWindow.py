#!/usr/bin/python
# -*- coding: utf-8 -*-

# @Time    : 2023/6/25 4:56 PM
# @Author  : LTH
# @File    : dataConversionWindow.py

import importlib.util

from toolsFramerwork.windowBase import windowBase
from framerwork.classes import *
from toolsDir.dataConversionLua.dataConversionUi import Ui_MainWindow


#python调用lua脚本
from lupa import LuaRuntime

# 获取当前脚本文件的绝对路径
script_path = os.path.abspath(__file__)


module = [
    {
        "name": "猫咪压缩数据转化",
        "path": os.path.join(os.path.dirname(script_path), "module", 'jsonToCocos2d.lua')
    },
    {
        "name": "世界 猫咪压缩数据转化",
        "path": os.path.join(os.path.dirname(script_path), "module", 'worldjsonToCocos2d.lua')
    },
]


class Window(windowBase):
    def __init__(self):
        self._btnLock = False
        Log().info("数据转化")
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.addTouch()
        self.ui.addItems(module)


    # 添加触控
    def addTouch(self):
        self.ui.homeButton.clicked.connect(self.homeButtonClicked)
        self.ui.conversionBtn.clicked.connect(self.conversionBtnClicked)


    def conversionBtnClicked(self):
        if self._btnLock:
            return
        Log().info("点击转化按钮")
        self._btnLock = True
        self.ui.conversionBtn.setText("转化中...")
        path = self.ui.getItems()

        # # 使用 Python 的 `importlib` 模块动态导入模块
        # spec = importlib.util.spec_from_file_location("module.name", path)
        # foo = importlib.util.module_from_spec(spec)
        # spec.loader.exec_module(foo)
        try:
            # 创建 Lua 运行环境
            lua = LuaRuntime(unpack_returned_tuples=True)
            #添加新的package.path
            newPath =  ';' + os.path.join(os.path.dirname(path), '?.lua')
            lua.execute("package.path = package.path .. '" + newPath + "'")
            fileHandler = open(path, encoding='utf-8')
            content = fileHandler.read()
            # # 执行 Lua 脚本文件
            lua.execute(content)
            # 获取 Lua 全局环境中的 greet 函数
            dataConversion = lua.globals()['dataConversion']

            newDate = dataConversion(self.ui.getBeforeData())

            # # 执行 Lua 脚本
            self.ui.setAfterData(newDate)
        except Exception as e:
            Log().error(e)
            Log().error("发生错误")
            self.ui.setAfterData("发生错误")

        self._btnLock = False
        self.ui.conversionBtn.setText("开始转化")

