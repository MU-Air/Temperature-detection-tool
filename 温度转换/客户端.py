import tkinter as tk
import requests
from ping3 import ping
from threading import Thread

VERSION = "1.0"

def send_request_and_get_result():
    try:
        username = username_entry.get()
        temperature = float(entry.get())
        conversion_type = var.get()
        url = "http://127.0.0.1:5000/calculate"  # 服务器 IP 地址和端口

        payload = {"username": username, "temperature": temperature, "conversion_type": conversion_type}
        
        # 在新线程中执行网络请求
        thread = Thread(target=send_request, args=(url, payload))
        thread.start()

    except ValueError:
        result.set("无效输入，请输入有效数字.")

def send_request(url, payload):
    try:
        response = requests.post(url, data=payload)

        if response.status_code == 200:
            result.set(response.text)
        else:
            result.set("服务器请求失败.")

    except Exception as e:
        result.set(f"请求失败: {str(e)}")

def check_connection_quality():
    try:
        url = "http://127.0.0.1:5000/check_connection_quality"  # 服务器的 IP 地址和端口

        # 在新线程中执行延迟检测
        thread = Thread(target=check_latency, args=(url,))
        thread.start()

    except Exception as e:
        result.set(f"检测失败: {str(e)}")

def check_latency(url):
    try:
        # 连接质量检测过程
        delay = ping(url, unit='ms')

        # 获取当前电脑IP
        current_ip = requests.get('https://api64.ipify.org?format=json').json()['ip']

        result.set(f"连接质量检测完成，延迟: {delay} ms，本机IP: {current_ip}")

    except Exception as e:
        result.set(f"检测失败: {str(e)}")

# 创建主窗口
window = tk.Tk()
window.title(f"转换工具 v{VERSION}")
window.geometry("300x400")

# 输入框（用户名）
username_label = tk.Label(window, text="输入用户名:")
username_label.pack(pady=10)
username_entry = tk.Entry(window)
username_entry.pack(pady=10)

# 输入框（温度）
entry_label = tk.Label(window, text="输入温度:")
entry_label.pack(pady=10)
entry = tk.Entry(window)
entry.pack(pady=10)

# 单选框
var = tk.IntVar()
celsius_radio = tk.Radiobutton(window, text="摄氏度转华氏度", variable=var, value=1)
celsius_radio.pack()
fahrenheit_radio = tk.Radiobutton(window, text="华氏度转摄氏度", variable=var, value=2)
fahrenheit_radio.pack()

# 转换按钮
convert_button = tk.Button(window, text="转换", command=send_request_and_get_result)
convert_button.pack(pady=10)

# 检测连接质量按钮
check_button = tk.Button(window, text="检测连接质量", command=check_connection_quality)
check_button.pack(pady=10)

# 结果显示
result = tk.StringVar()
result_label = tk.Label(window, textvariable=result)
result_label.pack(pady=10)

# 版本号显示
version_label = tk.Label(window, text=f"版本号: {VERSION}", font=("Helvetica", 8))
version_label.pack(side="bottom", pady=10)

# 启动主循环
window.mainloop()
