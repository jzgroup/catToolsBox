#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time    : 2023/6/25 2:06 PM
# @Author  : LTH
# @File    : compressImgWindow.py

from toolsFramerwork.windowBase import windowBase, Thread
from PyQt5.QtCore import QTimer
from PyQt5 import QtWidgets
from framerwork.classes import *
from toolsDir.compressImg.compressImgUi import Ui_MainWindow
from toolsDir.compressImg.compressImg import CompressImg
from PyQt5.QtWidgets import QMessageBox

# 检查libpng库是否存在
# libpng_path = ctypes.util.find_library('libpng16.16.dylib')

class Window(windowBase):
    def __init__(self):
        Log().info("x4转x2一条龙")
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.initData()
        self.addDrop()
        self.addTouch()
        # if libpng_path is not None:
        #     Log.info("libpng16.16.dylib 已安装")
        # else:
        #     Log.error("libpng16.16.dylib 未安装")
            # QMessageBox.information(self, "提示", "libpng16.16.dylib 未安装, 无法压缩，控制台运行 brew install libpng", QMessageBox.Yes)

    # 初始化数据
    def initData(self):
        # 读取数据
        if DataPool().getData('project_path'):
            self.ui.project_path.setText(DataPool().getData('project_path'))
            # 读取数据
            self.setCheckBoxData()

        self.ui.checkBox.setChecked(True)

        self.hideProgressBar()

    # 是否检测X4是否压缩过
    def checkX4isCompress(self):
        return self.ui.checkBox.isChecked()


    # 设置选项数据
    def setCheckBoxData(self):
        data = self.getSubpackage(self.ui.project_path.text())
        self.checkBoxTab = []

        checkBox = QtWidgets.QCheckBox("主包")
        checkBox.setChecked(True)
        self.ui.verticalLayout_2.addWidget(checkBox)
        self.checkBoxTab.append(checkBox)

        for i in data:
            checkBox = QtWidgets.QCheckBox(i)
            self.ui.verticalLayout_2.addWidget(checkBox)
            self.checkBoxTab.append(checkBox)

        subpackageTab = DataPool().getData('compressImg_subpackage')
        if subpackageTab:
            for i in self.checkBoxTab:
                if i.text() in subpackageTab:
                    i.setChecked(True)

        # 获得子包
    @staticmethod
    def getSubpackage(path):
        try:
            subpackage = Path.list_subDirs_name(os.path.join(path, "update"))
            # 排序
            subpackage.sort()
        except:
            Log().error("子包路径错误")
            subpackage = []
        return subpackage

    # 添加触控
    def addTouch(self):
        self.ui.homeButton.clicked.connect(self.homeButtonClicked)
        self.ui.pushButton.clicked.connect(self.pushButtonClicked)

    def clearCheckBoxData(self):
        if len(self.checkBoxTab) == 0:
            return
        for i in self.checkBoxTab:
            self.ui.verticalLayout.removeWidget(i)
            i.deleteLater()
        self.checkBoxTab = []
    # 获取压缩路径
    def getCompressPath(self):
        CompressPathTab = []
        for i in self.checkBoxTab:
            if i.isChecked():
                # CompressPathTab.append(i.text())
                path = self.ui.project_path.text()

                if i.text() == "主包":
                    newPath =  os.path.join(path, "res")
                    if os.path.exists(newPath):
                        CompressPathTab.append(newPath)
                    else:
                        CompressPathTab.append(path)
                        Log().error("不是正常的主包路径")
                else:
                    newPath =  os.path.join(path, "update", i.text())
                    if os.path.exists(newPath):
                        CompressPathTab.append(newPath)
                    else:
                        Log().error("子包路径错误")
        return CompressPathTab


    # 开始压缩
    def pushButtonClicked(self):
        Log().info("点击开始压缩按钮")
        self.progressBarTip = "正在压缩X4图片:"
        self.progressBarValue = 0
        thread = Thread(self.compressImg)
        thread.start()
        self.thread = thread
        self.showProgressBar()
        # 定时器 打印123
        self.timer = QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.start(500)
        self.setProgressBarValue(self.progressBarValue)
        self.setProgressBarTip(self.progressBarTip)

        # 保存子包信息
        subpackage = []
        for i in self.checkBoxTab:
            if i.isChecked():
                subpackage.append(i.text())
        DataPool().setData('compressImg_subpackage', subpackage)


    def update(self):
        if self.thread.isFinished():
            self.hideProgressBar()
            self.timer.stop()
            Log().info("定时器停止")
            QMessageBox.information(self, "提示", "压缩完成", QMessageBox.Ok)
            Log().info("压缩完成")
        else:
            self.setProgressBarValue(self.progressBarValue)
            self.setProgressBarTip(self.progressBarTip)


    def compressImg(self):
        CompressImg(self.ui.project_path.text(), self).compress()


    # 添加拖拽
    def addDrop(self):
        # # 可以使用户拖放文件夹以添加项目路径
        self.ui.project_path.setAcceptDrops(True)
        self.ui.project_path.dragEnterEvent = self.dragEnterEvent
        self.ui.project_path.dropEvent = self.dropEvent


    # 隐藏进度条
    def hideProgressBar(self):
       self.ui.pushButton.show()
       self.ui.progressBar.hide()
       self.ui.label_2.hide()

    # 显示进度条
    def showProgressBar(self):
       self.ui.pushButton.hide()
       self.ui.progressBar.show()
       self.ui.label_2.show()

    #修改进度条的提示
    def setProgressBarTip(self, tip):
       self.ui.label_2.setText(tip)


    # 设置进度条的值
    def setProgressBarValue(self, value):
        self.ui.progressBar.setValue(value)

    def dropEvent(self, event):
        if event.mimeData().hasUrls() and len(event.mimeData().urls()) == 1:
            # 如果拖动的 MIME 数据中包含 URI，则使用第一个 URI 设置进程路径
            url = event.mimeData().urls()[0]
            path = url.toLocalFile()
            self.ui.project_path.setText(path)
            if path:
                DataPool().setData('project_path', path)
                self.clearCheckBoxData()
                self.setCheckBoxData()



    def enterButtonClicked(self):
        self.pushButtonClicked()



