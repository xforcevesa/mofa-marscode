import os
from dotenv import load_dotenv  # 用于加载 .env 文件
from openai import OpenAI
from prompt import think_base_prompt

class RequirementClarificationAgent:
    def __init__(self, api_key: str, base_url: str):
        # 初始化 OpenAI 客户端
        self.client = OpenAI(api_key=api_key, base_url = base_url)
        self.base_prompt = think_base_prompt
        self.conversation_history = []  # 用于记录历史对话
        self.final_json = {} # 保存最终结果

    def generate_message(self, user_input: str) -> list:
        """
        生成发送到 API 的消息列表，包括角色、上下文和用户输入。
        """
        # 将用户输入加入历史记录
        self.conversation_history.append({"role": "user", "content": user_input})
        
        # 构建消息
        messages = [{"role": "system", "content": self.base_prompt}]
        messages.extend(self.conversation_history)  # 包含所有历史对话
        return messages

    def send_request(self, messages: list) -> str:
        """
        向 OpenAI 第三方 API 发送请求并返回模型的响应。
        """
        response = self.client.chat.completions.create(
            model='deepseek-ai/DeepSeek-V2.5',
            messages=messages,
            stream=True  # 开启流式返回
        )
        
        # 收集流式返回结果
        assistant_message = ""
        for chunk in response:
            delta = chunk.choices[0].delta.content
            if delta:
                assistant_message += delta
                print(delta, end='')  # 实时打印输出
        print() 

        # 将模型回复存入历史记录
        self.conversation_history.append({"role": "assistant", "content": assistant_message})
        return assistant_message

    def extract_json(self, llm_output: str) -> dict:
        """
        从 LLM 的输出中提取 JSON 对象。
        """
        try:
            start_idx = llm_output.find("{")
            end_idx = llm_output.rfind("}") + 1
            if start_idx != -1 and end_idx != -1:
                return eval(llm_output[start_idx:end_idx])
        except Exception as e:
            print(f"Error extracting JSON: {e}")
        return None

    def run(self):
        """
        主对话循环。
        """
        print("Agent: Hi there! How can I help you today?")
        while True:
            user_input = input("You: ")
            if user_input.lower() in ["done", "finish", "完成", "是的", "yes"]:
                if self.final_json:
                    print(f"Agent: Here's the finalized JSON:\n{self.final_json}")
                else:
                    print("Agent: It seems we haven't finalized the requirements yet.")
                break
            
            # 生成消息和请求
            messages = self.generate_message(user_input)
            llm_output = self.send_request(messages)
            
            # 尝试提取 JSON
            json_data = self.extract_json(llm_output)
            if json_data:
                self.final_json = json_data
                print("Agent: Does this JSON look correct? If so, type 'done' to finish.")

if __name__ == "__main__":
    # 加载环境变量
    load_dotenv()
    api_key = os.getenv("API_KEY")
    base_url = os.getenv("BASE_URL")

    if not api_key or not base_url:
        print("Error: Missing API_KEY or BASE_URL environment variable.")
        exit(1)

    # 创建并运行对话代理
    agent = RequirementClarificationAgent(api_key=api_key, base_url=base_url)
    agent.run()

