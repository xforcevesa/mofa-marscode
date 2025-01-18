import os
from typing import List
from dotenv import load_dotenv
from openai import OpenAI
from pydantic import BaseModel,Field

def load_llm_api_key_by_env_file(dotenv_path: str='.env.secret.1',) -> str:
    load_dotenv(dotenv_path)
    api_key = os.getenv('OPENAI_API_KEY',None)
    if api_key is None:
        api_key = os.getenv('API_KEY',None)
    return api_key

def create_openai_client(api_key: str=load_llm_api_key_by_env_file(),*args,**kwargs) -> OpenAI:
    client = OpenAI(api_key=api_key, base_url = "https://ark.cn-beijing.volces.com/api/v3", **kwargs)
    return client

def generate_json_from_llm(client, format_class: BaseModel, prompt: str = None, messages: List[dict] = None,
                           supplement_prompt: str = None, model_name: str = "ep-20250117172626-95vzs") -> str:
    if messages is None:
        messages = [
            {"role": "system",
             "content": "You are a professional Ai assistant"},
            {"role": "user", "content": prompt},
        ]
    if supplement_prompt is not None:
        messages.append({"role": "user", "content": supplement_prompt})
    completion = client.beta.chat.completions.parse(
        model=model_name,
        messages=messages,
        response_format=format_class,
    )
    return completion.choices[0].message.parsed

