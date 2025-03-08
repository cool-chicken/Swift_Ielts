from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
from bs4 import BeautifulSoup
import requests
import os
import json

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
KIMI_API_URL = "https://api.moonshot.com/v1/chat/completions"

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
        headers = {
            "Authorization": f"Bearer {KIMI_API_KEY}",
            "Content-Type": "application/json"
        }
        response = requests.post(
            KIMI_API_URL,
            headers=headers,
            json={
                "model": "moonshot-v1-8k",
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.3
            },
            timeout=30,
            verify=False
        )
        response.raise_for_status()
        return response.json()
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
        return jsonify({'error': '爬取失败，请检查URL或稍后重试'})

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
    请根据雅思写作评分标准对以下作文进行批改：
    - 作文题目：{question}
    - 学生作文：{essay}
    
    要求返回JSON格式：
    {{
        "score": 分数（0-9）,
        "feedback": "详细批改建议",
        "errors": ["语法错误1", "语法错误2", ...],
        "suggestions": ["哪些句子逻辑不清晰", "用词不当","高级替换","词汇替换" ...],
        "reference1": "参考范文1",
        “reference2”: "参考范文2"
    }}
    """
    
    try:
        # 调用 Kimi API
        result = call_kimi_api(prompt)
        feedback_content = result['choices'][0]['message']['content']
        
        # 解析 Kimi 的回复
        feedback_json = json.loads(feedback_content)
        score = feedback_json.get('score')
        feedback = feedback_json.get('feedback')
        errors = feedback_json.get('errors', [])
        suggestions = feedback_json.get('suggestions', [])
        reference1 = feedback_json.get('reference1', '')
        reference2 = feedback_json.get('reference2', '')
        
        return jsonify({
            "score": score,
            "feedback": feedback,
            "errors": errors,
            "suggestions": suggestions,
            "reference1": reference1,
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