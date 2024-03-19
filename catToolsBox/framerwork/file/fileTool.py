#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import shutil
import zipfile

from framerwork.log.log import Log


# @Time    : 2023/7/14 10:40 AM
# @Author  : LTH
# @File    : fileTool.py

class File:
    # 解压
    @staticmethod
    def unzip_file(zfile_path, unzip_dir):
        try:
            with zipfile.ZipFile(zfile_path) as zfile:
                zfile.extractall(path=unzip_dir)
        except zipfile.BadZipFile as e:
            Log.error(zfile_path + " 解压出问题请检查!")

    # 删除文件夹
    @staticmethod
    def remove_dir(dir_path):
        if os.path.isdir(dir_path):
            shutil.rmtree(dir_path)
        else:
            Log.error(dir_path + " 不是文件夹!")

    @staticmethod
    def getFileName(path):
        return os.path.splitext(os.path.basename(path))[0]

    @staticmethod
    def get_FileSize(filePath):
        if isinstance(filePath, bytes):
            text = filePath.decode('utf8')
        else:
            text = filePath

        fsize = os.path.getsize(text) / (1024 * 1024)  # 获取文件大小并转换为MB
        return round(fsize, 4)  # 保留两位小数