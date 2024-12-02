# 某东爬虫

---

## 0. 温馨提示：~~前方有可能导致血压升高的屎山，请谨慎观看，感到不适请立刻关闭本项目（~~

## 1. 概述

用于爬取某东的搜索页面商品列表信息（仅提取了页面中间部分的商品信息，页面两边和下方的推荐没有爬取）。

~~起因是我的一个朋友作业需要，故而诞生了此仓库，由于时间太赶写的不好是一堆屎山。~~

## 2. 实现思路

由于需要尽快写出来拿到数据才选用了 Selenium 来实现，结果也是一堆坑。

### 2.1 Selenium 反检测

反检测思路主要来自于：https://www.zenrows.com/blog/selenium-avoid-bot-detection#disable-automation-indicator-webdriver-flags

#### 2.1.1 生成浏览器会话时添加参数

```
# 禁用 blink 标识
options.add_argument("--disable-blink-features=AutomationControlled")
# 排除收集 enable-automation 开关
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option("useAutomationExtension", False)
```

#### 2.1.2 修改浏览器驱动二进制文件中的 JavaScript 代码签名

由于 JavaScript 代码签名是存在一个变量里的，所以一但加载 webdriver 就会被网站 js 检测到，网页的 ajax 请求就拿不到数据，接口返回 403 了。

具体方法可以用 vim 编辑器打开浏览器驱动的二进制文件全局查找字符串然后修改保存即可

```
# vim 打开chromedriver.exe
vim chromedriver.exe

# 命令模式下替换
:%s/cdc_/abc_/g

# wq保存退出
:wq
```

注意：因为本项目使用的是 chrome 浏览器，所以只测试了 chrome 的驱动，其他浏览器的驱动未经过尝试，也不知道其他浏览器需要修改的字符串是什么。

### 2.3 提取数据

#### 2.3.1 <del>野路子！</del>使用 Selenium 提供的 find_element() 方法

效率奇慢，可能是每一次 find_element() python 都要和 WebDriver 通信<del>（大概（我也不是很清楚（猜的</del>。导致时间开销很大了，而且本身 find_element() 也很慢。

~~当然，也可能是我写的屎山代码导致的。毕竟很多元素不一定是每一个卡片都会有的，所以就只能先尝试能不能取到，取不到再做处理（~~

详细可看 jdSpider 中的 get_items_data_old()

P.S.：走野路子行不通，绕了很多弯路还不一定能得到好的效果，还是需要理论指导！应该得先去问问用过的人，或许有更好的解决方案呢（？

#### 2.3.2 另辟蹊径？JavaScript 大显神通

首先感谢 [whiterasbk (子钰余子式) · GitHub](https://github.com/whiterasbk) 提供的重要帮助！
他为我完成了其中 JavaScript 的代码，以及实现了将 xpath 选择器转换为 css 选择器的函数，帮我完成了最重要的部分！十分感谢。

在换用 JavaScript 来定位元素取值后，整体速度提升了将近 30 倍，毫不夸张。~~野路子害死人啊~~

## 3. 项目结构定义

```
│
├─ config.py    # 程序配置文件
├─ jdSpider.py  # 爬虫主体部分
├─ main.py      # 程序入口
├─ rule.py      # 读取元素定位规则
│
├─config                    # 配置文件目录
│  │  config.json           # 配置文件
│  │  crawl_cache.json      # 爬取记录配置
│  │  crawl_cache.json.bak  # 爬取记录备份
│  │  rule.json             # 元素定位规则
│  │
│  └─user_data              # 浏览器用户数据目录
├─data          # 数据存储文件夹
│  └─temp       # 临时文件存储文件夹
└─js
   ├─ get_items_data.js # 获取商品列表脚本
   └─ stealth.min.js    # Selenium反检测js
```

## 4. 使用方式

### 4.1 环境要求

我开发使用的环境是 Python 3.10.7，理论上不低于 Python 3.10 应该都可以运行。

pandas 版本号 2.2.3，selenium 版本号 4.26.1。

```
# 填写配置文件
# 主要是 config.json 和 crawl_cache.json
# crawl_cache.json 中的 keyword 是要爬取的（用于搜索的）商品名

# 安装依赖
pip install -r requirements.txt

# 改变工作目录到项目文件夹
cd jd_spider

# 运行 main.py
python main.py
```

## 5.鸣谢

| 感谢名单                                                 |
| -------------------------------------------------------- |
| [whiterasbk (子钰余子式)](https://github.com/whiterasbk) |
| Ghosin                                                   |

感谢你们对我的帮助和支持！

## 6. 版权说明和风险声明

<font style="font-size: 20px; color:#f00">本项目仅供学习交流使用，不允许用于任何非法用途，使用本项目造成的一切后果由使用人承担。</font>

<font style="font-size: 20px; color:#f00">项目代码部分除引用的项目外均遵守 AGPLv3 开源协议，引用的部分遵守原项目的开源协议，如有侵权请联系删除，联系邮箱：i@flandrescarlet.cn。</font>
