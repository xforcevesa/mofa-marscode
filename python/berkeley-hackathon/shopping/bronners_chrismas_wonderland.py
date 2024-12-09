import undetected_chromedriver as uc
import time
import random
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import tiktoken
from typing import List
from openai import OpenAI
from pydantic import BaseModel
import os
import json
from dotenv import load_dotenv

load_dotenv('.env.secret')

COOKIE_FILE = 'www.bronners.com.json'

class Product(BaseModel):
    name: str = None
    price: str = None
    description: str = None
    image_url: str = None

class BronnersSearchText(BaseModel):
    products: List[Product] = None

def add_driver_cookies(driver, cookie_file_path):
    pass

def save_driver_cookies(driver, cookie_file_path):
    pass

def login_bronners(search_text: str, url: str = 'https://www.bronners.com/'):
    pass

def clean_html_js_and_style(html_content: str) -> str:
    pass

def estimate_tokens(content, model='gpt-4'):
    pass

def split_html_content(html_content, max_tokens_per_chunk, model='gpt-4'):
    pass

def process_large_html_content(llm_client, html_content: str, search_text: str = '', max_total_tokens=128000, model='gpt-4'):
    pass

def use_llm_return_json(llm_client, prompt: str, format_class, supplement_prompt: str = None,
                        model_name: str = 'gpt-4', image_data: str = None) -> str:
    pass

if __name__ == '__main__':
    search_text = 'Christmas'
    html_source = login_bronners(search_text=search_text)
    clean_html_source = clean_html_js_and_style(html_source)
    api_key = os.getenv('OPENAI_API_KEY')
    client = OpenAI(api_key=api_key)
    result = process_large_html_content(html_content=clean_html_source, llm_client=client, search_text=search_text)
    print(result)
