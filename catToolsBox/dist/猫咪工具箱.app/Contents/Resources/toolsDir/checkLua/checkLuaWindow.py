#!/usr/bin/python
# -*- coding: utf-8 -*-

# @Time    : 2023/6/25 4:56 PM
# @Author  : LTH
# @File    : dataConversionWindow.py

import importlib.util
import shutil
import subprocess

from PyQt5.QtWidgets import QMessageBox

from toolsFramerwork.windowBase import windowBase, Thread
from PyQt5.QtCore import QTimer
from framerwork.classes import *
from toolsDir.checkLua.checkLua import Ui_MainWindow


G_CACHE_PATH = AppData.get_cache_path(AppData)
if not os.path.exists(G_CACHE_PATH):
    os.makedirs(G_CACHE_PATH)

from toolsDir.checkLua.check.checkLua import CheckLua


# 获取当前脚本文件的绝对路径
script_path = os.path.abspath(__file__)


class Window(windowBase):
    def __init__(self):
        self._btnLock = False
        Log().info("数据转化")
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.addTouch()
        self.hideProgressBar()

        # 读取数据
        if DataPool().getData('lua_project_path'):
            self.ui.lineEdit.setText(DataPool().getData('lua_project_path'))
            self._projectPath = DataPool().getData('lua_project_path')
        elif DataPool().getData('project_path'):
            self.ui.lineEdit.setText(DataPool().getData('project_path'))
            self._projectPath = DataPool().getData('project_path')

        if DataPool().getData('frameworkVariableArrFilePath'):
            self.ui.lineEdit_2.setText(DataPool().getData('frameworkVariableArrFilePath'))
            self._frameworkVariableArrFilePath = DataPool().getData('frameworkVariableArrFilePath')
        else:
            frameworkVariableArrFilePath = os.path.join(os.path.dirname(script_path), "check", "frameworkVariableArr.json")
            self.ui.lineEdit_2.setText(frameworkVariableArrFilePath)
            self._frameworkVariableArrFilePath = frameworkVariableArrFilePath

        if DataPool().getData('customVariableArrFilePath'):
            self.ui.lineEdit_3.setText(DataPool().getData('customVariableArrFilePath'))
            self._customVariableArrFilePath = DataPool().getData('customVariableArrFilePath')
        else:
            self._customVariableArrFilePath = ""

        if DataPool().getData('checkLua_isFilterUpper'):
            self.ui.checkBox.setChecked(DataPool().getData('checkLua_isFilterUpper'))
            self._isFilterUpper = True
        else:
            self.ui.checkBox.setChecked(False)
            self._isFilterUpper = False


    # 添加触控
    def addTouch(self):
        self.ui.lineEdit.dragEnterEvent = self.dragEnterEvent
        self.ui.lineEdit_2.dragEnterEvent = self.dragEnterEvent
        self.ui.lineEdit_3.dragEnterEvent = self.dragEnterEvent
        self.ui.lineEdit.dropEvent = self.dropEvent
        self.ui.lineEdit_2.dropEvent = self.dropEvent2
        self.ui.lineEdit_3.dropEvent = self.dropEvent3
        self.ui.pushButton.clicked.connect(self.homeButtonClicked)
        self.ui.pushButton_2.clicked.connect(self.buttonClickedCheckLua)
        self.ui.pushButton_3.clicked.connect(self.openErrorFileClicked)
        self.ui.pushButton_4.clicked.connect(self.openVariableArrFileClicked)
        self.ui.checkBox.stateChanged.connect(self.checkBoxStateChanged)

    def checkBoxStateChanged(self, state):
        Log().info("checkBoxStateChanged" + str(state))
        DataPool().setData('checkLua_isFilterUpper', state == 2)
        self._isFilterUpper = state == 2



    def openErrorFileClicked(self):
        path = os.path.join(G_CACHE_PATH, "error.txt")
        os.system("open " + path)

    def openVariableArrFileClicked(self):
        path = os.path.join(G_CACHE_PATH, "variableArr.json")
        subprocess.run(["open", "-a", "TextEdit", path])
    def setProgressBarValue(self, value):
        self.ui.progressBar.setValue(value)

    # 开始检查
    def buttonClickedCheckLua(self):
        self._projectPath = self.ui.lineEdit.text()
        self._frameworkVariableArrFilePath = self.ui.lineEdit_2.text()
        self._customVariableArrFilePath = self.ui.lineEdit_3.text()
        if not self._projectPath:
            QMessageBox.information(self, "提示", "请选择项目路径", QMessageBox.Ok)
            return

        if self._projectPath:
            DataPool().setData('lua_project_path', self._projectPath)
        if self._frameworkVariableArrFilePath:
            DataPool().setData('frameworkVariableArrFilePath', self._frameworkVariableArrFilePath)
        if self._customVariableArrFilePath:
            DataPool().setData('customVariableArrFilePath', self._customVariableArrFilePath)


        Log().info("点击开始查询")
        self.progressBarValue = 0
        thread = Thread(self.checkLua)
        thread.start()
        self.thread = thread
        self.showProgressBar()
        # 定时器 打印123
        self.timer = QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.start(500)
        self.setProgressBarValue(self.progressBarValue)


    def update(self):
        if self.thread.isFinished():
            self.hideProgressBar()
            self.timer.stop()
            Log().info("定时器停止")
            QMessageBox.information(self, "提示", "检查完成", QMessageBox.Ok)
            Log().info("检查完成")
        else:
            self.setProgressBarValue(self.progressBarValue)

    def checkLua(self):
        CheckLua(self, self._projectPath, self._frameworkVariableArrFilePath, self._customVariableArrFilePath, self._isFilterUpper).run()

    # 隐藏进度条
    def hideProgressBar(self):
        self.ui.label_4.hide()
        self.ui.progressBar.hide()
        self.ui.pushButton_3.show()
        self.ui.pushButton_4.show()
        self.ui.pushButton_2.show()

    # 显示进度条
    def showProgressBar(self):
        self.ui.label_4.show()
        self.ui.progressBar.show()
        self.ui.pushButton_3.hide()
        self.ui.pushButton_4.hide()
        self.ui.pushButton_2.hide()

    def dropEvent(self, event):
        if event.mimeData().hasUrls() and len(event.mimeData().urls()) == 1:
            # 如果拖动的 MIME 数据中包含 URI，则使用第一个 URI 设置进程路径
            url = event.mimeData().urls()[0]
            path = url.toLocalFile()
            self.ui.lineEdit.setText(path)
            if path:
                DataPool().setData('lua_project_path', path)
                self._projectPath = path

    def dropEvent2(self, event):
        if event.mimeData().hasUrls() and len(event.mimeData().urls()) == 1:
            # 如果拖动的 MIME 数据中包含 URI，则使用第一个 URI 设置进程路径
            url = event.mimeData().urls()[0]
            path = url.toLocalFile()
            self.ui.lineEdit_2.setText(path)
            if path:
                DataPool().setData('frameworkVariableArrFilePath', path)
                self._frameworkVariableArrFilePath = path

    def dropEvent3(self, event):
        if event.mimeData().hasUrls() and len(event.mimeData().urls()) == 1:
            # 如果拖动的 MIME 数据中包含 URI，则使用第一个 URI 设置进程路径
            url = event.mimeData().urls()[0]
            path = url.toLocalFile()
            self.ui.lineEdit_3.setText(path)
            if path:
                DataPool().setData('customVariableArrFilePath', path)
                self._customVariableArrFilePath = path