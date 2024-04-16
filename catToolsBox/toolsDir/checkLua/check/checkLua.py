#!/usr/bin/python
# -*- coding: utf-8 -*-
import platform
# @Time    : 2024/3/22 15:46
# @Author  : LTH
# @File    : checkLua.py
import subprocess
import re
import json
from framerwork.classes import *


G_CACHE_PATH = AppData.get_cache_path(AppData)



# 当前脚本路径
script_dir = os.path.dirname(os.path.abspath(__file__))


# 项目路径
project_path = ""
frameworkVariableArrFilePath = os.path.join(script_dir, "frameworkVariableArr.json")
customVariableArrFilePath = os.path.join(script_dir, "customVariableArr.json")
variableArrPath = os.path.join(G_CACHE_PATH, "variableArr.json")
errorLogPath = os.path.join(G_CACHE_PATH, "error.txt")

# 读取json文件
def readJson(file_path):
    if not os.path.exists(variableArrPath):
        return []
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

# 项目路径下的所有lua文件
def getLuaFiles(project_path):
    luaFiles = []
    for root, dirs, files in os.walk(project_path):
        for file in files:
            if file.endswith(".lua"):
                luaFiles.append(os.path.join(root, file))
    return luaFiles

# 移除字符串中的 ANSI 颜色代码
def remove_ansi_color_codes(text):
    # ANSI 转义序列的正则表达式
    ansi_escape_sequence_re = re.compile(r'\033\[[0-9;]*m')
    return ansi_escape_sequence_re.sub('', text)

# 字符串是否全部大写
def isAllUpper(str):
    return str.isupper()


luaPath = os.path.join(script_dir, "mac", "lua")


# 检查操作系统架构
arch = platform.machine()

Log().info("系统架构")
def get_mac_cpu_type():
    if platform.system() != 'Darwin':
        raise EnvironmentError("This function is designed to be used on macOS.")

    # 使用uname命令直接从系统获取CPU类型
    cpu_arch = os.popen('uname -m').read().strip()

    # 使用sysctl检查是否在Rosetta下运行
    is_translated = os.popen('sysctl -n sysctl.proc_translated').read().strip()

    if cpu_arch == 'x86_64':
        if is_translated == '1':
            Log().info("Apple M1 under Rosetta 2")
            # return 'Apple M1 under Rosetta 2'
            return 1
        else:
            Log().info("Intel")
            # return 'Intel'
            return 2
    elif cpu_arch == 'arm64':
        Log().info("Apple M1")
        # return 'Apple M1'
        return 1
    else:
        Log().info(f'Unknown architecture: {cpu_arch}')
        # return f'Unknown architecture: {cpu_arch}'
        return 3

cpu_type = get_mac_cpu_type()
if cpu_type == 2:
    luaPath = os.path.join(script_dir, "x86", "lua")

luacheckPath = os.path.join(script_dir, "luacheck", "bin", "luacheck.lua")
luacheckLibPath = os.path.join(script_dir, "luacheck", "src")  # Luacheck 库的路径
argparsePath = os.path.join(script_dir, "argparse", "src")
lfsPath = os.path.join(script_dir, "lfs", "arm64")
if cpu_type == 2:
    lfsPath = os.path.join(script_dir, "lfs", "x86")

