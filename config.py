"""
Author: Flandre Scarlet i@flandrescarlet.cn
Date: 2024-11-23 11:42:18
LastEditors: Flandre Scarlet i@flandrescarlet.cn
LastEditTime: 2024-11-25 14:05:18
FilePath: /jd_spider/config.py
Copyright (c) 2024 by Flandre Scarlet, All Rights Reserved.
"""

import json


class spiderConfig:
    def __init__(self):
        # 读取配置文件
        with open("./config/config.json", mode="r", encoding="utf-8") as f:
            cnf = json.loads(f.read())
            self.username = cnf.get("phone")
            self.password = cnf.get("password")
            self.chromedriver_path = cnf.get("chromedriver_path")
            self.chrome_path = cnf.get("chrome_path")
            self.user_data_path = cnf.get("user_data_path")
            self.js_stealth_path = cnf.get("js_stealth_path")
            self.js_get_items_data_path = cnf.get("js_get_items_data_path")
