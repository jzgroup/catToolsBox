#!/usr/bin/python
# -*- coding: utf-8 -*-

# @Time    : 2023/6/29 8:31 AM
# @Author  : LTH
# @File    : systemTool.py



from framerwork.classes import *

label = G_PROJECT_NAME
path = G_APP_PATH


class SystemControls:
    # 设置开机自启
    @staticmethod
    def add_login_item():
        os.system(f'osascript -e \'tell application "System Events" to make login item at end with properties {{path:"{path}", name:"{label}", hidden:true}}\'')


    @staticmethod
    def remove_login_item():
        Log().info("删除开机自启动")
        code = os.system(f'osascript -e \'tell application "System Events" to delete login item "猫咪工具箱"\'')
        # 是否开机自启动
    @staticmethod
    def is_login_item():
        result = os.popen(f'osascript -e \'tell application "System Events" to get the name of every login item contains "{label}"\'').read()
        Log().info(result)
        if result == '':
            return False
        else:
            return True

    # 获取系统启动时间
    @staticmethod
    def get_system_start_time():
        return os.popen('sysctl -n kern.boottime').read().split(' ')[3].split(',')[0]


