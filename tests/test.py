import requests
import json

url = "https://api.dify.ai/v1/workflows/run"

payload = {
    "inputs": {
        "char_id": "许苗苗",
        "act_num": 1,
        "model_name": "qwen"
    },
    "response_mode": "streaming",
    "user": "<random string>"
}
headers = {
    "Authorization": "Bearer app-5g0InYQpYIrOxlzWJb5URjXH",
    "Content-Type": "application/json"
}

# 发送请求时需要设置 stream=True 来接收流式响应
response = requests.post(url, json=payload, headers=headers, stream=True)

# 确保响应以 utf-8 编码进行解码
response.encoding = 'utf-8'

print("--- 开始接收流式响应 ---")

# 遍历响应的每一行
for line in response.iter_lines(decode_unicode=True):
    # SSE 事件通常以 "data: " 开头，我们需要处理非空行
    if line and line.startswith('data: '):
        # 移除 "data: " 前缀，获取真正的 JSON 字符串
        json_string = line[len('data: '):]
        
        # 流结束时，Dify API 可能会发送一个 [DONE] 标记
        if json_string.strip() == '[DONE]':
            print("--- 响应流结束 ---")
            break
            
        try:
            # 使用 json.loads() 将 JSON 字符串解析为 Python 字典
            # 这个过程会自动将 \uXXXX 转换为对应的字符
            data = json.loads(json_string)
            
            # 使用 json.dumps() 来美化输出
            # ensure_ascii=False 是关键，它保证输出的是中文字符而不是\u编码
            pretty_json = json.dumps(data, indent=4, ensure_ascii=False)
            print(pretty_json)
            
        except json.JSONDecodeError:
            # 如果某一行不是有效的 JSON，则直接打印
            print(f"接收到非JSON数据: {json_string}")

