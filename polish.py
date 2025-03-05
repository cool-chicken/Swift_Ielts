def polish_essay(user_essay):
    sentences = user_essay.split(". ")
    polished_sentences = []
    for sentence in sentences:
        payload = {
            "model": "deepseek-chat",
            "messages": [
                {"role": "system", "content": "You are a professional IELTS essay polisher."},
                {"role": "user", "content": f"Polish the following sentence: {sentence}"}
            ],
            "stream": False
        }
        response = requests.post(f"{base_url}/chat/completions", headers=headers, data=json.dumps(payload))
        polished_sentences.append(response.json()["choices"][0]["message"]["content"])
    return ". ".join(polished_sentences)

# 示例调用
user_essay = "Your essay text here."
polished_essay = polish_essay(user_essay)
print(polished_essay)