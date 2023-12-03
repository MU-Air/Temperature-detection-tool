from flask import Flask, request

app = Flask(__name__)

@app.route('/calculate', methods=['POST'])
def calculate():
    try:
        # 处理客户端请求
        username = request.form.get('username')
        temperature = float(request.form.get('temperature'))
        conversion_type = int(request.form.get('conversion_type'))

        if conversion_type == 1:  # 摄氏度转华氏度
            result_value = f"您好{username}，温度 {temperature} 摄氏度等于 {(temperature * 9/5) + 32:.2f} 华氏度"
        elif conversion_type == 2:  # 华氏度转摄氏度
            result_value = f"您好{username}，温度 {temperature} 华氏度等于 {(temperature - 32) * 5/9:.2f} 摄氏度"
        else:
            result_value = f"您好{username}，请选择转换类型."

        # 输出客户端请求相关信息和服务端对客户端的响应
        print(f"客户端请求：用户名 {username}, 温度 {temperature}, 转换类型 {conversion_type}")
        print(f"服务端响应：{result_value}")

        return result_value, 200

    except ValueError:
        error_message = "无效输入，请输入有效数字."

        # 输出客户端请求相关信息（错误）和服务端对客户端的响应（错误）
        print(f"客户端请求错误：{error_message}")
        print(f"服务端响应：{error_message}")

        return error_message, 400

if __name__ == '__main__':
    app.run(debug=True)
