from openai import OpenAI

import requests

# 目标 URL
url = 'http://user-105.openllm.io/lab/v1/hello'

# 发送 GET 请求
response = requests.get(url)

# 检查响应状态码
if response.status_code == 200:
    # 请求成功，打印内容
    print(response.text)
else:
    # 请求失败，打印错误信息
    print('Failed to retrieve the webpage')


client = OpenAI(base_url="http://user-105.openllm.io/v1/hello", api_key="sk-8e56efe55f497afd")
# client = OpenAI(base_url="http://localhost:8000/v1", api_key="sk-8e56efe55f497afd")


def list_models():
    try:
        models = client.models.list()
        print("Available models:")
        for model in models.data:
            print(f"- {model.id}")
    except Exception as e:
        print(f"Error listing models: {e}")


def chat_completion(user_input):
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": user_input},
            ],
        )
        print("Chat Completion Response:")
        print(response.choices[0].message.content)
    except Exception as e:
        print(f"Error in chat completion: {e}")


if __name__ == "__main__":
    print("Testing API endpoints...")
    list_models()
    print("\n" + "=" * 50 + "\n")

    chat_input = input("Enter a message for chat completion: ")
    chat_completion(chat_input)
    print("\n" + "=" * 50 + "\n")