def run_luacheck(file_path):
     #添加argparsePath,luacheckLibPath到package.path
    result = subprocess.run([luaPath,
                    '-e', 'package.path = package.path .. ";' + argparsePath + '/?.lua"',
                    '-e', 'package.path = package.path .. ";' + luacheckLibPath + '/?.lua"',
                    '-e', 'package.path = package.path .. ";' + luacheckLibPath + '/?/init.lua"',
                    '-e', 'package.cpath = package.cpath .. ";' + lfsPath + '/?.so"',
                    luacheckPath, file_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return result.stdout, result.stderr

def checkLua(luaPath):
    output, error = run_luacheck(luaPath)
    if error:
        Log().error("Error: " + error.decode('utf-8'))
    else:
        # 将输出按行分割
        lines = output.decode('utf-8').splitlines()
        # 检查每一行，打印匹配的警告信息
        for line in lines:
            # 字符串包含accessing undefined variable
            if "accessing undefined variable" in line:
                #根据空格分割字符串
                words = line.split(" ")
                #获取变量名最后一个单词
                variable = words[-1].strip()
                variable = remove_ansi_color_codes(variable)

                #如果变量名不在数组中，添加到数组
                if variable not in customVariableArr and variable not in frameworkVariableArr and variable :
                    if isFilterUpper and isAllUpper(variable):
                        continue
                    if variable not in variableArr:
                        variableArr.append(variable)
                    string = "文件：" + words[4] + "  变量：" + variable
                    Log().info(string)

                    with open(errorLogPath, "a", encoding='utf-8') as f:
                        string += "\n"
                        f.write(string)



# 将 JSON 数组写入文件，每五个元素一行
def dump_json_array_with_line_breaks(data, filepath, line_break_every=5):
    # 打开文件准备写入
    with open(filepath, "w") as f:
        # 写入 JSON 数组开始的中括号
        f.write("[\n")
        # try:
        # 按照指定的元素数量插入逗号和换行符
        for i in range(0, len(data), line_break_every):
            # 获取当前行的片段
            chunk = data[i:i+line_break_every]
            # 转换当前片段为JSON格式（不在这个数组片段的末尾添加逗号）
            json_chunk = json.dumps(chunk)[1:-1].rstrip(',')
            # 写入转换后的JSON数组片段
            if i + line_break_every < len(data):
                # 如果不是最后一行，末尾添加逗号和换行符
                f.write("    " + json_chunk + ",\n")
            else:
                # 最后一行，末尾添加换行符
                f.write("    " + json_chunk + "\n")
        f.write("]")


def set_window(window):
    global win
    win = window

def set_frameworkVariableArr(arr):
    global frameworkVariableArr
    frameworkVariableArr = arr

def set_customVariableArr(arr):
    global customVariableArr
    customVariableArr = arr

def set_variableArr(arr):
    global variableArr
    variableArr = arr

# 是否过滤大写变量
isFilterUpper = False
def set_isFilterUpper(isFilterUp):
    global isFilterUpper
    isFilterUpper = isFilterUp

class CheckLua:
    def __init__(self, window, project_path, frameworkVariableArrPath, customVariableArrPath, isFilterUp):
        self.project_path = project_path
        self.frameworkVariableArrPath = frameworkVariableArrPath
        self.customVariableArrPath = customVariableArrPath
        self.window = window
        set_isFilterUpper(isFilterUp)

    def run(self):
        #删除 variableArrPath 文件
        if os.path.exists(variableArrPath):
            os.remove(variableArrPath)

        # 没有variableArrPath文件，创建一个
        if not os.path.exists(variableArrPath):
            with open(variableArrPath, "w") as f:
                json.dump([], f)

        # 清空errorLogPath文件
        if os.path.exists(errorLogPath):
            os.remove(errorLogPath)

        # 没有errorLogPath文件，创建一个
        if not os.path.exists(errorLogPath):
            with open(errorLogPath, "w") as f:
                f.write("")
                set_window(self.window)

        frameworkVariableArrFilePath = self.frameworkVariableArrPath
        customVariableArrFilePath = self.customVariableArrPath
        project_path = self.project_path

        frameworkVariableArr = []
        try:
            Log().info(frameworkVariableArrFilePath)
              # 读取文件
            frameworkVariableArr = readJson(frameworkVariableArrFilePath)
        except:
            Log().error("json文件错误,读取frameworkVariableArr文件失败")

        set_frameworkVariableArr(frameworkVariableArr)
        customVariableArr = []


        try:
            Log().info(customVariableArrFilePath)
            # 读取文件
            customVariableArr = readJson(customVariableArrFilePath)
        except:
            Log().error("json文件错误,读取customVariableArr文件失败")

        set_customVariableArr(customVariableArr)

        # 自定义变量数组
        set_variableArr([])
        Log().info(project_path)
        # project_path 如果是一个文件夹，获取文件夹下所有lua文件
        if os.path.isdir(project_path):
            Log().info(" # 获取所有lua文件")
            luaFiles = getLuaFiles(project_path)
            arrlen = len(luaFiles)
            i = 0
            for luaFile in luaFiles:
                checkLua(luaFile)
                win.progressBarValue = i/arrlen *100
                i = i + 1
        else:
            checkLua(project_path)




        dump_json_array_with_line_breaks(variableArr, variableArrPath)
        Log().info("检查完成")