#!/usr/bin/python
# -*- coding: utf-8 -*-
from PIL import Image,ImageFile
import shutil
from framerwork.classes import *

G_CACHE_PATH = AppData.get_cache_path(AppData)

debug_path = os.path.join(G_CACHE_PATH, '异常图片')
if os.path.exists(debug_path):
    shutil.rmtree(debug_path)
os.makedirs(debug_path)


over_step_1024 = 60
over_step_512 = 30
over_step_256 = 30
over_2048 = []  #长或宽超过2048
over_1024 = []  #长或宽略微超过1024
over_512 = []  #长或宽略微超过512
over_256 = []  #长或宽略微超过256

# 图片集合
list1 = []
list2 = []

class CheckImage:
    def __init__(self, projectPath, windows):
        # 项目路径
        self.projectPath = projectPath
        # 进度条
        self.windows = windows

    def checkImage(self):
        # 清空缓存
        Path.clearDir(debug_path)
        debug_path1 = os.path.join(debug_path, '超尺寸图片')
        path = self.projectPath
        files = Path.list_all_suffix(self.projectPath, '.png')
        self.windows.checkImageProgressBarValue = 0
        i = 0
        for file in files:
            i = i + 1
            self.windows.checkImageProgressBarValue = i/len(files)*30
            if "/g" in file:
                continue
            img = Image.open(file)
            if img.size[0] > 2048 or img.size[1] > 2048:
                over_2048.append(file)
            elif 1024 < img.size[0] < 1084 and img.size[1] < 1084:
                over_1024.append(file)
            elif 1024 < img.size[1] < 1084 and img.size[0] < 1084:
                over_1024.append(file)
            elif 512 < img.size[0] < 542 and img.size[1] < 542:
                over_512.append(file)
            elif 512 < img.size[1] < 542 and img.size[0] < 542:
                over_512.append(file)
            # elif img.size[1] > 256 and abs(img.size[1] - 256) < over_step_256:
            #     over_256.append(file)
            # elif img.size[0] > 256 and abs(img.size[0] - 256) < over_step_256:
            #     over_256.append(file)

        debugTxt = open(debug_path + "/debug.txt", "a", encoding='utf-8')

        if len(over_2048) != 0:
            debugTxt.write("over 2048:\n")
            os.makedirs(debug_path1 + "/2048")
            for file in over_2048:
                debugTxt.write(file + "\n")
                shutil.copyfile(file, debug_path1 + "/2048/" + file[len(path):].replace("/", "\\"))

        if len(over_1024) != 0:
            debugTxt.write("over 1024:\n")
            os.makedirs(debug_path1 + "/1024")
            for file in over_1024:
                debugTxt.write(file + "\n")
                shutil.copyfile(file, debug_path1 + "/1024/" + file[len(path):].replace("/", "\\"))

        if len(over_512) != 0:
            debugTxt.write("over 512:\n")
            os.makedirs(debug_path1 + "/512")
            for file in over_512:
                debugTxt.write(file + "\n")
                shutil.copyfile(file, debug_path1 + "/512/" + file[len(path):].replace("/", "\\"))
        if len(over_256) != 0:
            debugTxt.write("over 256:\n")
            os.makedirs(debug_path1 + "/256")
            for file in over_256:
                debugTxt.write(file + "\n")
                shutil.copyfile(file, debug_path1 + "/256/" + file[len(path):].replace("/", "\\"))

        if len(over_2048) == 0 and len(over_1024) == 0 and len(over_512) == 0 and len(over_256) == 0:
            shutil.rmtree(debug_path1)

        self.samePicture()
    # 读取文件

    def samePicture(self):
        dir_name = self.projectPath
        for dirpath, dirnames, filenames in os.walk(dir_name):
            for filename in filenames:
                src_path = dirpath + '/' + filename

                suffix = filename[-4:]
                if suffix != ".png":
                    continue
                # 只检查x2
                if not ("x2" in src_path):
                    continue
                # g文件夹不检查
                if "/g/" in src_path:
                    continue
                if File.get_FileSize(src_path) < 0.01:
                    continue
                list1.append(src_path)
                list2.append(False)

        # print("读取图片完毕")
        self.compare_image_with_hash()

    def compare_image_with_hash(self):
        debug_path2 = os.path.join(debug_path, '相同图片')
        path = self.projectPath
        imgId = 0
        # 可以优化大小
        canBeOptimized = 0

        for i in range(len(list1)):
            pd = True
            if list2[i]:
                continue
                # 文件的文件夹路径

            im1 = Image.open(list1[i])
            list2[i] = True

            for j in range(i + 1, len(list1)):
                if list2[j]:
                    continue
                # 相同文件夹
                if os.path.dirname(list1[i]) == os.path.dirname(list1[j]):
                    continue
                if File.get_FileSize(list1[i]) != File.get_FileSize(list1[j]):
                    continue
                # 相同文件名
                self.windows.checkImageProgressBarValue = 30 + (i / len(list1)) * 70
                if self.compare_image(im1, list1[j]):
                    if pd:
                        pd = False
                        imgId = imgId + 1
                        os.makedirs(debug_path2 + "/" + str(imgId))
                        imgPath = list1[i][len(path):].replace("/", "\\")
                        imgPath2 = list1[i][len(path):].replace("/", "\\\\")
                        shutil.copyfile(list1[i], debug_path2 + "/" + str(imgId) + "/" + imgPath)
                        fileSize = File.get_FileSize(list1[i])
                        imgPath2 = "\'" + imgPath2[2:] + "\'"


                    list2[j] = True
                    canBeOptimized = canBeOptimized + fileSize
                    imgPath = list1[j][len(path):].replace("/", "\\")
                    imgPath2 = list1[j][len(path):].replace("/", "\\\\")
                    imgPath2 = "\'" + imgPath2[2:] + "\'"

                    shutil.copyfile(list1[j], debug_path2 + "/" + str(imgId) + "/" + imgPath)



    # 完全相同的图片
    def compare_image(self, im1, img_file2):
        im2 = Image.open(img_file2)
        if im1.size != im2.size:
            return False
        b = im1 == im2
        ImageFile.LOAD_TRUNCATED_IMAGES = True

        return b