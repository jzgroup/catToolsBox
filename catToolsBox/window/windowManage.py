# #!/usr/bin/env python3
# # -*- coding: utf-8 -*-

#    TODO:   初始化
#    Author: LTH
#    Date:   2023-6-16

import sys

from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QSystemTrayIcon, QMenu, QAction, QMessageBox

from window.toolsBoxWindow import ToolsBoxWindow
from framerwork.classes import *


def compare_versions(version1, version2):
    v1_parts = version1.split('.')
    v2_parts = version2.split('.')

    for i in range(max(len(v1_parts), len(v2_parts))):
        v1_num = int(v1_parts[i]) if i < len(v1_parts) else 0
        v2_num = int(v2_parts[i]) if i < len(v2_parts) else 0

        if v1_num < v2_num:
            return -1
        elif v1_num > v2_num:
            return 1

    return 0


global upDateTip
upDateTip = ""

# 自定义线程类
class UpDtatTipThread(QThread):
    finished = pyqtSignal()  # 自定义信号，用于通知线程执行完毕

    def run(self):
        Log.info("更新线程启动")
        try:
            # 在这里编写线程执行的代码
            HtmlText = Crawler().getHtml(G_UPDATE_DOC_URL)
            tab = Crawler().getTencentHtmlTabData(HtmlText)
            Log.info("更新线程获取到的数据：")
            # 版本号
            version = tab[0][1]
            # 更新内容
            updateContent = tab[1][1]
            Log.info("最新版本：" + version)
            # 当前版本
            VERSION = G_VERSION
            Log.info("当前版本：" + VERSION)
            # Log.info("当前版本：" + DataPool.getData("version"))
            if DataPool().getData('version'):
                if compare_versions(DataPool().getData('version'), G_VERSION) == 1:
                    VERSION = DataPool().getData('version')
            global upDateTip
            upDateTip = ""

            if compare_versions(version, VERSION) == 1:
                DataPool().setData("version", version)
                upDateTip = updateContent
            else:
                Log.info("当前就是最新版本,或者更新信息已经看过了")
            self.finished.emit()  # 发射信号

        # #
        except Exception as e:
            Log.error("更新线程异常" + str(e))


def init():
    # 新建缓存文件夹
    Path().mkdir(G_CACHE_PATH)
    # 初始化日志
    Log().clear()
    Log().info("初始化日志")


# 设置窗口
def setWindow(window):
    global toolBoxWindow
    toolBoxWindow = window

    if DataPool().getData('version') and compare_versions(DataPool().getData('version'), G_VERSION) == 1:
        string = "版本号：" + G_VERSION + "       有新版本可用: " + str(DataPool().getData('version'))
        window.ui.statusbar.showMessage(string)
    else:
        window.ui.statusbar.showMessage("版本号：" + G_VERSION)



# 点击托盘图标
def trayIconActivated():
    if toolBoxWindow.isMinimized() or not toolBoxWindow.isVisible():
        toolBoxWindow.showNormal()
    else:
        toolBoxWindow.showMinimized()

def updateTip():
    # QMessageBox.information(toolBoxWindow, "更新提示", upDateTip, QMessageBox.Yes)
    global upDateTip
    if upDateTip and upDateTip != "":
        #去掉换行符
        upDateTip = upDateTip.replace("\\n", "\n")
        upDateTip += "\n (去仓库拉取最新版本吧)"
        QMessageBox.information(toolBoxWindow, "更新提示", upDateTip, QMessageBox.Yes)



class WindowManage:
    window = None
    _instance = None

    def __init__(self):
        self.window = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(WindowManage, cls).__new__(cls, *args, **kwargs)
        return cls._instance


    def main(self):
        # 更新提示线程
        # 创建线程对象
        thread = UpDtatTipThread()
        # 连接线程的finished信号到槽函数
        thread.finished.connect(updateTip)
        # 启动线程
        thread.start()

        init()
        app = QApplication(sys.argv)
        window = ToolsBoxWindow()
        window.show()
        self.window = window
        # 创建系统托盘图标
        tray_icon = QSystemTrayIcon(QIcon(G_ICON_PATH), app)
        setWindow(self.window)
        # 鼠标点击事件
        tray_icon.activated.connect(lambda: trayIconActivated())
        # 显示系统托盘图标
        tray_icon.show()
        # Log().info("系统启动时间" + SystemControls.get_system_start_time())
        sys.exit(app.exec_())


    # 恢复首页
    def restoreHome(self):
        Log.info("恢复首页")
        self.switchWindow(self, ToolsBoxWindow())

    # 切换window
    def switchWindow(self, window):
        Log().info("切换窗口")
        window.setGeometry(self.window.geometry())
        self.window.close()
        window.show()
        # 设置坐标
        self.window = window
        setWindow(self.window)
