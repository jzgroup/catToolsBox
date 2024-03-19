#!/usr/bin/python
# -*- coding: utf-8 -*-
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QMessageBox

# @Time    : 2023/7/4 4:26 PM
# @Author  : LTH
# @File    : codeGenerationWindow.py

from framerwork.classes import *
from toolsFramerwork.windowBase import windowBase
from toolsFramerwork.windowBase import Thread
from toolsDir.checkRes.checkRes import Ui_MainWindow
from toolsDir.checkRes.module.checkSound import CheckSound
from toolsDir.checkRes.module.checkVoice import CheckVoice
from toolsDir.checkRes.module.checkImage import CheckImage
import subprocess

G_CACHE_PATH = AppData.get_cache_path(AppData)

if not os.path.exists(G_CACHE_PATH):
    os.makedirs(G_CACHE_PATH)


class Window(windowBase):
    def __init__(self):
        self._checkVoiceModule = None
        self._checkSoundModule = None
        self.touchLock = None
        Log().info("检查资源")
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.initData()
        self.addTouch()
        self.addDrop()

    # 初始化数据
    def initData(self):
        # 读取数据
        if DataPool().getData('project_path'):
            self.ui.project_path.setText(DataPool().getData('project_path'))

    # 添加触控
    def addTouch(self):
        self.ui.backHome.clicked.connect(self.homeButtonClicked)
        self.ui.checkSoundButton.clicked.connect(self.checkSoundButtonClicked)
        self.ui.openCheckSoundTxtButton.clicked.connect(self.openCheckSoundTxtButtonClicked)
        self.ui.deleteUnusedSoundButton.clicked.connect(self.deleteUnusedSoundButtonClicked)
        self.ui.checkVoiceBtn.clicked.connect(self.checkVoiceBtnClicked)
        self.ui.openCheckVoiceBtn.clicked.connect(self.openCheckVoiceBtnClicked)
        self.ui.deleteCheckVoiceBtn.clicked.connect(self.deleteCheckVoiceBtnClicked)
        self.ui.checkImage.clicked.connect(self.checkImageClicked)
        self.ui.abnormalImages.clicked.connect(self.abnormalImagesClicked)
    # 添加拖拽
    def addDrop(self):
        # # 可以使用户拖放文件夹以添加项目路径
        self.ui.project_path.setAcceptDrops(True)
        self.ui.project_path.dragEnterEvent = self.dragEnterEvent
        self.ui.project_path.dropEvent = self.dropEvent

    def dropEvent(self, event):
        if event.mimeData().hasUrls() and len(event.mimeData().urls()) == 1:
            # 如果拖动的 MIME 数据中包含 URI，则使用第一个 URI 设置进程路径
            url = event.mimeData().urls()[0]
            path = url.toLocalFile()
            self.ui.project_path.setText(path)
            if path:
                DataPool().setData('project_path', path)


    def checkSoundButtonClicked(self):
        if self.touchLock:
            return
        self.touchLock = True
        projectPath = self.ui.project_path.text()
        if not projectPath:
            QMessageBox.warning(self, "警告", "请选择项目路径")
            return
        if not os.path.exists(projectPath):
            QMessageBox.warning(self, "警告", "项目路径不存在")
            return
        self.checkSoundProgressBarValue = 0
        self._checkSoundModule = CheckSound(projectPath, G_CACHE_PATH, self)
        # 检查音频

        Log().info("点击检查音频")
        thread = Thread(self.checkSound)
        thread.start()
        self.threadCheckSound = thread
        # 定时器 打印123
        self.timerCheckSound = QTimer()
        self.timerCheckSound.timeout.connect(self.updateCheckSound)
        self.timerCheckSound.start(500)
        self.ui.checkSoundProgressBar.setValue(self.checkSoundProgressBarValue)

    def checkSound(self):
        self._checkSoundModule.checkSound()


    def updateCheckSound(self):
        if self.threadCheckSound.isFinished():
            self.timerCheckSound.stop()
            self.touchLock = False
            Log().info("定时器停止")
            self.openCheckSoundTxtButtonClicked()
            Log().info("检查音频")
            self.ui.checkSoundProgressBar.setValue(0)
        else:
            self.ui.checkSoundProgressBar.setValue(self.checkSoundProgressBarValue)

    def openCheckSoundTxtButtonClicked(self):
        if self._checkSoundModule:
            self._checkSoundModule.openCheckSoundTxt()
        else:
            self._checkSoundModule = CheckSound("", G_CACHE_PATH, self)
            self._checkSoundModule.openCheckSoundTxt()

    def deleteUnusedSoundButtonClicked(self):
        projectPath = self.ui.project_path.text()
        if not projectPath:
            QMessageBox.warning(self, "警告", "请选择项目路径")
            return
        if not os.path.exists(projectPath):
            QMessageBox.warning(self, "警告", "项目路径不存在")
            return
        text = None
        if self._checkSoundModule:
            text = self._checkSoundModule.deleteUnusedSound()
        else:
            self._checkSoundModule = CheckSound(projectPath, G_CACHE_PATH, self)
            text = self._checkSoundModule.deleteUnusedSound()
        if text:
            QMessageBox.information(self, "提示", text, QMessageBox.Ok)


    def checkVoiceBtnClicked(self):
        if self.touchLock:
            return
        self.touchLock = True
        projectPath = self.ui.project_path.text()
        if not projectPath:
            QMessageBox.warning(self, "警告", "请选择项目路径")
            return
        if not os.path.exists(projectPath):
            QMessageBox.warning(self, "警告", "项目路径不存在")
            return
        self.checkVoiceProgressBarValue = 0
        self._checkVoiceModule = CheckVoice(projectPath, G_CACHE_PATH, self)
        # 检查台词
        Log().info("点击检查台词")
        thread = Thread(self.checkVoice)
        thread.start()
        self.threadCheckVoice = thread
        # 定时器 打印123
        self.timerCheckVoice = QTimer()
        self.timerCheckVoice.timeout.connect(self.updateCheckVoice)
        self.timerCheckVoice.start(500)
        self.ui.checkVoiceProgressBar.setValue(self.checkVoiceProgressBarValue)

    def checkVoice(self):
        self._checkVoiceModule.checkVoice()

    def updateCheckVoice(self):
        if self.threadCheckVoice.isFinished():
            self.timerCheckVoice.stop()
            self.touchLock = False
            Log().info("定时器停止")
            self.openCheckVoiceBtnClicked()
            Log().info("检查音频")
            self.ui.checkVoiceProgressBar.setValue(0)
        else:
            self.ui.checkVoiceProgressBar.setValue(self.checkVoiceProgressBarValue)


    def openCheckVoiceBtnClicked(self):
        if self._checkVoiceModule:
            self._checkVoiceModule.openCheckVoiceTxt()
        else:
            self._checkVoiceModule = CheckVoice("", G_CACHE_PATH, self)
            self._checkVoiceModule.openCheckVoiceTxt()

    def deleteCheckVoiceBtnClicked(self):
        projectPath = self.ui.project_path.text()
        if not projectPath:
            QMessageBox.warning(self, "警告", "请选择项目路径")
            return
        if not os.path.exists(projectPath):
            QMessageBox.warning(self, "警告", "项目路径不存在")
            return
        text = None
        if self._checkVoiceModule:
            text = self._checkVoiceModule.deleteUnusedSound()
        else:
            self._checkVoiceModule = CheckVoice(projectPath, G_CACHE_PATH, self)
            text = self._checkVoiceModule.deleteUnusedSound()
        if text:
            QMessageBox.information(self, "提示", text, QMessageBox.Ok)


    def checkImageClicked(self):
        if self.touchLock:
            return
        self.touchLock = True
        projectPath = self.ui.project_path.text()
        if not projectPath:
            QMessageBox.warning(self, "警告", "请选择项目路径")
            return
        if not os.path.exists(projectPath):
            QMessageBox.warning(self, "警告", "项目路径不存在")
            return
        self.checkImageProgressBarValue = 0

        self._checkImageModule = CheckImage(projectPath, self)
        # 检查台词
        Log().info("点击检查图片")
        thread = Thread(self.checkImage)
        thread.start()
        self.threadCheckImage = thread
        # 定时器 打印123
        self.timerCheckImage = QTimer()
        self.timerCheckImage.timeout.connect(self.updateCheckImagee)
        self.timerCheckImage.start(500)
        self.ui.checkImgProgressBar.setValue(self.checkImageProgressBarValue)

    def checkImage(self):


        self._checkImageModule.checkImage()

    def updateCheckImagee(self):
        if self.threadCheckImage.isFinished():
            self.timerCheckImage.stop()
            self.touchLock = False
            Log().info("定时器停止")
            # self.abnormalImagesClicked()
            Log().info("检查图片")
            self.ui.checkImgProgressBar.setValue(0)
        else:
            self.ui.checkImgProgressBar.setValue(self.checkImageProgressBarValue)

    #
    def abnormalImagesClicked(self):
        subprocess.Popen(['open', '-R', os.path.join(G_CACHE_PATH, '异常图片')])


