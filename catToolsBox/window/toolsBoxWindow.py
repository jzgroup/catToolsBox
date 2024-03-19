# #!/usr/bin/env python3
# # -*- coding: utf-8 -*-

#    TODO:   工具箱窗口
#    Author: LTH
#    Date:   2023-6-19

import importlib
import subprocess
import importlib.util
from PyQt5 import QtWidgets

from window.settings.settingsWindow import SettingsWindow
from window.toolsBoxUi import Ui_MainWindow
from window.toolsManage import ToolsManage

from framerwork.classes import *




class ToolsBoxWindow(QtWidgets.QMainWindow):
    def __init__(self):
        Log().info("打开工具箱窗口")


        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.showToolsBox(ToolsManage().get_tools())
        self.addTouch()

    # 添加触控
    def addTouch(self):
        self.ui.toolsDir.clicked.connect(self.toolsDirBtnClicked)
        self.ui.settingButton.clicked.connect(self.settingBtnClicked)
        self.ui.cacheDir.clicked.connect(self.cacheDirBtnClicked)

        # 工具箱按钮
        for toolBtn in self.ui.toolsBtnTab:
            button = self.ui.toolsBtnTab[toolBtn]
            button.clicked.connect(self.toolBtnClicked)

    def cacheDirBtnClicked(self):
        Log().info("点击缓存目录按钮")
        subprocess.Popen(['open', '-R', G_CACHE_PATH])

    @staticmethod
    def toolsDirBtnClicked():
        Log().info("点击工具箱目录按钮")
        subprocess.Popen(['open', '-R', G_TOOLS_PATH])

    @staticmethod
    def settingBtnClicked():
        Log().info("点击设置窗口按钮")
        from window.windowManage import WindowManage
        # 从新的“module”对象中访问导入的Python类、函数和变量
        WindowManage.switchWindow(WindowManage, SettingsWindow())

    # 工具箱按钮点击事件
    def toolBtnClicked(self, name):

        button = self.sender()
        toolData = button.toolData
        toolName = name or toolData.getName()

        # try:
        Log().info("打开工具: " + toolName)
        # 定义要导入的模块名称和文件路径
        scriptPath = toolData.scriptPath()

        if not os.path.exists(scriptPath):
            Log().error(toolData.getName() + ":启动失败 " + "，请检查工具路径是否正确")
            return

        # 使用 Python 的 `importlib` 模块动态导入模块
        spec = importlib.util.spec_from_file_location(toolName, scriptPath)
        module = importlib.util.module_from_spec(spec)
        # 使用“loader.exec_module()”方法加载 Python 模块并解析到新的“module”对象中
        AppData.set_current_tool(AppData, toolName)
        spec.loader.exec_module(module)
        Log().info("加载模块" + scriptPath)
        from window.windowManage import WindowManage

        try:
            # 从新的“module”对象中访问导入的Python类、函数和变量
            WindowManage.switchWindow(WindowManage, module.Window())
        except Exception as e:
            # 直接运行
            subprocess.Popen(['python3', scriptPath])
            Log().error(toolData.getName() + ":启动失败")
            Log().error(e)
         # 从新的“module”对象中访问导入的Python类、函数和变量
        # WindowManage.switchWindow(WindowManage, module.Window())
        #

        # except Exception as e:
        #     Log().error(toolData.getName() + ":启动失败")
        #     Log().error("错误信息:" + str(e))

    def closeEvent(self, event):
        Log().info("关闭工具箱窗口")
        event.accept()
