#!/usr/bin/python
# -*- coding: utf-8 -*-

# @Time    : 2023/7/4 5:07 PM
# @Author  : LTH
# @File    : soundEffect.py

# 配置数据
def configData():
    data = {
        "sheetId": 1,
        "rowId": 1,
        "colId": 1,
    }
    return data


def generateSoundEffectCode(data, row, col):
    rowMax = len(data)
    # colMax  = len(data[0])

    # -- 播放音效[sfx27400024]炫彩玄幻开场动画粒子
    # function M: playEffectsfx27400024()
    #     return self:playSound("sfx27400024")
    # end
    code = ""
    for i in range(row, rowMax):
        if data[i][col] and data[i][col + 1]:
            code += "-- 播放音效[" + data[i][col+1] + "]" + data[i][col] + "\n"
            code += "function M:playEffect" + data[i][col + 1] + "()\n"
            code += "    return self:playSound(\"" + data[i][col + 1] + "\")\n"
            code += "end\n"

    return code


def generateCode(data, row, col):
    try:
        return generateSoundEffectCode(data, row, col)
    except Exception as e:
        # 向上抛出异常
        raise e
