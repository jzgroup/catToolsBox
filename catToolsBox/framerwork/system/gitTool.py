#!/usr/bin/python
# -*- coding: utf-8 -*-

# @Time    : 2023/6/25 11:43 AM
# @Author  : LTH
# @File    : gitTool.py

import subprocess


class Git:
    # 配置提交模版
    def config_commit_template(path):
        subprocess.call(["git", "config", "--global", "commit.template", path])

