#!/usr/bin/python
# -*- coding: utf-8 -*-

# @Time    : 2023/6/25 4:56 PM
# @Author  : LTH
# @File    : dataConversionWindow.py

import importlib.util

from toolsFramerwork.windowBase import windowBase
from framerwork.classes import *
from toolsDir.dataConversion.dataConversionUi import Ui_MainWindow


# 获取当前脚本文件的绝对路径
script_path = os.path.abspath(__file__)


module = [
    {
        "name": "json转cocos2d数据",
        "path": os.path.join(os.path.dirname(script_path), "module", 'jsonToCocos2d.py')
    },
       {
        "name": "子包的json转cocos2d数据",
        "path": os.path.join(os.path.dirname(script_path), "module", 'worldJsonToCocos2d.py')
    }
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

        # 使用 Python 的 `importlib` 模块动态导入模块
        spec = importlib.util.spec_from_file_location("module.name", path)
        foo = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(foo)
        self.ui.setAfterData(foo.dataConversion(self.ui.getBeforeData()))

        self._btnLock = False
        self.ui.conversionBtn.setText("开始转化")

