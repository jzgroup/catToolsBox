# #!/usr/bin/env python3
# # -*- coding: utf-8 -*-

#    TODO:   json工具
#    Author: LTH
#    Date:   2023-6-20
import json
from framerwork.log.log import Log


class Json:
    @staticmethod
    # 读取json数据
    def read_json(file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            Log().error("读取:" + file_path + ",数据失败")
            Log().error(str(e))
            return {}

    @staticmethod
    # 写入json数据
    def write_json(file_path, data):
        try:
            with open(file_path, "w") as f:
                json.dump(data, f)
        except Exception as e:
            Log().error("写入:" + file_path + ",数据失败")
            Log().error(e)
