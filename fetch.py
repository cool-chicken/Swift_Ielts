from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
from bs4 import BeautifulSoup
import requests
import os
import json
from openai import OpenAI
import re

app = Flask(__name__, static_folder="static", template_folder=".")
CORS(app)

# 预定义可爬取的 URL 列表（确保合法性和安全性）
ALLOWED_URLS = {
    'ieltsliz_essays': "https://ieltsliz.com/100-ielts-essay-questions/communication-and-personality/",
    'ieltsliz_tips': 'https://ieltsliz.com/ielts-writing-task-2-essay-planning-tips/'
}

# 从环境变量中获取 Kimi API Key
KIMI_API_KEY = os.getenv("KIMI_API_KEY")
if not KIMI_API_KEY:
    raise ValueError("请设置 KIMI_API_KEY 环境变量")

def crawl_questions(url):
    try:
        response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
        soup = BeautifulSoup(response.text, 'html.parser')
        content_div = soup.find('div', class_='entry-content')
        paragraphs = content_div.find_all('p') if content_div else []
        
        questions = []
        for p in paragraphs:
            text = p.get_text().strip()
            if text and (text[0].isdigit() or text.startswith(('Discuss', 'Some'))):
                questions.append(text)
        return questions
    except Exception as e:
        return None

def call_kimi_api(prompt):
    try:
        client = OpenAI(
            api_key = KIMI_API_KEY,
            base_url="https://api.moonshot.cn/v1",
        )
        response = client.chat.completions.create(
            model="moonshot-v1-128k",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2
        )
        return response
    except Exception as e:
        raise Exception(f"API调用失败: {str(e)}")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/crawl', methods=['POST'])
def handle_crawl():
    data = request.json
    url_key = data.get('url_key')
    custom_url = data.get('custom_url')
    
    # 验证 URL 是否合法
    if url_key:
        url = ALLOWED_URLS.get(url_key)
    elif custom_url and 'ieltsliz.com' in custom_url:  # 限制自定义域名
        url = custom_url
    else:
        return jsonify({'error': 'Invalid URL'})
    
    questions = crawl_questions(url)
    if questions is not None:
        return jsonify({'questions': questions})
    else:
        return jsonify({'error': '爬取失败,请检查URL或稍后重试'})

@app.route('/answer')
def answer():
    return render_template('answer.html')

@app.route('/api/evaluate', methods=['POST'])
def evaluate_essay():
    data = request.json
    question = data.get('question')
    essay = data.get('essay')
    
    if not all([question, essay]):
        return jsonify({'error': '缺少题目或作文内容'})
    
    # 构建评分提示词
    prompt = f"""
    请根据雅思写作评分标准对以下作文进行严谨批改（至少250词）：
    - 作文题目：{question}
    - 学生作文：{essay}
    
    要求返回JSON格式：
    {{
        "score": 分数（0-9）,
        "feedback": "从写作任务回应情况、连贯与衔接、词汇丰富程度、语法准确性、句子结构多样性等方面给出评价",
        "errors": ["语法错误1", "语法错误2", ...],
        "suggestions": ["哪些句子逻辑不清晰", "用词不当","高级替换","词汇替换" ...],
        "reference": "参考范文"
    }}
    """
    
    try:
        # 调用 Kimi API
        result = call_kimi_api(prompt)
        feedback_content = result.choices[0].message.content
        feedback_content = feedback_content.strip()
        feedback_content = re.sub(r'\s+', ' ', feedback_content)
        print("Kimi API Response:")
        print(feedback_content)
        # 解析 Kimi 的回复
        feedback_json = json.loads(feedback_content)
        print("Kimi API Response (JSON):")
        print(feedback_json)
        score = feedback_json.get('score')
        feedback = feedback_json.get('feedback')
        errors = feedback_json.get('errors', [])
        suggestions = feedback_json.get('suggestions', [])
        reference = feedback_json.get('reference', '')
        
        return jsonify({
            "score": score,
            "feedback": feedback,
            "errors": errors,
            "suggestions": suggestions,
            "reference": reference
        })

    except json.JSONDecodeError:
        return jsonify({'error': 'Kimi 返回的数据格式无效'})
    except KeyError as e:
        return jsonify({'error': f'解析 Kimi 响应失败: 缺少字段 {str(e)}'})
    except Exception as e:
        print(feedback_content)
        return jsonify({'error': f'API调用失败: {str(e)}'})

@app.route('/api/more_references', methods=['POST'])
def get_more_references():
    data = request.json
    question = data.get('question')
    
    if not question:
        return jsonify({'error': '缺少题目'})
    
    # 构建获取更多范文的提示词
    prompt2 = f"""
    请根据以下雅思作文题目生成一篇新的范文（至少250词）：
    - 作文题目：{question}
    
    要求返回严格的JSON格式:
    {{
        'reference2': '参考范文'
    }}
    """
    
    try:
        # 调用 Kimi API
        result2 = call_kimi_api(prompt2)
        feedback_content2 = result2.choices[0].message.content
        print("Kimi API Response2:")
        print(type(feedback_content2))
        # 解析 Kimi 的回复
        feedback_content2 = feedback_content2.strip()
        feedback_content2 = re.sub(r'\s+', ' ', feedback_content2)
        feedback_json2 = json.loads(feedback_content2)
        print("Kimi API Response2 (JSON):")
        print(type(feedback_json2))
        reference2 = feedback_json2.get('reference2', '')
        print("reference2:")
        print(reference2)
        
        return jsonify({
            "reference2": reference2
        })

    except json.JSONDecodeError:
        return jsonify({'error': 'Kimi 返回的数据格式无效'})
    except KeyError as e:
        return jsonify({'error': f'解析 Kimi 响应失败: 缺少字段 {str(e)}'})
    except Exception as e:
        return jsonify({'error': f'API调用失败: {str(e)}'})
    
if __name__ == '__main__':
    app.run(debug=True)