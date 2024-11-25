"""
Author: Flandre Scarlet i@flandrescarlet.cn
Date: 2024-11-22 16:28:55
LastEditors: Flandre Scarlet i@flandrescarlet.cn
LastEditTime: 2024-11-25 14:04:49
FilePath: /jd_spider/rule.py
Copyright (c) 2024 by Flandre Scarlet, All Rights Reserved.
"""

import json

# 读取规则文件
with open("config/rule.json", mode="r", encoding="utf-8") as f:
    conf = json.loads(f.read())


class Rule:

    def __init__(self):
        # 界面 xpath 规则
        self.interface_login_text = conf.get("interface").get("login_text")
        self.interface_items_list = conf.get("interface").get("items_list")
        # 界面 item xpath 规则
        self.interface_item_item_description = (
            conf.get("interface").get("item").get("item_description")
        )
        self.interface_item_item_price = (
            conf.get("interface").get("item").get("item_price")
        )
        self.interface_item_item_price_notes = (
            conf.get("interface").get("item").get("item_price_notes")
        )
        self.interface_item_comment_count = (
            conf.get("interface").get("item").get("comment_count")
        )
        self.interface_item_store_name = (
            conf.get("interface").get("item").get("store_name")
        )
        self.interface_item_product_tags = (
            conf.get("interface").get("item").get("product_tags")
        )
        self.interface_logged = conf.get("interface").get("logged")

        # 页数
        self.interface_page_num = conf.get("interface").get("page_num")

        # 跳转
        self.interface_page_jump_input = conf.get("interface").get("page_jump_input")
        self.interface_page_jump_button = conf.get("interface").get("page_jump_button")

        # 登录页 xpath 规则
        self.login_username = conf.get("login").get("username")
        self.login_password = conf.get("login").get("password")
        self.login_button = conf.get("login").get("button")

        # 搜索页 xpath 规则
        self.search_input = conf.get("search").get("input")
        self.search_button = conf.get("search").get("button")


if __name__ == "__main__":
    test = Rule().login_username
    print(test)
