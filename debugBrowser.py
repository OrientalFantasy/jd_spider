import os
import socket
from selenium.webdriver.chrome.options import Options


class DebugBrowser:
    def __init__(self):
        self.ip = "127.0.0.1"
        self.port = 9222
        self.user_file = (
            "./"  # 注意：确保这个目录可写，或者指定到一个实际存在且可写的目录
        )
        self.chrome_option = Options()
        print("DebugBrowser 初始化完成，设置为 IP: 127.0.0.1, 端口: 9222")

    def debug_chrome(self):
        if self.check_port():
            print(f"端口 {self.port} 已在使用中，将连接到此端口上的浏览器实例。")
            self.chrome_option.add_experimental_option(
                "debuggerAddress", f"{self.ip}:{self.port}"
            )
        else:
            print(f"端口 {self.port} 未在使用，尝试启动新的 Chrome 浏览器实例。")
            # 获取并扩展 %ProgramFiles% 环境变量
            program_files = os.environ.get("ProgramFiles")
            chrome_path = os.path.join(
                program_files, "Google", "Chrome", "Application", "chrome.exe"
            )
            if not os.path.exists(chrome_path):
                print(f"未找到 Chrome 执行文件：{chrome_path}")
                return None

            print(f"使用路径 {chrome_path} 启动 Chrome。")
            # 构建命令行并使用 os.popen 启动
            chrome_cmd = f'"{chrome_path}" --remote-debugging-port={self.port} --user-data-dir="{self.user_file}"'
            try:
                process = os.popen(chrome_cmd)
                output = process.read()
                print("Chrome 浏览器启动命令已发送。")
                print(output)  # 输出 Chrome 启动日志
            except Exception as e:
                print(f"尝试启动 Chrome 时出现错误: {str(e)}")

            self.chrome_option.add_experimental_option(
                "debuggerAddress", f"{self.ip}:{self.port}"
            )
        return self.chrome_option

    def check_port(self):
        """
        判断调试端口是否监听
        :return:check 是否监听
        """
        print(f"检查端口 {self.port} 是否在监听...")
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex((self.ip, self.port))
        sock.close()
        if result == 0:
            print(f"端口 {self.port} 正在监听。")
            return True
        else:
            print(f"端口 {self.port} 未监听。")
            return False
