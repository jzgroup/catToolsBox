#!/usr/bin/python
# -*- coding: utf-8 -*-

# @Time    : 2023/9/8 3:58 PM
# @Author  : LTH
# @File    : CheckInternationalization.py


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




if __name__ == '__main__':
    projectPath = "/Users/babybus/Documents/project/com.sinyee.babybus.care"
    xlsxPath = '/Users/babybus/Desktop/【情商】13《照顾小宝宝》-外配音频表（国际化）.xlsx'
    Log().info("检查台词")
    effectTab = getEffectTab(projectPath)
    filenames = Path.list_all_suffix(projectPath, '.lua')
    length = len(filenames)
    count = 0
    for file in filenames:

        src_path = file

        count = count + 1
        # 文件名
        fileName = getFileName(file)
        if fileName == 'SoundVoice':
            continue
        if fileName == 'supplement':
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

    for effect in effectTab:
        if effectTab[effect] == 0:
            Log().error("检查台词: " + effect + " 未被使用")
    excel = Excel()
    data = excel.open(xlsxPath)
    effectExcelTab = []

    # 范围
    radius = [1, len(data)]
    index = 1
    for row in data:
        if row[2] and row[2] != '音频编码' and index <= radius[1] and index >= radius[0]:
            effectExcelTab.append(row[2])
        index = index + 1
        if index > radius[1]:
            break
    # print(effectExcelTab)


    for effect in effectTab:
        if effect not in effectExcelTab:
            Log().error("检查台词: " + effect + " 未在表格中")
    
    for effect in effectExcelTab:
        strEffect = str(effect)
        if strEffect not in effectTab :
            Log().error("检查台词: " + strEffect + " 未在代码中")
        # elif effectTab[effect] == 0:
        #     Log().error("检查台词: " + strEffect + " 未被使用")
    

    Log().info("检查台词完成")

