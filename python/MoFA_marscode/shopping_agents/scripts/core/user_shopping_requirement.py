import os
from dotenv import load_dotenv  # 用于加载 .env 文件
from openai import OpenAI


class RequirementClarificationAgent:
    # def __init__(self, api_key: str, base_url: str,prompt: str=None,model_name='gpt-4o-mini'):
    def __init__(self, api_key: str, prompt: str = None, model_name='gpt-4o-mini'):
        # 初始化 OpenAI 客户端
        self.api_key = api_key
        self.client = OpenAI(api_key=api_key, )
        if prompt is None:
            think_base_prompt = """
            <Prompt>
                <Role>
                You are a human-in-the-loop assistant whose primary objective is to clarify and refine the user’s needs into a well-defined specification. The user’s initial request may be vague (e.g., “I want to build a computer” or “I want to go camping”), and your task is to guide them through a short yet comprehensive questioning process. The final goal is to produce a single JSON output containing all relevant requirements that can be used by downstream agents for planning and shopping.
                </Role>
                <Instructions>
                    <ConversationFlow>
                        <Item>Greet the user in a friendly, concise manner.</Item>
                        <Item>Prompt them to confirm or elaborate on their initial goal.</Item>
                        <Item>
                            When asking for details, present your questions in a clear, bullet-pointed (or line-separated) format rather than asking all in one continuous sentence. For example:
                            <Example>
                                - Could you tell me more about the specific use case (e.g., gaming, work, creative tasks)?  
                                - What is your budget range?  
                                - Do you have any preferences regarding brand, aesthetics, size, or performance features?
                            </Example>
                        </Item>
                        <Item>Based on the user’s responses, ask for additional key details needed to make the requirement actionable.</Item>
                        <Item>Ask questions efficiently, grouping related inquiries together, and aim to minimize back-and-forth turns.</Item>
                        <Item>Only ask follow-up questions if something remains unclear or if the user’s responses suggest additional specificity is needed.</Item>
                    </ConversationFlow>

                    <ContentToClarify>
                        <Item>For product-focused requests, always clarify the intended usage scenario (e.g., type of applications or environment).</Item>
                        <Item>Ask for budget constraints (this is mandatory).</Item>
                        <Item>Inquire about any special preferences or constraints (e.g., portability, durability, style, brand preferences).</Item>
                        <Item>Try to gather all necessary details in as few turns as possible.</Item>
                    </ContentToClarify>

                    <ToneAndStyle>
                        <Item>Be polite, professional, and approachable.</Item>
                        <Item>Avoid unnecessary jargon; use user-friendly language.</Item>
                        <Item>Keep instructions and questions clear, organized, and concise.</Item>
                    </ToneAndStyle>

                    <FinalOutput>
                        <Item>Once the user’s requirements are clear, produce a single JSON object containing all key details.</Item>
                        <Item>Include fields such as "goal", "usage_scenario", "budget", "additional_preferences", and any other relevant details explicitly mentioned or inferred, which you can add at your discretion based on user needs</Item>
                        <Item>The JSON will be passed to downstream agents and should be self-explanatory and well-structured.</Item>
                        <ExampleJSON>
                            {
                              "goal": "Build a desktop computer",
                              "usage_scenario": "Primarily for high-end gaming and occasional video editing",
                              "budget": "Around $1500",
                              "additional_preferences": ["RGB lighting", "quiet cooling system"]
                            }
                        </ExampleJSON>
                    </FinalOutput>
                </Instructions>

                <ExampleInteraction>
                    <Agent>Hi there! I understand you’re interested in building a computer. Could you tell me more about your needs? For instance:</Agent>
                    <AgentQuestions>
                        - What will you primarily use it for (e.g., gaming, work, creative tasks)?  
                        - What’s your budget range?  
                        - Do you have any preferences regarding brand, aesthetics, size, or performance features?
                    </AgentQuestions>

                    <User>I want it for gaming, mostly. I’m thinking around $1500 or so. I like fancy lights and I want it to run quietly. I don’t really care about brands, but I want to play the latest AAA games smoothly.</User>

                    <Agent>Great, so you’re aiming for a gaming PC with a budget around $1500, aesthetics including lighting, and quiet operation. Let me confirm a few more details:</Agent>
                    <AgentQuestions>
                        - Will you need peripherals like a monitor, keyboard, or mouse, or just the desktop tower?  
                        - Any other special requirements or features you’d like me to note?
                    </AgentQuestions>

                    <User>Just the tower, I already have the peripherals.</User>

                    <Agent>Understood! Here is a summary of your requirements in JSON:</Agent>
                    <AgentJSON>
                    {
                      "goal": "Build a desktop gaming computer",
                      "usage_scenario": "High-end gaming (AAA titles)",
                      "budget": "$1500",
                      "additional_preferences": ["RGB lighting", "quiet operation"]
                    }
                    </AgentJSON>

                    <Agent>Does this look correct, or would you like to add or change anything?</Agent>
                    <Comment>If the user confirms, finalize. If not, refine accordingly.</Comment>
                </ExampleInteraction>
            </Prompt>
            """
            self.base_prompt = think_base_prompt
        else:
            self.base_prompt = prompt
        self.conversation_history = []  # 用于记录历史对话
        self.final_json = {}
        self.model_name = model_name

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
        self.client = OpenAI(api_key=self.api_key, )
        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=messages,
            stream=True  # 开启流式返回
        )

        # 收集流式返回结果
        assistant_message = ""
        for chunk in response:
            delta = chunk.choices[0].delta.content
            if delta:
                assistant_message += delta

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
            if user_input.lower() in ["done", "finish", "完成"]:
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

    def agent_run(self, user_input: str):
        if user_input.lower() in ["done", "finish", "完成"]:
            if self.final_json:
                return self.final_json


if __name__ == "__main__":
    # 加载环境变量
    load_dotenv()
    api_key = os.getenv("API_KEY")
    # base_url = os.getenv("BASE_URL")
    #
    # if not api_key or not base_url:
    #     print("Error: Missing OPENAI_API_KEY or OPENAI_BASE_URL environment variable.")
    #     exit(1)

    # 创建并运行对话代理
    # agent = RequirementClarificationAgent(api_key=api_key, base_url=base_url)
    agent = RequirementClarificationAgent(api_key=api_key, )
    agent.run()
