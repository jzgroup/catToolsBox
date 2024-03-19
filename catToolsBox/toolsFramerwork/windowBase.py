#!/usr/bin/python
# -*- coding: utf-8 -*-

# @Time    : 2023/7/13 2:42 PM
# @Author  : LTH
# @File    : windowBase.py

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import QThread

from framerwork.classes import *


# 继承QThread
class Thread(QThread):  # 线程1
    def __init__(self, fun):
        super().__init__()
        self.fun = fun

    def run(self):
        self.fun()

class windowBase(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()

    # 检查键盘
    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Escape:
            self.homeButtonClicked()
        # 回车键
        if event.key() == QtCore.Qt.Key_Return or event.key() == QtCore.Qt.Key_Enter:
            self.enterButtonClicked()

    # 按钮点击事件
    def homeButtonClicked(self):
        Log().info("点击返回按钮")
        from window.windowManage import WindowManage
        # 从新的“module”对象中访问导入的Python类、函数和变量
        WindowManage.restoreHome(WindowManage)

    # 添加拖拽
    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls() and len(event.mimeData().urls()) == 1:
            # 如果拖动的 MIME 数据中包含 URI，则接受拖动操作
            event.acceptProposedAction()

    def enterButtonClicked(self):
        pass
