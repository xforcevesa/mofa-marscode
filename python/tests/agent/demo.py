from mofa.run.run_agent import run_dspy_or_crewai_agent
from mofa.kernel.utils.util import load_agent_config
from mofa.run.run_agent import  run_dspy_or_crewai_agent
import dspy

from mofa.utils.download.arxiv_papers import arxiv_search_and_download

#
# from dsp import LM
# import requests
#
# from mofa.agent_build.reasoner.reasoner import ReasonerModule
#
# from dsp import LM
# import requests
# class SiliconFlowClient(LM):
#     def __init__(self, model:str, api_key:str, base_url:str=None):
#         self.model = model
#         self.api_key = api_key
#         if base_url is None:
#             base_url = "https://api.siliconflow.cn/v1/chat/completions"
#         self.base_url = base_url
#         self.history = []
#         self.kwargs = {"temperature":0.7}  # 初始化kwargs属性
#     def basic_request(self, prompt: str, **kwargs):
#         headers = {
#             "accept": "application/json",
#             "content-type": "application/json",
#             "authorization": f"Bearer {self.api_key}"
#         }
#         data = {
#             "model": self.model,
#             "messages": [
#                 {"role": "user", "content": prompt}
#             ],
#             "stream": False,
#             "max_tokens": kwargs.get("max_tokens", 512),
#             "temperature": kwargs.get("temperature", 0.7),
#             "top_p": kwargs.get("top_p", 0.7),
#             "top_k": kwargs.get("top_k", 50),
#             "frequency_penalty": kwargs.get("frequency_penalty", 0.5),
#             "n": kwargs.get("n", 1)
#         }
#         response = requests.post(self.base_url, headers=headers, json=data)
#         response = response.json()
#         self.history.append({
#             "prompt": prompt,
#             "response": response,
#             "kwargs": kwargs,
#         })
#         return response
#     def __call__(self, prompt, only_completed=True, return_sorted=False, **kwargs):
#         response = self.basic_request(prompt, **kwargs)
#         completions = [result.get('message').get("content") for result in response["choices"]]
#         return completions
# # 使用示例
# import dspy
# # 初始化自定义客户端
# silicon_flow_client = SiliconFlowClient(
#     model="deepseek-ai/DeepSeek-V2-Chat",
#     api_key="sk-",
#     base_url="https://api.siliconflow.cn/v1/chat/completions"
# )
# # 配置DSPy
# dspy.configure(lm=silicon_flow_client)
# # 生成响应
# response = silicon_flow_client(prompt="你好 你是谁？ ")
#
# agent_config =  {'agents': [{'name': 'reasoner', 'role': 'Knowledgeable Assistant', 'goal': 'You are an AI-powered assistant with access to a vast database of knowledge across multiple domains, including history, science, literature, and geography. Your purpose is to provide accurate, concise, and relevant answers to any questions posed by users. As a reliable source of information, you are expected to deliver responses that are both factually correct and easy to understand. Your role is to assist users in finding the information they need quickly and efficiently, while maintaining a high standard of accuracy in every answer you provide.', 'backstory': "Answer questions based on user's questions\n", 'verbose': True, 'allow_delegation': False, 'tools': None}], 'tasks': [{'description': '你是谁? ', 'expected_output': 'details', 'agent': 'reasoner', 'max_inter': 1, 'human_input': False}], 'model': {'model_api_key': ' ', 'model_name': 'gpt-4o-mini', 'model_max_tokens': 2048, 'module_api_url': None}, 'other': {'proxy_url': None}, 'env': {'SERPER_API_KEY': None, 'AGENTOPS_API_KEY': None}, 'crewai_config': {'memory': False}}
# reasoner = ReasonerModule(role=agent_config.get('role', ''), backstory=agent_config.get('backstory', ''),
#                                       context=agent_config.get('context', None), objective=agent_config.get('objective', None), specifics=agent_config.get('specifics', None),
#                                       actions=agent_config.get('actions', None), results=agent_config.get('results', None), example=agent_config.get('example', None), answer=agent_config.get('answer', None),
#                                       temperature=agent_config.get('temperature', 0.7), input_fields=agent_config.get('input_fields', None))
#
# agent_result = run_dspy_or_crewai_agent(agent_config)
# print(agent_result)
# answer = reasoner.forward(question="你是谁?", kwargs=agent_config.get('input_fields', {}))
# print(answer)
# from taskweaver.app.app import TaskWeaverApp

