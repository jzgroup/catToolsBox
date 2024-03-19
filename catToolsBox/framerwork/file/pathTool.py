# #!/usr/bin/env python3
# # -*- coding: utf-8 -*-


#    TODO:   路径工具
#    Author: LTH
#    Date:   2023-6-20

import os
import shutil


class Path:

    """新建文件夹"""
    @staticmethod
    def mkdir(path):
        if not os.path.exists(path):
            os.makedirs(path)
        return path

    # 清空文件夹
    @staticmethod
    def clearDir(path):
        if os.path.exists(path):
            shutil.rmtree(path)
        os.makedirs(path)
        return path

    """列出指定路径下所有文件"""

    @staticmethod
    def list_all(dir_name):
        if not os.path.isdir(dir_name):
            return []
        file_list = []
        for dirPath, dirNames, filenames in os.walk(dir_name):
            for filename in filenames:
                file_list.append(os.path.join(dirPath, filename))
        return file_list

    # 列出指定路径下所有文件, 指定后缀
    @staticmethod
    def list_all_suffix(dir_name, suffix):
        if not os.path.isdir(dir_name):
            return []
        file_list = []
        for dirPath, dirNames, filenames in os.walk(dir_name):
            for filename in filenames:
                if filename.endswith(suffix):
                    file_list.append(os.path.join(dirPath, filename))
        return file_list

    """列出指定路径下子文件夹"""

    @staticmethod
    def list_subDirs(path):
        if not os.path.isdir(path):
            return []
        subDirs = []
        for name in os.listdir(path):
            new_path = os.path.join(path, name)
            if os.path.isdir(new_path):
                subDirs.append(new_path)
        return subDirs

    """列出指定路径下所有文件夹, 只要文件夹名"""

    @staticmethod
    def list_subDirs_name(path):
        if not os.path.isdir(path):
            return []
        subDirs = []
        for name in os.listdir(path):
            new_path = os.path.join(path, name)
            if os.path.isdir(new_path):
                subDirs.append(name)
        return subDirs

    """列出指定路径下子文件"""
    @staticmethod
    def list_subFiles(path):
        if not os.path.isdir(path):
            return []
        subFiles = []
        for name in os.listdir(path):
            new_path = os.path.join(path, name)
            if os.path.isfile(new_path):
                subFiles.append(new_path)
        return subFiles

    
