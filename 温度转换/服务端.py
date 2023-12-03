from flask import Flask, request
import psutil
import threading
import tkinter as tk
import os
import signal

app = Flask(__name__)

# 获取 CPU 使用率和内存占用
def get_system_info():
    cpu_usage = psutil.cpu_percent(interval=1)
    memory_usage = psutil.virtual_memory().percent
    return cpu_usage, memory_usage

# 创建主窗口
window = tk.Tk()
window.title("服务端监控")
window.geometry("400x300")

# 标题标签
title_label = tk.Label(window, text="服务端输出")
title_label.pack(pady=10)

# 输出框
output_text = tk.Text(window, height=10, width=50, state="disabled")
output_text.pack(pady=10)

def print_to_gui(message):
    output_text.config(state="normal")
    output_text.insert(tk.END, message + "\n")
    output_text.config(state="disabled")
    output_text.see(tk.END)

# Flask 路由
@app.route('/')
def index():
    return "Hello, this is the server."

@app.route('/calculate', methods=['POST'])
def calculate():
    try:
        username = request.form.get('username')
        temperature = float(request.form.get('temperature'))
        conversion_type = int(request.form.get('conversion_type'))

        if conversion_type == 1:  # 摄氏度转华氏度
            result_value = f"您好{username}，温度 {temperature} 摄氏度等于 {(temperature * 9/5) + 32:.2f} 华氏度"
        elif conversion_type == 2:  # 华氏度转摄氏度
            result_value = f"您好{username}，温度 {temperature} 华氏度等于 {(temperature - 32) * 5/9:.2f} 摄氏度"
        else:
            result_value = f"您好{username}，请选择转换类型."

        print_to_gui(f"客户端请求：用户名 {username}, 温度 {temperature}, 转换类型 {conversion_type}")
        print_to_gui(f"服务端响应：{result_value}")

        return result_value, 200

    except ValueError:
        error_message = "无效输入，请输入有效数字."
        print_to_gui(f"客户端请求错误：{error_message}")
        print_to_gui(f"服务端响应：{error_message}")
        return error_message, 400

def start_flask():
    app.run(debug=False)

# 启动更新窗口标题的线程
update_thread = threading.Thread(target=start_flask)
update_thread.start()

# 在窗口中显示 CPU 和内存信息
def update_window_title():
    while True:
        cpu_usage, memory_usage = get_system_info()
        window.title(f"服务端监控 - CPU: {cpu_usage}%  内存: {memory_usage}%")
        window.update()

# 启动更新窗口标题的线程
update_thread = threading.Thread(target=update_window_title)
update_thread.start()

# 关闭服务器按钮
def stop_server():
    os.kill(os.getpid(), signal.SIGINT)

stop_button = tk.Button(window, text="关闭服务器", command=stop_server)
stop_button.pack(pady=10)

# 启动 Tkinter 主循环
window.mainloop()
