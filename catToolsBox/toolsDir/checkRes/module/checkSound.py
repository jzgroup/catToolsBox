#!/usr/bin/python
# -*- coding: utf-8 -*-

# @Time    : 2023/7/13 3:58 PM
# @Author  : LTH
# @File    : checkSound.py


from framerwork.classes import *

# 文件名
def getFileName(path):
    return os.path.splitext(os.path.basename(path))[0]


# # 获取音频文件集合
def getEffectTab(dir_name):
    effectTab = {}
    dir_name = dir_name + '/res/snd/effect'
    for dirpath, dirnames, filenames in os.walk(dir_name):
        for f in filenames:
            suffix = f[-4:]
            if suffix != '.mp3':
                continue
            effectTab[getFileName(f)] = 0

    return effectTab


class CheckSound:
    def __init__(self, projectPath, cachePath, windows):
        # 项目路径
        self.projectPath = projectPath
        # 缓存路径
        self.cachePath = os.path.join(cachePath, 'checkSound.txt')
        # 进度条
        self.windows = windows

    def checkSound(self):
        # 缓存路径
        if os.path.exists(self.cachePath):
            os.remove(self.cachePath)
        Log().info("检查音频")
        effectTab = getEffectTab(self.projectPath)
        filenames = Path.list_all_suffix(self.projectPath, '.lua')
        length = len(filenames)
        count = 0
        for file in filenames:
            src_path = file

            count = count + 1
            self.windows.checkSoundProgressBarValue = count / length * 100
            # 文件名
            fileName = getFileName(file)
            if fileName == 'SoundEffect':
                continue
            f = open(src_path, 'r', encoding='utf-8')
            # #读出该文件所有的行
            alllines = f.readlines()
            for eachline in alllines:
                # 去掉每行头尾空白
                eachline = eachline.strip()
                # 注释的行不读
                if eachline.startswith("--"):
                    continue
                # 代码中调用音频
                for effect in effectTab:
                    if effect in eachline:
                        effectTab[effect] = effectTab[effect] + 1
            f.close()
        Log().info("检查音频完成")
        # 续写
        f = open(self.cachePath, 'a', encoding='utf-8')
        for effect in effectTab:
            if effectTab[effect] == 0:
                f.write(effect + '\n')
        f.close()

    def openCheckSoundTxt(self):
        if not os.path.exists(self.cachePath):
            return "无无用音频"
        os.system('open ' + self.cachePath)

    # 删除无用音频
    def deleteUnusedSound(self):
        if not os.path.exists(self.cachePath):
            return "无无用音频"
        f = open(self.cachePath, 'r', encoding='utf-8')
        # #读出该文件所有的行
        alllines = f.readlines()
        for eachline in alllines:
            if eachline == '':
                continue
            filePath =  os.path.join(self.projectPath, 'res/snd/effect/' + eachline.strip() + ".mp3")
            try:
                os.remove(filePath)
            except:
                Log().error("删除无用音频失败：" + filePath)
        f.close()
        return "删除无用音频成功"

    def openCheckVoiceTxt(self):
        pass





