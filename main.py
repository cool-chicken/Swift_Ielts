import os
import base64
import httpx
from openai import OpenAI

client = OpenAI(
    api_key='sk-EEC4MsuJlItTmE8jrkwF3K9LWMSwjug7LnE7YY6ItMZwthcB',
    base_url="https://api.moonshot.cn/v1",
)


def estimate_token_count(input_messages) -> int:
    """
    在这里实现你的 Tokens 计算逻辑，或是直接调用我们的 Tokens 计算接口计算 Tokens

    https://api.moonshot.cn/v1/tokenizers/estimate-token-count
    """
    header = {
        "Authorization": f"Bearer {'sk-EEC4MsuJlItTmE8jrkwF3K9LWMSwjug7LnE7YY6ItMZwthcB'}",
    }
    data = {
        "model": "moonshot-v1-128k",
        "messages": input_messages,
    }
    r = httpx.post("https://api.moonshot.cn/v1/tokenizers/estimate-token-count", headers=header, json=data)
    r.raise_for_status()
    return r.json()["data"]["total_tokens"]


def select_model(input_messages, max_tokens=1024) -> str:
    """
    select_model 根据输入的上下文消息 input_messages，以及预期的 max_tokens 值，
    选择一个大小合适的模型。

    select_model 内部会调用 estimate_token_count 函数计算 input_messages 所占用
    的 tokens 数量，加上 max_tokens 的值作为 total_tokens，并根据 total_tokens
    所处的区间选择恰当的模型。
    """
    prompt_tokens = estimate_token_count(input_messages)
    total_tokens = prompt_tokens + max_tokens
    if total_tokens <= 8 * 1024:
        return "moonshot-v1-8k"
    elif total_tokens <= 32 * 1024:
        return "moonshot-v1-32k"
    elif total_tokens <= 128 * 1024:
        return "moonshot-v1-128k"
    else:
        raise Exception("too many tokens 😢")



answer = '''The bar charts show data about computer ownership, with a further classification by
level of education, from 2002 to 2010.
A steady but significant rise can be seen in the percentage of the population that owned
a computer over the period. Just over half the population owned computers in 2002,
whereas by 2010 three out of four people had a home computer.
An analysis of the data by level of education shows that higher levels of education
correspond to higher levels of computer ownership in both of those years. In 2002, only
around 15% of those who did not finish high school had a computer but this figure had
trebled by 2010. There were also considerable increases, of approximately 30
percentage points, for those with a high school diploma or an unfinished college
education (reaching 65% and 85% respectively in 2010). However, graduates and
postgraduates proved to have the greatest level of ownership in 2010, at 90% and 95%
respectively, 20 percentage points higher than in 2002.
The last decade has seen a substantial growth in computer ownership in general, and
across all educational levels.'''
question_text_path = "/Users/rachelwu/ielts_platform/database/writing_tasks/Ielts_1_text.txt"
image_file_path = "/Users/rachelwu/ielts_platform/database/writing_tasks/Ielts_1.png"

# 读取文本文件内容
try:
    with open(question_text_path, 'r') as file:
            essay_requirements = file.read()
except FileNotFoundError:
        raise ValueError(f"Text file not found: {question_text_path}")

try:
    with open(image_file_path, 'rb') as file:
            image_data = file.read()
except FileNotFoundError:
        raise ValueError(f"Image file not found: {image_file_path}")


messages = [
    {"role": "system", "content": "You are an IELTS essay grader."},
    {"role": "user", "content": f"Here is the question image: {image_data}"},
    {"role": "user", "content": f"the requirements: {essay_requirements};Grade the following essay: {answer}"}
]

max_tokens = 2048
model = select_model(messages, max_tokens)

completion = client.chat.completions.create(
    model=model,
    messages=messages,
    max_tokens=max_tokens,
    temperature=0.3,
)

print("model:", model)
print("max_tokens:", max_tokens)
print("completion:", completion.choices[0].message.content)
