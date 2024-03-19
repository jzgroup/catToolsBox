#!/usr/bin/python
# -*- coding: utf-8 -*-
from PyQt5 import QtWidgets, QtCore

# @Time    : 2023/7/3 7:55 AM
# @Author  : lth
# @File    : settingsWindow.py

from framerwork.classes import *
from window.settings.settings import Ui_mainWindow
from window.toolsManage import ToolsManage


class ToolItem(QtWidgets.QFrame):
    def __init__(self, name, key, isShow, parent=None):
        super().__init__(parent)

        self.name = name
        # self.isCache = isCache
        # 是否显示
        self.isNoShow = isShow
        self.key = key
        self.initUI()

    def initUI(self):
        self.setMinimumSize(QtCore.QSize(0, 0))
        self.setObjectName("tools")
        # self.setFrameShape(QtWidgets.QFrame.Box)


    def addSubModule(self):
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        # 设置高
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        # self.spinBox = QtWidgets.QSpinBox(self)
        # self.spinBox.setObjectName("spinBox")
        # self.horizontalLayout_3.addWidget(self.spinBox)
        self.label_3 = QtWidgets.QLabel(self)
        self.label_3.setObjectName("label_3")
        self.label_3.setText(self.name)
        # 设置长
        self.label_3.setFixedWidth(200)
        self.horizontalLayout_3.addWidget(self.label_3)
        self.checkBox_3 = QtWidgets.QCheckBox(self)
        self.checkBox_3.setObjectName("checkBox_3")
        self.checkBox_3.setText("是否关闭显示")
        self.horizontalLayout_3.addWidget(self.checkBox_3)

        if self.isNoShow:
            self.checkBox_3.setChecked(True)
        else:
            self.checkBox_3.setChecked(False)

        #点击事件
        self.checkBox_3.stateChanged.connect(self.checkBox_stateChanged)

    def checkBox_stateChanged(self):
        key =  self.key
        noShwoTab = DataPool().getData("NoShowTab")
        if noShwoTab is None:
            noShwoTab = {}

        # Log().info(self.checkBox_3.isChecked())
        if self.checkBox_3.isChecked():
            noShwoTab[key] = True
            DataPool().setData("NoShowTab", noShwoTab)
        else:
            noShwoTab[key] = False
            DataPool().setData("NoShowTab", noShwoTab)





    # 添加拖拽
    def addDrop(self):
        if self.isCache:
            # # 可以使用户拖放文件夹以添加项目路径
            self.lineEdit.setAcceptDrops(True)
            self.lineEdit.dragEnterEvent = self.dragEnterEvent
            self.lineEdit.dropEvent = self.dropEvent

    # 添加拖拽
    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls() and len(event.mimeData().urls()) == 1:
            # 如果拖动的 MIME 数据中包含 URI，则接受拖动操作
            event.acceptProposedAction()

    def dropEvent(self, event):
        if event.mimeData().hasUrls() and len(event.mimeData().urls()) == 1:
            # 如果拖动的 MIME 数据中包含 URI，则使用第一个 URI 设置进程路径
            url = event.mimeData().urls()[0]
            path = url.toLocalFile()
            self.lineEdit.setText(path)
            key = self.name + "cache"
            if path:
                DataPool().setData(key, path)



class SettingsWindow(QtWidgets.QMainWindow):
    def __init__(self):
        Log().info("打开设置箱窗口")
        self._startEncryptLock = False
        super().__init__()
        self.ui = Ui_mainWindow()
        self.ui.setupUi(self)
        self.init()
        self.addTouch()

        self.ui.verticalLayout_4.setSpacing(10)
        tab = ToolsManage().get_tools()

        noShwoTab = DataPool().getData("NoShowTab")
        if noShwoTab is None:
            noShwoTab = {}

        for i in tab:
            data = tab[i]

            tool = ToolItem(data.getName(), data.getPath(),  noShwoTab.get(data.getPath()) and noShwoTab[data.getPath()], self)
            tool.addSubModule()
            self.ui.verticalLayout_4.addWidget(tool)

    # 初始化
    def init(self):
        Log().info("初始化工具箱窗口")
        # # self.ui.checkBox.setChecked(False)
        # Log.info(DataPool().getData("isOpenLogin"))
        if DataPool().getData("isOpenLogin"):
            self.ui.checkBox.setChecked(True)
        else:
            self.ui.checkBox.setChecked(False)

    # 添加触控
    def addTouch(self):
        self.ui.backHome.clicked.connect(self.homeButtonClicked)
        self.ui.checkBox.stateChanged.connect(self.checkBoxStateChanged)

    def homeButtonClicked(self):
        Log().info("点击返回按钮")
        from window.windowManage import WindowManage
        # 从新的“module”对象中访问导入的Python类、函数和变量
        WindowManage.restoreHome(WindowManage)

    def checkBoxStateChanged(self):
        Log().info("点击复选框")
        if self.ui.checkBox.isChecked():
            SystemControls.add_login_item()
            Log().info("复选框被选中")
            self._startEncryptLock = True
        else:
            SystemControls.remove_login_item()
            Log().info("复选框未被选中")
            self._startEncryptLock = False
        SystemControls.is_login_item()
        DataPool().setData("isOpenLogin", self._startEncryptLock)