#!/usr/bin/python
# -*- coding: utf-8 -*-

# @Time    : 2024/2/19 15:41
# @Author  : LTH
# @File    : RunLua.py

#python调用lua脚本
from lupa import LuaRuntime


if __name__ == '__main__':
    # 创建 Lua 运行环境
    lua = LuaRuntime(unpack_returned_tuples=True)

    # # 执行 Lua 脚本文件
    lua.execute('dofile("script.lua")')


    # 获取 Lua 全局环境中的 greet 函数
    greet = lua.globals()['greet']

    # 调用 Lua 函数
    # greet('Python')

    # 获取 Lua 全局环境中的 greet 函数的返回值
    result = greet('Python')




