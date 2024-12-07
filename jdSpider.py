"""
Author: Flandre Scarlet i@flandrescarlet.cn
Date: 2024-11-21 14:44:35
LastEditors: Flandre Scarlet i@flandrescarlet.cn
LastEditTime: 2024-11-25 14:05:00
FilePath: /jd_spider/jdSpider.py
Copyright (c) 2024 by Flandre Scarlet, All Rights Reserved.
"""

import os
import time
import json
import pandas
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from rule import Rule
from config import spiderConfig


class jdSpider:

    def __init__(self):
        with open("./config/crawl_cache.json", mode="r", encoding="utf-8") as f:
            cr_cnf = json.loads(f.read())
        # 加载xpath规则
        self.xpath_rule = Rule()
        self.config = spiderConfig()
        # 读取爬取的关键字
        self.keyword = cr_cnf.get("keyword")
        # 读取已爬取到的页数
        self.crawled_page_num = cr_cnf.get("crawled_page_num")
        # 读取已爬取的数据记录数
        self.crawled_count = cr_cnf.get("crawled_count")

    def get_time_str(self):
        return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

    def init_driver(self):
        service = Service(executable_path=self.config.chromedriver_path)
        options = Options()
        # 连接已打开的浏览器
        # chrome.exe --remote-debugging-port=9222 --user-data-dir="./config/user_data"
        # options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")

        # 禁用blink标识
        options.add_argument("--disable-blink-features=AutomationControlled")
        # 取消"Chrome正受到自动软件的控制"提示
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        # 禁用Chrome的自动化扩展
        options.add_experimental_option("useAutomationExtension", False)
        # 关闭WebGL
        options.add_argument("--disable-webgl")
        # 设置用户数据文件夹
        options.add_argument(
            f"--user-data-dir={os.getcwd() + self.config.user_data_path}"
        )

        if self.config.chrome_path != "default":
            options.binary_location = self.config.chrome_path

        options.add_argument("--no-sandbox")  # 禁用沙盒模式
        options.add_argument("--log-level=3")  # 设置日志等级
        options.add_argument("--ignore-certificate-errors")  # 忽略证书错误
        # 设置UA
        # options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36")

        driver = webdriver.Chrome(service=service, options=options)
        # 修改 navigator.webdriver 属性
        driver.execute_script(
            "Object.defineProperty(navigator, 'webdriver', {get: () => undefined});"
        )

        # driver.maximize_window()
        driver.set_window_size(1280, 720)
        driver.implicitly_wait(10)  # 设置隐式等待
        return driver

    # 检查是否登录
    def is_logged(self, driver):
        try:
            driver.get("https://www.jd.com")
            # 尝试获取用户名界面元素，如果能够正常获取（即已登录）则返回True
            # 此处的try仅是用于尝试是否能获取到该元素（因为如果未登录则不存在此界面元素会报错），不用于错误捕获。
            try:
                logged_element = driver.find_element(
                    by=By.XPATH, value=self.xpath_rule.interface_logged
                ).text
                if logged_element:
                    return True
            except Exception as e:
                pass
            login_text = driver.find_element(
                by=By.XPATH, value=self.xpath_rule.interface_login_text
            ).text
            # print(login_text)
            if login_text == "未登录" or login_text == "请登录":
                return False
            else:
                return True
        except Exception as e:
            print(e)
            print(f"{self.get_time_str()} 检查是否登录失败...")
            return False

    # 登录函数
    def jd_login(self, driver):
        driver.get("https://passport.jd.com/uc/login")
        driver.find_element(
            by=By.XPATH, value=self.xpath_rule.login_username
        ).send_keys(self.config.username)
        driver.find_element(
            by=By.XPATH, value=self.xpath_rule.login_password
        ).send_keys(self.config.password)
        driver.find_element(by=By.XPATH, value=self.xpath_rule.login_button).click()
        print(f"{self.get_time_str()} 等待用户完成滑块验证码...")
        while True:
            if "www.jd.com" not in driver.current_url:
                print(f"{self.get_time_str()} 等待用户登录...")
                time.sleep(0.25)
            else:
                break
        return driver

    # 搜索函数
    def search(self, driver, keyword):
        driver.get("https://search.jd.com/")
        # 定位搜索框
        search_input_element = driver.find_element(
            by=By.XPATH, value=self.xpath_rule.search_input
        )
        search_input_element.send_keys(keyword)
        time.sleep(2)
        # 定位并点击搜索按钮
        driver.find_element(by=By.XPATH, value=self.xpath_rule.search_button).click()
        return driver

    # 检查是否在滑块验证码界面
    def check_search_captcha(self, driver):
        print(f"{self.get_time_str()} 正在检测页面异常")
        while True:
            if "search.jd.com" not in driver.current_url:
                print(f"{self.get_time_str()} 等待用户通过验证码")
                time.sleep(0.25)
            else:
                print(f"{self.get_time_str()} 无异常")
                break
        return driver

    # 翻页到页面底部来实现网页完全加载
    def move_page_bottom(self, driver):
        driver = webdriver.ActionChains(driver)
        # 模拟用户按pagedown实现页面完全加载
        for i in range(15):
            driver.send_keys(Keys.PAGE_DOWN).perform()
            time.sleep(round(random.uniform(0.2, 0.9), 2))
        return driver

    # 上一页
    def page_up(self, driver):
        driver = webdriver.ActionChains(driver)
        driver.send_keys(Keys.LEFT).perform()

    # 下一页
    def page_down(self, driver):
        driver = webdriver.ActionChains(driver)
        driver.send_keys(Keys.RIGHT).perform()

    # 更新数据状态
    def update_status(self, path, keyword, crawled_page_num, crawled_count):
        with open(file=path, mode="w", encoding="utf-8") as f:
            f.write(
                json.dumps(
                    {
                        "keyword": keyword,
                        "crawled_page_num": crawled_page_num,
                        "crawled_count": crawled_count,
                    },
                    ensure_ascii=False,
                )
            )
        print(f"{self.get_time_str()} 缓存信息已更新！")

    # 获取商品列表最多为几页
    def get_page_num(self, driver):
        try:
            page_num = driver.find_element(
                by=By.XPATH, value=self.xpath_rule.interface_page_num
            ).text
        except Exception as e:
            print(e)
            print(f"{self.get_time_str()} 获取总页码失败")
            # 设置获取错误的默认最大页码为50页
            page_num = 50
        return int(page_num)

    # 获取所有商品信息
    # 旧的实现方式 采用 selenium 提供的 find_element 方法，效率太低。
    def get_items_data_old(self, driver, data_frame):
        # 判断当前页码，跳转到上次爬取页面的后一页继续
        now_page_num = int(
            driver.find_element(
                by=By.CSS_SELECTOR, value="#J_bottomPage > span.p-num > a.curr"
            ).text
        )
        # 判断页码
        if now_page_num != self.crawled_page_num:
            page_num_input = driver.find_element(
                by=By.XPATH, value=self.xpath_rule.interface_page_jump_input
            )
            # print(page_num_input)
            print(f"{self.get_time_str()} 清除页码输入框")
            page_num_input.clear()
            print(f"{self.get_time_str()} 输入页码：{self.crawled_page_num}")
            page_num_input.send_keys(self.crawled_page_num)
            print(f"{self.get_time_str()} 点击跳转按钮")
            driver.find_element(
                by=By.XPATH, value=self.xpath_rule.interface_page_jump_button
            ).click()
        # 检查是否有验证码
        self.check_search_captcha(driver=driver)
        # 获取商品列表
        items = driver.find_elements(
            by=By.XPATH, value=self.xpath_rule.interface_items_list
        )

        print(
            f"{self.get_time_str()} 正在爬取第{self.crawled_page_num}页，当前页面商品数量：{len(items)}。"
        )
        print("===============")
        for item in items:
            print(f"{self.get_time_str()} 正在爬取第{self.crawled_count}条数据")

            # 商品描述
            item_description = "N/A"
            try:
                item_description = item.find_element(
                    by=By.XPATH, value=self.xpath_rule.interface_item_item_description
                ).text
            except Exception as e:
                # print(e)
                print(f"{self.get_time_str()} 商品描述获取失败")
            print(f"{self.get_time_str()} 商品描述：{item_description}")

            # 价格
            item_price = "N/A"
            try:
                item_price = item.find_element(
                    by=By.XPATH, value=self.xpath_rule.interface_item_item_price
                ).text
            except Exception as e:
                # print(e)
                print(f"{self.get_time_str()} 价格获取失败")
            print(f"{self.get_time_str()} 商品价格：{item_price}")

            # 商品价格备注
            item_price_notes = "N/A"
            try:
                item_price_notes = item.find_element(
                    by=By.XPATH, value=self.xpath_rule.interface_item_item_price_notes
                ).text
                print(f"{self.get_time_str()} 更多价格信息：{item_price_notes}")
            except Exception as e:
                # print(e)
                print(f"{self.get_time_str()} 更多价格标签获取失败")
                print(f"{self.get_time_str()} 更多价格信息：{item_price_notes}")

            # 评价数量
            comment_count = "N/A"
            try:
                comment_count = item.find_element(
                    by=By.XPATH, value=self.xpath_rule.interface_item_comment_count
                ).text
            except Exception as e:
                # print(e)
                print(f"{self.get_time_str()} 评论数量获取失败")
            print(f"{self.get_time_str()} 评价数量：{comment_count}")

            # 店铺名称
            store_name = "N/A"
            try:
                store_name = item.find_element(
                    by=By.XPATH, value=self.xpath_rule.interface_item_store_name
                ).text
            except Exception as e:
                # print(e)
                print(f"{self.get_time_str()} 店铺名称获取失败")
            print(f"{self.get_time_str()} 店铺名称：{store_name}")

            # 商品标签
            tag_temp_list = []
            product_tags = "N/A"
            try:
                for i in item.find_elements(
                    by=By.XPATH, value=self.xpath_rule.interface_item_product_tags
                ):
                    tag_temp_list.append(i.find_element(by=By.XPATH, value="i").text)
                product_tags = "、".join(str(item) for item in tag_temp_list)
            except Exception as e:
                # print(e)
                print(f"{self.get_time_str()} 商品tag不存在")
            print(f"{self.get_time_str()} 商品tag：{product_tags}")

            new_row = {
                "item_description": item_description,
                "item_price": item_price,
                "item_price_notes": item_price_notes,
                "comment_count": comment_count,
                "store_name": store_name,
                "product_tags": product_tags,
            }
            # 将新行字典转换为DataFrame
            new_row_df = pandas.DataFrame([new_row])
            # 使用concat方法将新行添加到data_frame中
            data_frame = pandas.concat([data_frame, new_row_df], ignore_index=True)
            self.crawled_count += 1
            print(
                f"{self.get_time_str()} 成功提交数据到data_frame，当前共有{len(data_frame)}条数据。"
            )
            print("---------------")
        self.crawled_page_num += 1
        self.update_status(
            path="./config/crawl_cache.json",
            keyword=self.keyword,
            crawled_page_num=self.crawled_page_num,
            crawled_count=self.crawled_count,
        )
        return data_frame

    # 获取所有商品信息
    # 使用 execute_script 方法执行 JavaScript
    # 利用 JavaScript 脚本在浏览器端定位元素取值后返回
    def get_items_data(self, driver, data_frame):
        # 判断当前页码，跳转到上次爬取页面的后一页继续
        now_page_num = int(
            driver.find_element(
                by=By.CSS_SELECTOR, value="#J_bottomPage > span.p-num > a.curr"
            ).text
        )
        if now_page_num != self.crawled_page_num:
            page_num_input = driver.find_element(
                by=By.CSS_SELECTOR, value=self.xpath_rule.interface_page_jump_input
            )
            page_num_input.clear()
            page_num_input.send_keys(self.crawled_page_num)
            driver.find_element(
                by=By.CSS_SELECTOR, value=self.xpath_rule.interface_page_jump_button
            ).click()

        # 检查是否有验证码
        self.check_search_captcha(driver)

        # 使用JavaScript获取商品信息
        with open(self.config.js_get_items_data_path, mode="r", encoding="utf-8") as f:
            items_data_js = f.read()

        items_data = driver.execute_script(f"return {items_data_js}")

        if items_data is None:
            raise Exception("thing went wrong, somehow items_data is None")

        for item_data in items_data:
            new_row_df = pandas.DataFrame([item_data])
            data_frame = pandas.concat([data_frame, new_row_df], ignore_index=True)
            self.crawled_count += 1
            print(
                f"{self.get_time_str()} 第{self.crawled_count-1}条数据爬取成功: {item_data}"
            )

        self.crawled_page_num += 1
        self.update_status(
            path="./config/crawl_cache.json",
            keyword=self.keyword,
            crawled_page_num=self.crawled_page_num,
            crawled_count=self.crawled_count,
        )
        return data_frame

    # 将xpath选择器转换为css选择器
    def xpath_to_css(self, xpath):
        css = ""
        # 拆分XPath，忽略以'//'开头的任意位置的选择
        parts = xpath.strip().split("/")
        for part in parts:
            if part.startswith("@"):  # 忽略纯属性
                continue

            # 检查是否包含条件
            if "[" in part:
                tag, conditions = part.split("[")
                conditions = conditions[:-1]  # 移除结尾的']'
                css_conditions = []

                # 可能存在多个条件，需要拆分处理
                conditions_parts = conditions.split(" and ")
                for cond in conditions_parts:
                    if "=" in cond:
                        attr, value = cond.split("=")
                        value = value.strip("\"'")
                        if "id" in attr:
                            css_conditions.append(f"#{value}")
                        elif "class" in attr:
                            css_conditions.append(f'.{value.replace(" ", ".")}')
                        else:
                            css_conditions.append(f'[{attr}="{value}"]')
                    elif (
                        cond.isdigit()
                    ):  # 索引位置转换为:nth-child()，注意XPath基于1开始
                        css_conditions.append(f":nth-child({cond})")
                css += f"{tag if tag else '*'}{''.join(css_conditions)} "
            else:
                # 处理常规标签
                if part and not part.startswith("@"):
                    css += f"{part} "

        # 返回CSS选择器，去除额外的空格
        return css.strip().replace(" ", " > ")

    # 导出数据保存为 csv
    def output_csv(self, pd_obj):
        data_file_path = f'./data/temp/{time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime())}_{self.keyword}_p{self.crawled_page_num-1}.csv'
        pd_obj.to_csv(data_file_path, encoding="utf-8-sig", index=False)
        print(f"{self.get_time_str()} 导出成功！文件位于：{data_file_path}")

    # 清洗数据并导出
    def wash_data(self, data_path, file_type="csv"):
        # 获取文件夹内所有CSV文件的路径
        csv_files = [
            os.path.join(data_path, file)
            for file in os.listdir(data_path)
            if file.endswith(".csv")
        ]

        # 读取所有CSV文件到DataFrame列表中
        data_frames = []
        for file in csv_files:
            df = pandas.read_csv(file, encoding="utf-8-sig")
            data_frames.append(df)

        # 合并所有DataFrame为一个，并且只保留一个表头
        merged_df = pandas.concat(data_frames, ignore_index=True)

        # 去除重复的记录
        merged_df.drop_duplicates(inplace=True)
        print(f"{self.get_time_str()} 文件清洗完成，正在尝试导出文件。")
        data_file_path = f'./data/{time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime())}_{self.keyword}.{file_type}'
        # 将合并后的DataFrame导出
        if file_type == "csv":
            merged_df.to_csv(data_file_path, index=False, encoding="utf-8-sig")
        elif file_type == "xlsx":
            merged_df.to_excel(data_file_path, index=False)
        print(f"{self.get_time_str()} 导出成功！文件位于：{data_file_path}")