# inputs = {'role': 'Research Analyst', 'backstory': 'You are a highly skilled research analyst with extensive experience in interpreting and synthesizing complex academic research. You excel at identifying patterns, trends, and shifts in research focus. Your task is to delve into the provided summaries of research papers, identify the various strategies and ideas proposed by different authors.Address the issue by integrating your own comprehension.', 'objective': 'Your objective is to analyze summarized academic papers to understand the different approaches and ideas researchers have taken to enhance the capabilities of mixed large language models (LLMs). Specifically, you will:\n\nCreation Dates: Determine the creation dates of the papers to understand the timeline and relevance of the research.\nPrimary Authors: Identify the primary authors and assess their expertise and contributions to the field.\nMain Themes and Topics: Investigate the main themes and topics of each paper, focusing on the specific problems they aim to solve.\nMethodologies: Explore the methodologies used by different authors to address the problems, noting any innovative or unique approaches.\nEvolution of Research: Analyze how the focus of research has shifted over time, identifying any emerging trends or changes in approach.\nConstruct Narrative: Construct a clear and concise narrative that highlights the diversity of approaches, the evolution of research themes, and the progression of ideas over time.\n', 'example': "Task: 如何增强混合大语言模型的能力？\nAnswer:\n  Improve Pre-training Methods:\n\n  Knowledge Integration: During the pre-training process, integrate entity embeddings from knowledge bases, and combine entity linking loss with masked language modeling (MLM) loss to enhance the model's knowledge recall ability [2304.01597v1].\n  Self-supervised Learning: Utilize a larger scale of unlabeled data, and improve the model's language understanding and generation capabilities through self-supervised learning [2304.01597v1].\n", 'task': None, 'log_path': './data/output/log/paper_dataflow.md', 'log_type': 'markdown', 'log_step_name': 'report_writer_agent', 'model_api_key': '', 'model_name': 'deepseek-ai/DeepSeek-V2-Chat', 'model_api_url': 'https://api.siliconflow.cn/v1/chat/completions', 'proxy_url': None, 'agent_type': 'reasoner', 'max_iterations': 1, 'context': '[{"./data/output/arxiv_papers/2410.15489v1.pdf": "Answer:\\n\\nThe paper in question appears to be a comprehensive study on generative models and their applications, particularly in the field of robotics and computer vision. Here are the details synthesized from the provided data:\\n\\n1. **Creation Time**: The paper references various recent advancements and techniques, suggesting it was likely created around 2023-2024. Specific dates mentioned include 2023 and 2024 in the citations, indicating recent research contributions.\\n\\n2. **Main Author**: The main author of the paper is not explicitly named in the provided data. However, several authors are mentioned in the citations, such as Kangle Deng, Yuyang Deng, and Wee Kiat Chan, among others. These authors could be contributors or co-authors.\\n\\n3. **Research Methods**: The paper discusses various research methods including Variational Autoencoders (VAEs), Generative Adversarial Networks (GANs), and diffusion models. These methods are used for tasks like dimensionality reduction, data generation, and enhancing sensor data for robotics applications.\\n\\n4. **Abstract Summary**: The abstract likely summarizes the application of generative AI models across different levels of computing stacks in autonomous systems, emphasizing their role in enhancing data for downstream tasks and improving robotic capabilities through advanced AI techniques.\\n\\n5. **Practical Application Value**: The research results have significant practical application value, particularly in robotics where they enhance data processing capabilities and enable more sophisticated interactions with environments. The models discussed help in generating realistic data, improving motion planning, and enabling robots to respond to complex instructions effectively.\\n\\nThis synthesis primarily uses data from `rag_data`, supplemented by `llm_data`, ensuring a comprehensive and accurate response to the query."}, {"./data/output/arxiv_papers/2307.06152v1.pdf": "Answer: The creation time of the paper is not explicitly mentioned, but it references research trends since 2018, indicating a relatively recent publication. The main author of the paper is not clearly identified from the provided data. The research methods or techniques used in the paper include Variational Autoencoders (VAEs), Reinforcement Learning (RL), and possibly Asymmetric Self-Play. The abstract content summary is not directly available, but it discusses the application of generative models in various fields such as robotics and computer vision, emphasizing their role in enhancing data for downstream tasks and augmenting sensor-rich datasets. The practical application value of the research results in the paper lies in improving decision-making capabilities in autonomous systems, particularly in air combat scenarios, through advanced AI techniques like RL and generative models."}, {"./data/output/arxiv_papers/2310.06775v2.pdf": "Answer:\\n\\nThe creation time of the paper is not explicitly mentioned in the provided data. The main author of the paper is not clearly identified, but it mentions a participatory design approach involving direct researcher input and critique during the ACE framework elaboration. The research methods or techniques used in the paper include a participatory design approach and the classification of memory into episodic and declarative categories. The abstract content summary is not provided, but it discusses advancements in fields such as robotics and the development of a systematic framework for AI implementation. The practical application value of the research results includes enhancing decision-making capabilities in fields like air combat and providing a framework for developing capable and beneficial AI systems."}]'}
# x = """1. AI agents, intelligent agents, autonomous systems
# 2. machine learning, reinforcement learning, decision-making
# 3. natural language processing, conversational agents, AI interaction""".split(',')
# download_data = arxiv_search_and_download(query=x, max_results=1, days_back=365 * 3,download_dir='.')
# print(download_data)

