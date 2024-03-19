#!/usr/bin/python
# -*- coding: utf-8 -*-

#    TODO:   git提交模版设置窗口
#    Author: LTH
#    Date:   2023-6-25

from toolsFramerwork.windowBase import windowBase
from PyQt5.QtWidgets import QMessageBox

from toolsDir.githook.githookUi import Ui_MainWindow
from framerwork.classes import *

# 获取当前脚本文件的绝对路径
script_path = os.path.abspath(__file__)


class Window(windowBase):
    def __init__(self):
        self._btnLock = False
        Log().info("git提交模版设置窗口")
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.addTouch()
        self.ui.addItems(self.readData())

    # 添加触控
    def addTouch(self):
        self.ui.homeButton.clicked.connect(self.homeButtonClicked)
        self.ui.setup.clicked.connect(self.setStage)


    # 提示窗口
    def showMessageBox(self, title, message):
        QMessageBox.information(self, title, message, QMessageBox.Ok)

    # 槽函数：选定的阶段
    def setStage(self):
        if self._btnLock:
            return
        self._btnLock = True
        currentItem = self.ui.listWidget.currentItem()
        if currentItem:
            # 获取当前选中的阶段
            stage = currentItem.text()
            # 获取当前选中的阶段的配置
            stageConfig = self._testConfig[stage]

            # 用户路径
            userPath = os.path.expanduser('~')
            # 写入文件
            with open(os.path.join(userPath, ".stCommitMsg"), "w", encoding='utf-8') as f:
                f.write(stageConfig)

            Git.config_commit_template(os.path.join(userPath, ".stCommitMsg"))
            self._btnLock = False
            Log().info("git设置阶段为：" + stage)
            self.showMessageBox("提示", "git设置阶段为：" + stage + "\n设置成功")

    # 读取阶段数据
    def readData(self):
        # 文本配置文件路径
        textPath = os.path.join(os.path.dirname(script_path), 'text_config.json')
        self._testConfig = Json.read_json(textPath)
        return self._testConfig
