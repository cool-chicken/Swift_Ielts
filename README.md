# Swift_Ielts 🎓✍️

### 这是一个为雅思备考同学设计的大作文智能批改程序

## 项目简介 📚

Swift_Ielts 是一个基于 Flask 框架的 Web 应用程序，旨在帮助雅思备考的同学进行大作文的智能批改。用户可以提交自己的作文，系统会根据雅思写作评分标准进行批改，并提供详细的反馈和建议。

## 功能特性 ✨

- **作文批改**：根据雅思写作评分标准对用户提交的作文进行批改，提供评分、反馈、语法错误和建议。
- **参考范文**：提供参考范文，帮助用户更好地理解和改进自己的作文。
- **更多范文**：用户可以获取更多的参考范文，进一步提升写作水平。

## 安装与运行 🚀

### 环境要求 🛠️

- Python 3.8+
- Flask
- Flask-CORS
- BeautifulSoup4
- Requests
- OpenAI

### 安装步骤 📥

1. 克隆项目到本地：
    ```sh
    git clone https://github.com/yourusername/Swift_Ielts.git
    cd Swift_Ielts
    ```

2. 创建并激活虚拟环境：
    ```sh
    python -m venv venv
    source venv/bin/activate  # 对于 Windows 用户，使用 `venv\Scripts\activate`
    ```

3. 安装依赖包：
    ```sh
    pip install -r requirements.txt
    ```

4. 设置环境变量：
    ```sh
    export KIMI_API_KEY="your_actual_api_key_here"
    ```
    申请步骤：
    1. 访问 <a href="https://platform.moonshot.cn/console/api-keys" style="color:blue;">Moonshot API Keys</a>
    2. 新建 API Key
    3. 将 API Key 复制到 your_actual_api_key_here处

5. 运行应用程序：
    ```sh
    python fetch.py
    ```

6. 在浏览器中打开 <a href="http://127.0.0.1:5000" style="color:green;">http://127.0.0.1:5000</a> 访问应用程序。

## 使用说明 📖

1. 打开应用程序后，选择或输入作文题目。
2. 在文本框中输入你的作文内容。
3. 点击“提交批改”按钮，系统会对你的作文进行批改，并显示评分和反馈。
4. 点击“更多范文”按钮，可以获取更多的参考范文。

## 文件结构 🗂️

```
Swift_Ielts/
│
├── static/
│   ├── styles.css          # 样式文件
│
├── templates/
│   ├── index.html          # 主页面
│   ├── answer.html         # 作文批改页面
│
├── fetch.py                # 主应用程序文件
├── requirements.txt        # 依赖包列表
├── README.md               # 项目说明文件
```

## 贡献指南 🤝

欢迎对本项目进行贡献！如果你有任何建议或发现了问题，请提交 issue 或 pull request。

## 许可证 📄

本项目采用 MIT 许可证。详情请参阅 LICENSE 文件。