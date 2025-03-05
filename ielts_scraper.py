import os
import requests
from bs4 import BeautifulSoup
import configparser

# 加载配置文件
config = configparser.ConfigParser()
config.read('config.ini')

BASE_URL = config['SETTINGS']['BASE_URL']
STORAGE_PATH = config['SETTINGS']['STORAGE_PATH']

def fetch_essay_questions(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # 检查请求是否成功
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 假设题目存储在特定的HTML标签中，例如 <div class="question">
        questions = [q.text.strip() for q in soup.select('div.question')]
        
        return questions
    except requests.exceptions.RequestException as e:
        print(f"Error fetching questions: {e}")
        return []

def save_questions(questions, storage_path):
    # 确保存储目录存在
    os.makedirs(storage_path, exist_ok=True)
    
    # 以时间戳命名文件
    filename = os.path.join(storage_path, f"questions_{datetime.now().strftime('%Y%m%d%H%M%S')}.txt")
    
    with open(filename, 'w', encoding='utf-8') as f:
        for question in questions:
            f.write(question + "\n")

if __name__ == "__main__":
    questions = fetch_essay_questions(BASE_URL)
    if questions:
        save_questions(questions, STORAGE_PATH)
        print(f"Successfully saved {len(questions)} questions.")
    else:
        print("No questions found.")