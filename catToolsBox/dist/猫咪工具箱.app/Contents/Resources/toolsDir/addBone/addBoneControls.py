#!/usr/bin/python
# -*- coding: utf-8 -*-
import shutil

# @Time    : 2023/7/14 9:55 AM
# @Author  : LTH
# @File    : addBoneControls.py

from framerwork.classes import *


G_CACHE_PATH = AppData.get_cache_path(AppData)

if not os.path.exists(G_CACHE_PATH):
    os.makedirs(G_CACHE_PATH)

class AddBoneControls:
    def __init__(self, bonePath, excelPath, projectPath, isCompress, window):
        self.bonePath = bonePath
        self.excelPath = excelPath
        self.projectPath = projectPath
        self.isCompress = isCompress
        self.window = window

    def addOneBone(self):
        if os.path.isdir(self.bonePath):
            self.addOneBoneDir(self.bonePath)
            return "添加成功"
        File.remove_dir(G_CACHE_PATH)
        bonex2Path, bonex4Path = self.getOneBonePath(self.bonePath)
        Log.info("bonex2Path: " + bonex2Path)
        Log.info("bonex4Path: " + bonex4Path)

        dirX2Path = os.path.join(G_CACHE_PATH, "x2")
        dirX4Path = os.path.join(G_CACHE_PATH, "x4")

        File.unzip_file(bonex2Path, dirX2Path)
        File.unzip_file(bonex4Path, dirX4Path)
        self.move_file(dirX2Path, True)
        self.move_file(dirX4Path, False)

        return "添加成功"

    def addOneBoneDir(self, dirPath):
        File.remove_dir(G_CACHE_PATH)
        subFiles = Path.list_subFiles(dirPath)
        bonePath = ""
        for file in subFiles:
            if file[-4:] == ".zip":
                bonePath = file
                break
        bonex2Path, bonex4Path = self.getOneBonePath(bonePath)
        Log.info("bonex2Path: " + bonex2Path)
        Log.info("bonex4Path: " + bonex4Path)

        dirX2Path = os.path.join(G_CACHE_PATH, "x2")
        dirX4Path = os.path.join(G_CACHE_PATH, "x4")

        File.unzip_file(bonex2Path, dirX2Path)
        File.unzip_file(bonex4Path, dirX4Path)
        self.move_file(dirX2Path, True)
        self.move_file(dirX4Path, False)


    def addMoreBone(self):
        subDirs = Path.list_subDirs(self.bonePath)
        self.addOneBoneDir(subDirs[0])
        self.window.progressBarValue = 10

        addProgressInit = 10/len(subDirs)
        unzipPathTab = []
        for name in subDirs:
            subFiles = Path.list_subFiles(name)
            addProgress = addProgressInit/len(subFiles)
            for file in subFiles:
                self.window.progressBarValue += addProgress
                if file[-4:] == ".zip" and ("x2" in file or "X2" in file):
                    unzipPath = os.path.join(G_CACHE_PATH, File.getFileName(file))
                    File.unzip_file(file, unzipPath)
                    unzipPathTab.append(unzipPath)
                    break
        self.window.progressBarValue = 20


        Log.info("unzipPathTab: " + str(unzipPathTab))
        xmlPathTab = []
        addProgressInit = 10/len(unzipPathTab)
        for unzipPath in unzipPathTab:
            subFiles = Path.list_subFiles(unzipPath)
            addProgress = addProgressInit/len(subFiles)
            for file in subFiles:
                self.window.progressBarValue += addProgress
                if file[-4:] == ".xml":
                    xmlPathTab.append(file)
                    break
        Log.info("xmlPathTab: " + str(xmlPathTab))
        self.window.progressBarValue = 30

        mainXml = None
        addProgressInit = 20/len(xmlPathTab)
        for xmlPath in xmlPathTab:
            if mainXml is None:
                mainXml = xmlPath
            else:
                self.addXml(mainXml, xmlPath)
            self.window.progressBarValue += addProgressInit
        self.window.progressBarValue = 50


        # 读取xml文件
        tree = ET.parse(mainXml)  # 类ElementTree
        root = tree.getroot()  # 这时得到的root是一个指向Element的对象

        animation = []

        for node in root.iter("animation"):
            if node.attrib.get("name") == "mao2":
                for child in node.iter("mov"):
                    if animation.count(child.attrib.get("name")) == 0:
                        animation.append(child.attrib.get("name"))
                    else:
                        Log.error("animation name repeat: " + child.attrib.get("name"))
                        try:
                            # 删除
                            self.del_xmlNode(root, [child.attrib.get("name")])
                        except Exception as e:
                            Log.error("del_xmlNode error: " + str(e))

        #
        tree = ET.ElementTree(root)
        tree.write(mainXml)
        excel = Excel()


        for data in self.colData(excel.open(self.excelPath)):
            dataTab = []
            for v in data:
                if v in dataTab:
                    return data[1] + "中有重复动作:" + v
                elif v != "":  # 在Python中使用 != 而不是 ~=
                    dataTab.append(v)

        try:
            self.splitXml(mainXml)
        except Exception as e:
            Log.error("splitXml error: " + str(e))
            return "表格格式错误"

        return "添加成功"


    # 获取x2 x4的路径(防刁民)
    def getOneBonePath(self, path):
        bonex2Path = ""
        bonex4Path = ""
        if 'x2' in path:
            bonex2Path = path
            bonex4Path = path.replace('x2', 'x4')
        elif 'x4' in path:
            bonex2Path = path.replace('x4', 'x2')
            bonex4Path = path
        elif 'X2' in path:
            bonex2Path = path
            bonex4Path = path.replace('X2', 'X4')
        elif 'X4' in path:
            bonex2Path = path.replace('X4', 'X2')
            bonex4Path = path
        return bonex2Path, bonex4Path

    # 移动文件
    def move_file(self, dest_path, isX2):
        if isX2:
            imgPath = "x2"
        else:
            imgPath = "x4"
        projectPath = self.projectPath
        for filename in os.listdir(dest_path):
            suffix = filename[-4:]
            if suffix == 'list' or suffix == '.png':
                if os.path.isfile(projectPath + '/res/img/' + imgPath + '/bone/' + filename):
                    os.remove(projectPath + '/res/img/' + imgPath + '/bone/' + filename)
                shutil.move(dest_path + '/' + filename, projectPath + '/res/img/' + imgPath + '/bone')
            elif suffix == '.xml' and isX2:
                if os.path.isfile(projectPath + '/res/img/common/bone/' + filename):
                    os.remove(projectPath + '/res/img/common/bone/' + filename)
                shutil.move(dest_path + '/' + filename, projectPath + '/res/img/common/bone')

    def addXml(self, path, path2):
        # 读取xml文件
        tree1 = ET.parse(path)  # 类ElementTree
        root1 = tree1.getroot()  # 这时得到的root是一个指向Element的对象

        # 读取xml文件
        tree2 = ET.parse(path2)  # 类ElementTree
        root2 = tree2.getroot()  # 这时得到的root是一个指向Element的对象
        for node in root1.iter("animation"):
            if node.attrib.get("name") == root1.attrib.get("name"):
                # print(node.attrib.get("name"))
                for node2 in root2.iter("animation"):
                    if node2.attrib.get("name") == root2.attrib.get("name"):
                        for child in node2.iter("mov"):
                            node.append(child)


        # 保存到原来位置
        tree1.write(path)

    # 拆分XML
    def splitXml(self, xmlPath):

        # 读取xml文件
        tree = ET.parse(xmlPath)  # 类ElementTree
        root = tree.getroot()  # 这时得到的root是一个指向Element的对象
        allAniName = []
        excel = Excel()

        excelTab = self.colData(excel.open(self.excelPath))

        addProgressinit = 50/len(excelTab)
        for item in excelTab:
            addProgress = addProgressinit/len(item)
            if not self.is_all_chinese(item[1]):
                name = item[1]
                del (item[1])
                allAniName = allAniName + item
                self.createBoneXml(root, item, name)
                self.window.progressBarValue += addProgress

        self.window.progressBarValue = 100
        allAniName = self.deleteDuplicatedElementFromList(allAniName)
        # # 删除主文件的动作信息
        self.del_xmlNode(root, allAniName)

        #
        tree = ET.ElementTree(root)
        tree.write(self.projectPath + "/res/img/common/bone/" + os.path.basename(xmlPath))


    #检验是否有中文字符
    def is_all_chinese(self, strs):
        for _char in strs:
            if '\u4e00' <= _char <= '\u9fa5':
                return True
        return False

    # 删除节点
    def del_xmlNode(self, root, allAniName):
        for node in root.iter("animation"):
            for child in list(node.iter("mov")):
                for aniName in allAniName:
                    if child.attrib.get("name") == aniName:
                        node.remove(child)
                        allAniName.remove(aniName)
                        continue

    def createBoneXml(self, oldRoot, aniItem, name):
        projectPath = self.projectPath
        # 获取下骨骼名(防止多骨骼文件)
        boneName = oldRoot.attrib.get("name")

        # 添加基础属性
        root = ET.Element('skeleton', oldRoot.attrib)

        ET.SubElement(root, 'armatures')
        # 重要的动作属性
        animations = ET.SubElement(root, 'animations')
        animation = ET.SubElement(animations, 'animation', {"name": boneName})

        # Element.append(childElement)
        ET.SubElement(root, 'TextureAtlas')

        # 获取动作信息
        for neighbor in oldRoot.iter("mov"):
            if len(aniItem) == 0:
                break
            for aniName in aniItem:
                if neighbor.attrib.get("name") == aniName:
                    animation.append(neighbor)
                    aniItem.remove(aniName)
                    continue

        Xml.prettyXml(root, '\t', '\n')

        tree = ET.ElementTree(root)
        tree.write(projectPath + "/res/img/common/bone" + "/" + name + ".xml")

    # 去掉重复元素
    def deleteDuplicatedElementFromList(self, listA):
        # 重复的动作有那里
        animation = []
        for item in listA:
            if item in animation:
                Log.error(item)
            elif item != "":  # 在Python中使用 != 而不是 ~=
                animation.append(item)
        return sorted(set(listA), key=listA.index)

    # 横向改变数据
    def colData(self, excelData):
        dataTab = []
        for j in range(len(excelData[0])):
            data = []
            for i in range(len(excelData)):
                if excelData[i][j] is not None:
                    data.append(excelData[i][j])
                else:
                    break
            if len(data) > 0:
                dataTab.append(data)

        return dataTab
