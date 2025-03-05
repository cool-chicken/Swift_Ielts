import base64
import requests
import json

def call_kimi_api(answer, text_file_path, image_file_path):
    # 读取 API 密钥
    try:
        with open('api_key.txt', 'r') as file:
            api_key = file.read().strip()
            if not api_key:
                raise ValueError("Please provide your Kimi API key")
    except FileNotFoundError:
        raise ValueError("API key file not found. Please ensure 'api_key.txt' exists.")

    # 读取文本文件内容
    try:
        with open(text_file_path, 'r') as file:
            essay_requirements = file.read()
    except FileNotFoundError:
        raise ValueError(f"Text file not found: {text_file_path}")

    # 读取图片文件并转换为 Base64（如果需要）
    try:
        with open(image_file_path, 'rb') as file:
            image_data = base64.b64encode(file.read()).decode('utf-8')
    except FileNotFoundError:
        raise ValueError(f"Image file not found: {image_file_path}")

    base_url = "https://api.kimi.com/v1/"  # 假设 API 版本为 v1
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    # 构造请求体
    payload = {
    "model": "kimi-ielts grader",  # 假设模型名称
        "messages": [
            {"role": "system", "content": "You are an IELTS essay grader."},
            {"role": "user", "content": f"Grade the following essay: {answer}"},
            {"role": "user", "content": f"Here is the question image (Base64 encoded): {image_data}"},
            {"role": "user", "content": f"Essay requirements: {essay_requirements}"}
        ],
        "temperature": 0.3
    }

    # 发送请求
    response = requests.post(f"{base_url}chat/completions", headers=headers, data=json.dumps(payload))

    # 处理响应
    if response.status_code == 402:
        raise ValueError("Insufficient balance to process the request. Please check your account balance.")
    elif response.status_code != 200:
        try:
            error_info = response.json().get('error', {})
            raise Exception(f"API request failed with error: {error_info.get('message', 'Unknown error')}")
        except ValueError:  # 如果响应不是 JSON 格式
            raise Exception(f"API request failed with status code {response.status_code}: {response.text}")

    return response.json()

# 示例调用
answer = "My answer is here."
question_text_path = "/Users/rachelwu/ielts_platform/database/writing_tasks/Ielts_1_text.txt"
image_file_path = "/Users/rachelwu/ielts_platform/database/writing_tasks/Ielts_1.png"
try:
    response = call_kimi_api(answer, question_text_path, image_file_path)
    print(response)
except ValueError as e:
    print(e)
except Exception as e:
    print(e)