# inputs = {'role': 'Research Analyst', 'backstory': 'You are a highly skilled research analyst with extensive experience in interpreting and synthesizing complex academic research. You excel at identifying patterns, trends, and shifts in research focus. Your task is to delve into the provided summaries of research papers, identify the various strategies and ideas proposed by different authors.Address the issue by integrating your own comprehension.', 'objective': 'Your objective is to analyze summarized academic papers to understand the different approaches and ideas researchers have taken to enhance the capabilities of mixed large language models (LLMs). Specifically, you will:\n\nCreation Dates: Determine the creation dates of the papers to understand the timeline and relevance of the research.\nPrimary Authors: Identify the primary authors and assess their expertise and contributions to the field.\nMain Themes and Topics: Investigate the main themes and topics of each paper, focusing on the specific problems they aim to solve.\nMethodologies: Explore the methodologies used by different authors to address the problems, noting any innovative or unique approaches.\nEvolution of Research: Analyze how the focus of research has shifted over time, identifying any emerging trends or changes in approach.\nConstruct Narrative: Construct a clear and concise narrative that highlights the diversity of approaches, the evolution of research themes, and the progression of ideas over time.\n', 'example': "Task: 如何增强混合大语言模型的能力？\nAnswer:\n  Improve Pre-training Methods:\n\n  Knowledge Integration: During the pre-training process, integrate entity embeddings from knowledge bases, and combine entity linking loss with masked language modeling (MLM) loss to enhance the model's knowledge recall ability [2304.01597v1].\n  Self-supervised Learning: Utilize a larger scale of unlabeled data, and improve the model's language understanding and generation capabilities through self-supervised learning [2304.01597v1].\n", 'task': None, 'log_path': './data/output/log/paper_dataflow.md', 'log_type': 'markdown', 'log_step_name': 'report_writer_agent', 'model_api_key': '', 'model_name': 'deepseek-ai/DeepSeek-V2-Chat', 'model_api_url': 'https://api.siliconflow.cn/v1/chat/completions', 'proxy_url': None, 'agent_type': 'reasoner', 'max_iterations': 1, 'context': '[{"./data/output/arxiv_papers/2410.15489v1.pdf": "Answer:'}
# agent_result = run_dspy_or_crewai_agent(agent_config=inputs)
# print(agent_result)

