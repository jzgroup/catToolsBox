#!/usr/bin/python
# -*- coding: utf-8 -*-
import importlib

from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QMessageBox

# @Time    : 2023/7/4 4:26 PM
# @Author  : LTH
# @File    : addBoneWindow



from toolsFramerwork.windowBase import windowBase
from framerwork.classes import *
from toolsDir.addBone.addBone import Ui_MainWindow
from toolsDir.addBone.addBoneControls import AddBoneControls
from toolsFramerwork.windowBase import Thread

class Window(windowBase):
    def __init__(self):
        self._btnLock = False
        Log().info("添加骨骼")
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.initData()
        self.addTouch()
        self.addDrop()
        # 隐藏待开发
        self.ui.checkBox.hide()


    # 添加触控
    def addTouch(self):
        self.ui.backHome.clicked.connect(self.homeButtonClicked)
        self.ui.addOneBone.clicked.connect(self.addOneBoneClicked)
        self.ui.addMoreBone.clicked.connect(self.addMoreBoneClicked)

    # 初始化数据
    def initData(self):
        # 读取数据
        if DataPool().getData('project_path'):
            self.ui.project_path.setText(DataPool().getData('project_path'))
        if DataPool().getData('oneBonePath'):
            self.ui.oneBenePath.setText(DataPool().getData('oneBonePath'))
        if DataPool().getData('moreBoneExcelPath'):
            self.ui.excelFile.setText(DataPool().getData('moreBoneExcelPath'))
        if DataPool().getData('moreBonePath'):
            self.ui.moreBonePath.setText(DataPool().getData('moreBonePath'))

    # 添加拖拽
    def addDrop(self):
        # # 可以使用户拖放文件夹以添加项目路径
        self.ui.project_path.setAcceptDrops(True)
        self.ui.project_path.dragEnterEvent = self.dragEnterEvent
        self.ui.project_path.dropEvent = self.dropEvent

        self.ui.oneBenePath.setAcceptDrops(True)
        self.ui.oneBenePath.dragEnterEvent = self.dragEnterEvent
        self.ui.oneBenePath.dropEvent = self.oneBoneDropEvent

        self.ui.moreBonePath.setAcceptDrops(True)
        self.ui.moreBonePath.dragEnterEvent = self.dragEnterEvent
        self.ui.moreBonePath.dropEvent = self.moreBoneDropEvent

        self.ui.excelFile.setAcceptDrops(True)
        self.ui.excelFile.dragEnterEvent = self.dragEnterEvent
        self.ui.excelFile.dropEvent = self.excelDropEvent
    def dropEvent(self, event):
        if event.mimeData().hasUrls() and len(event.mimeData().urls()) == 1:
            # 如果拖动的 MIME 数据中包含 URI，则使用第一个 URI 设置进程路径
            url = event.mimeData().urls()[0]
            path = url.toLocalFile()
            self.ui.project_path.setText(path)
            if path:
                DataPool().setData('project_path', path)

    def oneBoneDropEvent(self, event):
        if event.mimeData().hasUrls() and len(event.mimeData().urls()) == 1:
            # 如果拖动的 MIME 数据中包含 URI，则使用第一个 URI 设置进程路径
            url = event.mimeData().urls()[0]
            path = url.toLocalFile()
            if 'x2' in path or 'X2' in path or 'x4' in path or 'X4' in path or os.path.isdir(path):
                self.ui.oneBenePath.setText(path)
                if path:
                    DataPool().setData('oneBonePath', path)
            else:
                Log().error('请拖入正确的骨骼文件')
                QMessageBox.warning(self, "警告", "请拖入正确的骨骼文件", QMessageBox.Yes)

    def excelDropEvent(self, event):
        if event.mimeData().hasUrls() and len(event.mimeData().urls()) == 1:
            # 如果拖动的 MIME 数据中包含 URI，则使用第一个 URI 设置进程路径
            url = event.mimeData().urls()[0]
            path = url.toLocalFile()
            if 'xlsx' in path or 'xls' in path:
                self.ui.excelFile.setText(path)
                if path:
                    DataPool().setData('moreBoneExcelPath', path)
            else:
                Log().error('请拖入正确的excel文件')
                QMessageBox.warning(self, "警告", "请拖入正确的excel文件", QMessageBox.Yes)

    def moreBoneDropEvent(self, event):
        if event.mimeData().hasUrls() and len(event.mimeData().urls()) == 1:
            # 如果拖动的 MIME 数据中包含 URI，则使用第一个 URI 设置进程路径
            url = event.mimeData().urls()[0]
            path = url.toLocalFile()
            if os.path.isdir(path):
                self.ui.moreBonePath.setText(path)
                if path:
                    DataPool().setData('moreBonePath', path)
            else:
                Log().error('请拖入正确的骨骼文件夹')
                QMessageBox.warning(self, "警告", "请拖入正确的骨骼文件夹", QMessageBox.Yes)


    def addOneBoneClicked(self):
        if not self.ui.project_path.text() or self.ui.project_path.text() == '':
            Log().error('请拖入项目路径')
            QMessageBox.warning(self, "警告", "请拖入项目路径", QMessageBox.Yes)
            return
        if not self.ui.oneBenePath.text() or self.ui.oneBenePath.text() == '':
            Log().error('请拖入骨骼文件')
            QMessageBox.warning(self, "警告", "请拖入骨骼文件", QMessageBox.Yes)
            return

        if self._btnLock:
            return
        self._btnLock = True

        text = AddBoneControls(self.ui.oneBenePath.text(), None, self.ui.project_path.text(),
                        self.ui.checkBox.isChecked(), None).addOneBone()
        Log().info("添加骨骼完成")
        QMessageBox.information(self, "提示", text, QMessageBox.Yes)
        self._btnLock = False


    def addMoreBoneClicked(self):
        if not self.ui.project_path.text() or self.ui.project_path.text() == '':
            Log().error('请拖入项目路径')
            QMessageBox.warning(self, "警告", "请拖入项目路径", QMessageBox.Yes)
            return
        if not self.ui.moreBonePath.text() or self.ui.moreBonePath.text() == '':
            Log().error('请拖入骨骼文件夹')
            QMessageBox.warning(self, "警告", "请拖入骨骼文件夹", QMessageBox.Yes)
            return
        if not self.ui.excelFile.text() or self.ui.excelFile.text() == '':
            Log().error('请拖入excel文件')
            QMessageBox.warning(self, "警告", "请拖入excel文件", QMessageBox.Yes)
            return
        if self._btnLock:
            return
        self._btnLock = True

        self.progressBarValue = 0

        thread = Thread(self.addMoreBone)
        thread.start()
        self.thread = thread
        # 定时器
        self.timer= QTimer()
        self.timer.timeout.connect(self.updateAddMoreBone)
        self.timer.start(500)
        self.ui.moreProgressBar.setValue(self.progressBarValue)
        self._btnLock = False

    def addMoreBone(self):
        self.text = AddBoneControls(self.ui.moreBonePath.text(), self.ui.excelFile.text(), self.ui.project_path.text(),
                        self.ui.checkBox.isChecked(), self).addMoreBone()

    def updateAddMoreBone(self):
        if self.thread.isFinished():
            self.timer.stop()
            self.touchLock = False
            Log().info("添加骨骼完成")
            self.ui.moreProgressBar.setValue(0)
            QMessageBox.information(self, "提示", self.text, QMessageBox.Yes)
        else:
            self.ui.moreProgressBar.setValue(self.progressBarValue)
