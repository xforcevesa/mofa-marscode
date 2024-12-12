import os
from typing import List
from dotenv import load_dotenv
from openai import OpenAI
from pydantic import BaseModel,Field

def load_llm_api_key_by_env_file(dotenv_path: str='.env.secret',) -> str:
    load_dotenv(dotenv_path)
    api_key = os.getenv('OPENAI_API_KEY')
    return api_key

def create_openai_client(api_key: str=load_llm_api_key_by_env_file(),*args,**kwargs) -> OpenAI:
    print(f"======kwargs:{kwargs}======")
    client = OpenAI(api_key=api_key,**kwargs)
    return client

def generate_json_from_llm(client, format_class: BaseModel, prompt: str = None, messages: List[dict] = None,
                           supplement_prompt: str = None, model_name: str = 'gpt-4o-mini') -> str:
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

