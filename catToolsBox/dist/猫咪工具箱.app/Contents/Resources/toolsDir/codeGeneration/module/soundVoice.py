#!/usr/bin/python
# -*- coding: utf-8 -*-

# @Time    : 2023/7/4 5:07 PM
# @Author  : LTH
# @File    : soundEffect.py

# 配置数据
def configData():
    data = {
        "sheetId": 0,
        "rowId": 2,
        "colId": 3,
    }
    return data


def generateSoundVoiceCode(data, row, col):
    rowMax = len(data)
    # colMax  = len(data[0])
    # -- 播放配音[v124369]qq的蛋糕帽，要装饰些什么呢
    # functionM: playEffectv124369()
    #     return self:playSound("v124369")
    # end

    code = ""
    for i in range(row, rowMax):
        if data[i][col] and data[i][col + 1]:
            code += "-- 播放配音[" + data[i][col] + "]" + data[i][col + 1] + "\n"
            code += "function M:playEffect" + data[i][col] + "()\n"
            code += "    return self:playSound(\"" + data[i][col] + "\")\n"
            code += "end\n"

    return code


def generateCode(data, row, col):
    try:
        return generateSoundVoiceCode(data, row, col)
    except Exception as e:
        # 向上抛出异常
        raise e

