#!/usr/bin/python
# -*- coding: utf-8 -*-
import importlib

# @Time    : 2023/7/4 4:26 PM
# @Author  : LTH
# @File    : codeGenerationWindow.py


from toolsFramerwork.windowBase import windowBase
from PyQt5.QtWidgets import QMessageBox

from framerwork.classes import *
from toolsDir.codeGeneration.codeGeneration import Ui_mainWindow


# 获取当前脚本文件的绝对路径
script_path = os.path.abspath(__file__)
G_CACHE_PATH = AppData.get_cache_path(AppData)

if not os.path.exists(G_CACHE_PATH):
    os.makedirs(G_CACHE_PATH)

module = [
    {
        "name": "音效",
        "path": os.path.join(os.path.dirname(script_path), "module", 'soundEffect.py')
    },
    {
        "name": "台词",
        "path": os.path.join(os.path.dirname(script_path), "module", 'soundVoice.py')
    },
    {
        "name": "埋点经分",
        "path": os.path.join(os.path.dirname(script_path), "module", 'umengData.py')
    },
    {
        "name": "骨骼换装",
        "path": os.path.join(os.path.dirname(script_path), "module", 'decorate.py')
    }
]


class Window(windowBase):
    def __init__(self):
        self._btnLock = False
        Log().info("代码生成")
        super().__init__()
        self.ui = Ui_mainWindow()
        self.ui.setupUi(self)

        self.addTouch()
        self.addItems()
        self.initData()
        self.addDrop()



    def initData(self):
        path = DataPool().getData('excelPath')
        if path:
            self.ui.lineEdit.setText(path)
            # 有埋点关键字
            if '数据采集' in path or '埋点' in path or '经分' in path:
                self.ui.comboBox.setCurrentIndex(2)
            elif '音效' in path:
                self.ui.comboBox.setCurrentIndex(0)
            elif '换装' in path:
                self.ui.comboBox.setCurrentIndex(3)
            else:
                self.ui.comboBox.setCurrentIndex(1)

        self.ui.textEdit.textChanged.connect(self.textEditChanged)

    # 添加触控
    def addTouch(self):
        self.ui.backHome.clicked.connect(self.homeButtonClicked)
        self.ui.comboBox.currentIndexChanged.connect(self.comboBoxIndexChanged)
        self.ui.startGeneration.clicked.connect(self.startGenerationClicked)
        self.ui.openCodeFile.clicked.connect(self.openCodeFileClicked)

    def addItems(self):
        for item in module:
            self.ui.comboBox.addItem(item["name"], item["path"])

    # 下拉框选择事件
    def comboBoxIndexChanged(self):
        Log().info("下拉框选择事件")
        # 选择了
        Log().info(self.ui.comboBox.currentText())
        path = self.ui.comboBox.currentData()
        # 使用 Python 的 `importlib` 模块动态导入模块
        spec = importlib.util.spec_from_file_location("module.name", path)
        foo = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(foo)
        self.modle = foo
        # textEditm没有数据
        if self.ui.textEdit.toPlainText() == "":
            self.setNumberData(foo.configData())
        else:
            Log.info("富文本有数据")
            data = {
                "sheetId": 0,
                "rowId": 0,
                "colId": 0,
            }
            self.setNumberData(data)

    def textEditChanged(self):
        # 富文本有数据
        if self.ui.textEdit.toPlainText() != "":
            Log.info("富文本有数据")
            data = {
                "sheetId": 0,
                "rowId": 0,
                "colId": 0,
            }
            self.setNumberData(data)

    # 设置数字框数据
    def setNumberData(self, data):
        self.ui.spinBoxExecl.setValue(data["sheetId"])
        self.ui.spinBoxRow.setValue(data["rowId"])
        self.ui.spinBoxCol.setValue(data["colId"])


    # 添加拖拽
    def addDrop(self):
        # # 可以使用户拖放文件夹以添加项目路径
        self.ui.lineEdit.setAcceptDrops(True)
        self.ui.lineEdit.dragEnterEvent = self.dragEnterEvent
        self.ui.lineEdit.dropEvent = self.dropEvent

    def startGenerationClicked(self):
        if self.ui.textEdit.toPlainText() == "" and self.ui.lineEdit.text() == "":
            Log().info("没有数据")
            QMessageBox.information(self, "提示", "没有数据", QMessageBox.Yes)
            return
        newData = ""
        if self.ui.textEdit.toPlainText() == "":
            self.excel = Excel()
            data = self.excel.open(self.ui.lineEdit.text(), self.ui.spinBoxExecl.value())
            try:
                newData = self.modle.generateCode(data, self.ui.spinBoxRow.value(), self.ui.spinBoxCol.value())
            except Exception as e:
                QMessageBox.information(self, "提示", "发生错误，文件是否存在，格式是否正确", QMessageBox.Yes)
                return
        else:
            HtmlText = self.ui.textEdit.toHtml()
            try:
                table_data = Crawler().getHtmlTabData(HtmlText)
                newData = self.modle.generateCode(table_data, self.ui.spinBoxRow.value(), self.ui.spinBoxCol.value())
            except Exception as e:
                Log().error("不符合的格式")
                QMessageBox.information(self, "提示", "不符合的格式", QMessageBox.Yes)
                return
        # 续写
        path = os.path.join(G_CACHE_PATH, self.ui.comboBox.currentText() + "code.txt")
        f = open(path, 'w', encoding='utf-8')
        f.write(newData)
        f.close()
        os.system("open " + path)



    def openCodeFileClicked(self):
        path = os.path.join(G_CACHE_PATH, self.ui.comboBox.currentText() + "code.txt")
        os.system("open " + path)


    def dropEvent(self, event):
        if event.mimeData().hasUrls() and len(event.mimeData().urls()) == 1:
            # 如果拖动的 MIME 数据中包含 URI，则使用第一个 URI 设置进程路径
            url = event.mimeData().urls()[0]
            path = url.toLocalFile()
            if path.endswith('.xlsx') or path.endswith('.xls'):
                self.ui.lineEdit.setText(path)
                if path:
                    DataPool().setData('excelPath', path)

                # 有埋点关键字
                if '数据采集' in path or '埋点' in path or '经分' in path:
                    self.ui.comboBox.setCurrentIndex(2)
                elif '音效' in path:
                    self.ui.comboBox.setCurrentIndex(0)
                elif '换装' in path:
                    self.ui.comboBox.setCurrentIndex(3)
                else:
                    self.ui.comboBox.setCurrentIndex(1)

            else:
                Log().info("不支持的文件类型")
                QMessageBox.information(self, "提示", "不支持的文件类型,请拖入excel文件", QMessageBox.Yes)