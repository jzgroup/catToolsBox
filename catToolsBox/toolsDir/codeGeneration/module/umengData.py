#!/usr/bin/python
# -*- coding: utf-8 -*-

# @Time    : 2023/7/4 5:07 PM
# @Author  : LTH
# @File    : soundEffect.py

# 配置数据
def configData():
    data = {
        "sheetId": 0,
        "rowId": 1,
        "colId": 2,
    }
    return data


def generateUmengDataCode(data, row, col):
    rowMax = len(data)
    # colMax  = len(data[0])

    # -- 观察室道具使用
    # function M.recordqmmmsj037(name)
    #     NV.recordEvent("qmmmsj037", name)
    # end
    code = ""
    for i in range(row, rowMax):
        if data[i][col] and data[i][col + 1]:
            try:
                second = str(data[i][col + 2])
                third = str(data[i][col + 3])
            except:
                second = ""
                third = ""
            secondStr = ["", "", ""]
            thirdStr = ["", "", ""]
            if third != "" and third != "无"and third != "None":
                secondStr[0] = "index1"
                second = second.split('、')
                secondStr[1] = "local name1 = {"
                for key, value in enumerate(second):
                    secondStr[1] = secondStr[1] + "\"" + value + "\""
                    if key != len(second) - 1:
                        secondStr[1] = secondStr[1] + ", "
                secondStr[1] = secondStr[1] + "}"
                secondStr[2] = ", name1[index1]"
                thirdStr[0] = ", index2"
                third = third.split('、')
                thirdStr[1] = "local name2 = {"
                for key, value in enumerate(third):
                    thirdStr[1] = thirdStr[1] + "\"" + value + "\""
                    if key != len(third) - 1:
                        thirdStr[1] = thirdStr[1] + ", "
                thirdStr[1] = thirdStr[1] + "}"
                thirdStr[2] = ", name2[index2]"
            elif second != "" and second != "无" and second != "None":
                secondStr[0] = "index"
                second = second.split('、')
                secondStr[1] = "local name = {"
                for key, value in enumerate(second):
                    secondStr[1] = secondStr[1] + "\"" + value + "\""
                    if key != len(second) - 1:
                        secondStr[1] = secondStr[1] + ", "
                secondStr[1] = secondStr[1] + "}"
                secondStr[2] = ", name[index]"
            numcode = data[i][col]

            code += "--[经分]" + numcode + data[i][col + 1] + "\n"
            code += "function M.record" + numcode + "(" + secondStr[0] + thirdStr[0] + ")" + "\n"
            if secondStr[1] != "":
                code += "\t" + secondStr[1] + "\n"
            if thirdStr[1] != "":
                code += "\t" + thirdStr[1] + "\n"
            code += "\tNV.recordEvent(\"" + numcode + "\"" + secondStr[2] + thirdStr[
                2] + ")" + "\n" + "end" + "\n"
            code += "\n"

    return code


def generateCode(data, row, col):
    try:
        return generateUmengDataCode(data, row, col)
    except Exception as e:
        # 向上抛出异常
        raise e
