#!/usr/bin/python
# -*- coding: utf-8 -*-

# @Time    : 2023/7/13 3:58 PM
# @Author  : LTH
# @File    : checkVoice.py


from framerwork.classes import *

# 文件名
def getFileName(path):
    return os.path.splitext(os.path.basename(path))[0]


# # 获取台词文件集合
def getEffectTab(dir_name):
    effectTab = {}
    dir_name = os.path.join(dir_name, 'res/i18n/zh/snd/effect/')

    for dirpath, dirnames, filenames in os.walk(dir_name):
        for f in filenames:
            suffix = f[-4:]
            if suffix != '.mp3':
                continue
            effectTab[getFileName(f)] = 0

    return effectTab


class CheckVoice:
    def __init__(self, projectPath, cachePath, windows):
        # 项目路径
        self.projectPath = projectPath
        # 缓存路径
        self.cachePath = os.path.join(cachePath, 'checkVoice.txt')
        # 进度条
        self.windows = windows

    def checkVoice(self):
        # 缓存路径
        if os.path.exists(self.cachePath):
            os.remove(self.cachePath)
        Log().info("检查台词")
        effectTab = getEffectTab(self.projectPath)
        filenames = Path.list_all_suffix(self.projectPath, '.lua')
        length = len(filenames)
        count = 0
        for file in filenames:

            src_path = file

            count = count + 1
            self.windows.checkVoiceProgressBarValue = count / length * 100
            # 文件名
            fileName = getFileName(file)
            if fileName == 'SoundVoice':
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
                # 代码中调用台词
                for effect in effectTab:
                    if effect in eachline:
                        effectTab[effect] = effectTab[effect] + 1
            f.close()

        # 续写
        f = open(self.cachePath, 'a', encoding='utf-8')
        for effect in effectTab:
            if effectTab[effect] == 0:
                f.write(effect + '\n')
        f.close()

    def openCheckVoiceTxt(self):
        if not os.path.exists(self.cachePath):
            return "无无用台词"
        os.system('open ' + self.cachePath)

    # 删除无用台词
    def deleteUnusedSound(self):
        if not os.path.exists(self.cachePath):
            return "无无用台词"
        f = open(self.cachePath, 'r', encoding='utf-8')
        # #读出该文件所有的行
        alllines = f.readlines()
        for eachline in alllines:
            if eachline == '':
                continue
            list_subDirs = Path.list_subDirs(os.path.join(self.projectPath, 'res/i18n/'))
            # filePath = os.path.join(self.projectPath, 'res/snd/effect/' + eachline.strip() + ".mp3")
            for dir in list_subDirs:
                filePath = os.path.join(dir, 'snd/effect/' + eachline.strip() + ".mp3")
                if os.path.exists(filePath):
                    try:
                        os.remove(filePath)
                    except:
                        Log().error("删除无用台词失败：" + filePath)
                else:
                    Log().error("无台词：" + filePath)
            f.close()
        return "删除无用台词成功"





