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
        "colId": 1,
    }
    return data


def generateDecorateCode(data, row, col):
    rowMax = len(data)
    colMax  = len(data[0])

    # local changeItem = {
    #     {
    #         b = "mao2_tou", f1 = "mao2_tou", f2 = "mao2_pf_tou01", f3 = "mao2_pf_tou02", f4 = "mao1_pf_tou03", f5 = "mao1_pf_tou04", f6 = "mao1_pf_tou05", f7 = "mao1_pf_tou06", f8 = "mao1_pf_tou07", f9 = "mao3_pf_tou08", f10 = "mao3_pf_tou09", f11 = "mao3_pf_tou10", f12 = "mao3_pf_tou11", f13 = "mao3_pf_tou12", f14 = "mao3_pf_tou13", f15 = "mao3_pf_tou14", f16 = "mao2_pf_tou15", f17 = "mao1_pf_tou16", f18 = "mao1_pf_tou17", f19 = "mao3_pf_tou18", f20 = "mao3_pf_tou19", f21 = "mao2_pf_tou20", f22 = "mao2_pf_tou21", f23 = "mao2_pf_tou22", f24 = "mao2_pf_tou23", f25 = "mao2_pf_tou24"},
    # {b = "mao2_st", f1 = "mao2_st", f2 = "mao2_pf_st01", f3 = "mao2_pf_st02", f4 = "mao1_pf_st03", f5 = "mao1_pf_st04", f6 = "mao1_pf_st05", f7 = "mao1_pf_st06", f8 = "mao1_pf_st07", f9 = "mao3_pf_st08", f10 = "mao3_pf_st09", f11 = "mao3_pf_st10", f12 = "mao3_pf_st11", f13 = "mao3_pf_st12", f14 = "mao3_pf_st13", f15 = "mao3_pf_st14", f16 = "mao2_pf_st15", f17 = "mao1_pf_st16", f18 = "mao1_pf_st17", f19 = "mao3_pf_st18", f20 = "mao3_pf_st19", f21 = "mao2_pf_st20", f22 = "mao2_pf_st21", f23 = "mao2_pf_st22", f24 = "mao2_pf_st23", f25 = "mao2_pf_st24"},
    # }}
    code = "local changeItem = {\n"
    for i in range(row, rowMax):
        if data[i][col] and data[i][col + 1]:
            code += "{b = \"" + data[i][col] + "\", "
            for j in range(col + 1, colMax):
                if data[i][j]:
                    string = data[i][j]
                    if '隐藏' in string or '无' in string:
                        string = ""
                    code += "f" + str(j - col) + " = \"" + string + "\", "
            code += "},\n"

    code += "}\n"

    return code


def generateCode(data, row, col):
    try:
        return generateDecorateCode(data, row, col)
    except Exception as e:
        # 向上抛出异常
        raise e

