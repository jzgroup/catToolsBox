#!/usr/bin/python
# -*- coding: utf-8 -*-

# @Time    : 2023/6/25 5:04 PM
# @Author  : BOBO
# @File    : jsonToCocos2d.py

import json

from framerwork.classes import *

def jsonToCocos2d(jsonStr):

    # 去掉{} =\
    # jsonStr =
    try:
        data = json.loads(jsonStr)
    except Exception as e:
        Log().error(e)
        Log().error("数据格式错误")
        return "数据格式错误"

    xmlStr = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n"
    xmlStr += "<userDefaultRoot>\n"
    xmlStr += "<USTORE_TABLE_FOR_CLEAR>{\"bb_parent\":["

    for key in data:
        # 使用 partition 方法分割字符串，并取第三个元素
        key = key.partition("_")[2]
        xmlStr += "\"" + key + "\","

    xmlStr = xmlStr[:-1]
    xmlStr += "]}</USTORE_TABLE_FOR_CLEAR>\n"
    for key in data:
        # 使用 partition 方法分割字符串，并取第三个元素
        newKey = key.partition("_")[2]

        xmlStr += "<" + newKey + ">" + data[key] + "</" + newKey + ">\n"
    xmlStr += "</userDefaultRoot>"

    return xmlStr


def dataConversion(jsonStr):
    return jsonToCocos2d(jsonStr)


