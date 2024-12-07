"""
Author: Flandre Scarlet i@flandrescarlet.cn
Date: 2024-11-23 13:47:43
LastEditors: Flandre Scarlet i@flandrescarlet.cn
LastEditTime: 2024-11-25 14:04:18
FilePath: /jd_spider/main.py
Copyright (c) 2024 by Flandre Scarlet, All Rights Reserved.
"""

import time
import random
import pandas
from rule import Rule
from jdSpider import jdSpider
from config import spiderConfig


def main():
    # 初始化需要的变量
    rule = Rule()
    spider_cnf = spiderConfig()
    spider = jdSpider()

    # 创建浏览器窗口
    driver = jdSpider.init_driver(spider)

    # 加载 stealth.min.js 绕过selenium检查
    with open(spider_cnf.js_stealth_path, mode="r", encoding="utf-8") as f:
        stealth = f.read()
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {"source": stealth})
    # 访问 https://bot.sannysoft.com 查看 stealth.min.js 是否正确加载
    # driver.get("https://bot.sannysoft.com")

    # 登录账号
    while True:
        driver.get("https://www.jd.com/")
        print(f"{jdSpider.get_time_str(spider)} 检查是否已登录。")
        if jdSpider.is_logged(spider, driver=driver):
            print(f"{jdSpider.get_time_str(spider)} 已登录！正在等待跳转搜索...")
            break
        else:
            driver = jdSpider.jd_login(spider, driver=driver)
            print(f"{jdSpider.get_time_str(spider)} 登录成功！正在等待跳转搜索...")
            continue
    print(
        f"{jdSpider.get_time_str(spider)} 上次爬取的关键字是：{spider.keyword}，共爬取 {spider.crawled_page_num - 1} 页，共爬取 {spider.crawled_count - 1} 条记录。"
    )
    print(f"{jdSpider.get_time_str(spider)} 正在爬取第 {spider.crawled_page_num} 页")
    # 输入搜索关键词
    jdSpider.search(spider, driver=driver, keyword=spider.keyword)
    time.sleep(round(random.uniform(0.2, 0.5), 2))
    jdSpider.move_page_bottom(spider, driver=driver)
    page_num = jdSpider.get_page_num(spider, driver=driver)
    print(f"{jdSpider.get_time_str(spider)} 当前总页数为：{page_num}页")
    for i in range(spider.crawled_page_num, page_num + 1):
        # 检查是否有验证码
        jdSpider.check_search_captcha(spider, driver=driver)
        time.sleep(round(random.uniform(1, 2.5), 2))
        if i != 0:
            # 翻页到页面底部
            jdSpider.move_page_bottom(spider, driver=driver)

        data_frame = pandas.DataFrame(
            columns=[
                "item_description",
                "item_price",
                "item_price_notes",
                "comment_count",
                "store_name",
                "product_tags",
            ]
        )
        # 检查是否有验证码
        jdSpider.check_search_captcha(spider, driver=driver)
        # 获取商品数据
        data_frame = jdSpider.get_items_data(
            spider, driver=driver, data_frame=data_frame
        )

        # 数据导出
        jdSpider.output_csv(spider, pd_obj=data_frame)

        print(f"{jdSpider.get_time_str(spider)} 爬取下一页...")
        jdSpider.page_down(spider, driver=driver)
    # debug
    # input(f"{jdSpider.get_time_str(spider)} Press Enter to continue...\n")
    # 关闭浏览器
    driver.quit()
    # 数据导出
    jdSpider.wash_data(spider, data_path="./data/temp", file_type="xlsx")


if __name__ == "__main__":
    main()
