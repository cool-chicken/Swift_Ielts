from openai import OpenAI
import os


KIMI_API_KEY = os.getenv("KIMI_API_KEY")
if not KIMI_API_KEY:
    raise ValueError("请设置 KIMI_API_KEY 环境变量")

client = OpenAI(
    api_key = KIMI_API_KEY,
    base_url="https://api.moonshot.cn/v1",
)
 
completion = client.chat.completions.create(
    model="moonshot-v1-128k",
    messages=[
        {"role": "system",
         "content": "你是 Kimi，由 Moonshot AI 提供的人工智能助手，你更擅长中文和英文的对话。你会为用户提供安全，有帮助，准确的回答。同时，你会拒绝一切涉及恐怖主义，种族歧视，黄色暴力等问题的回答。Moonshot AI 为专有名词，不可翻译成其他语言。"},
        {"role": "user", "content": "你好，请给出python库lxml的介绍以及详细用法"}
    ],
    temperature=0.3,
)
 
print(completion.choices[0].message)
