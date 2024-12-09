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
import requests
import json

# HACK: assume that there is a cookie file
COOKIE_FILE = 'www.bestbuy.com.json'

class Product(BaseModel):
    name: str = None
    price: str = None
    description: str = None
    image_url: str = None

class BestBuySearchText(BaseModel):
    products: List[Product] = None

    # load cookie file
def add_driver_cookies(driver, cookie_file_path):
    if os.path.exists(cookie_file_path):
        with open(cookie_file_path, 'r') as f:
            cookies = json.load(f)
            for cookie in cookies:
                driver.add_cookie(cookie)
    return driver

def login_bestbuy(search_text: str, url: str = 'https://www.bestbuy.com/'):
    driver = uc.Chrome(headless=False, use_subprocess=False)
    driver.get(url)
    driver = add_driver_cookies(driver=driver, cookie_file_path=COOKIE_FILE)
    driver.refresh()
    print("Waiting for user to click")
    time.sleep(random.choice([1, 6]))

    # choose America
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, 'body > div.page-container > div > div > div > div:nth-child(1) > div.country-selection > a.us-link > img'))
    ).click()

    # waiting for search box load compelete
    search_box = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, 'gh-search-input'))
    )
    search_box.send_keys(search_text + Keys.RETURN)

    time.sleep(random.choice([1, 4]))
    html_source = driver.page_source
    driver.close()
    return html_source

def clean_html_js_and_style(html_content: str) -> str:
    soup = BeautifulSoup(html_content, 'html.parser')
    for tag in soup(['script', 'style']):
        tag.decompose()
    clean_html = str(soup)
    return clean_html


# HACK
def estimate_tokens(content, model='gpt-4'):
    encoding = tiktoken.encoding_for_model(model)
    return len(encoding.encode(content))

def split_html_content(html_content, max_tokens_per_chunk, model='gpt-4'):
    encoding = tiktoken.encoding_for_model(model)
    soup = BeautifulSoup(html_content, 'html.parser')

    chunks = []
    current_chunk = ''
    current_tokens = 0

    def process_node(node):
        nonlocal current_chunk, current_tokens, chunks

        if isinstance(node, NavigableString):
            text = str(node)
            tokens = len(encoding.encode(text))

            if current_tokens + tokens > max_tokens_per_chunk:
                if current_chunk.strip():
                    chunks.append(current_chunk)
                current_chunk = ''
                current_tokens = 0

            current_chunk += text
            current_tokens += tokens

        elif isinstance(node, Tag):
            start_tag = f'<{node.name}'
            for attr, value in node.attrs.items():
                if isinstance(value, list):
                    value = ' '.join(value)
                start_tag += f' {attr}="{value}"'
            start_tag += '>'
            end_tag = f'</{node.name}>'

            start_tag_tokens = len(encoding.encode(start_tag))
            end_tag_tokens = len(encoding.encode(end_tag))

            prev_chunk = current_chunk
            prev_tokens = current_tokens

            if current_tokens + start_tag_tokens > max_tokens_per_chunk:
                if current_chunk.strip():
                    chunks.append(current_chunk)
                current_chunk = ''
                current_tokens = 0

            current_chunk += start_tag
            current_tokens += start_tag_tokens

            for child in node.contents:
                process_node(child)

            if current_tokens + end_tag_tokens > max_tokens_per_chunk:
                if current_chunk.strip():
                    current_chunk += end_tag
                    chunks.append(current_chunk)
                else:
                    current_chunk = start_tag + end_tag
                    chunks.append(current_chunk)
                current_chunk = ''
                current_tokens = 0
            else:
                current_chunk += end_tag
                current_tokens += end_tag_tokens

    root = soup.body if soup.body else soup
    for element in root.contents:
        process_node(element)

    if current_chunk.strip():
        chunks.append(current_chunk)

    return chunks

def process_large_html_content(llm_client, html_content: str, search_text: str = '', max_total_tokens=128000, model='gpt-4'):
    total_tokens = estimate_tokens(html_content, model=model)

    if total_tokens <= max_total_tokens:
        prompt = f"""Backstory:
            You are interacting with an HTML webpage that displays content resulting from a keyword search. The webpage contains various pieces of main content that need to be extracted and utilized.

            Objective:

            To extract all the main content from the current HTML webpage in the exact order it appears, and display it accordingly.

            Specifics:

            The content originates from a search result for a specific keyword.
            All main content elements such as text, images, and links should be included.
            The original order of content on the webpage must be preserved.
            Exclude any irrelevant elements like advertisements or navigation menus.
            Tasks:

            Analyze the HTML structure of the webpage.
            Identify and extract all main content elements.
            Organize the extracted content in the sequence it appears on the page.
            Prepare the content for display or further processing.
            Actions:

            Parse the HTML document to access the DOM structure.
            Locate the containers or elements that hold the main content.
            Extract the text, images, and links from these elements.
            Maintain the sequence by organizing content as per their order in the HTML.
            Format the extracted content for clear presentation.
            Results:

            A compiled list of all main content from the webpage, organized sequentially.
            The content is ready for display or can be used for additional processing tasks.
            The extracted data accurately reflects the information presented on the webpage after the keyword search. 

            This is Html source {html_content}

            Search Keyword: {search_text}
            """
        response = use_llm_return_json(llm_client=llm_client, prompt=prompt, format_class=BestBuySearchText)
        print("处理内容未超出 token 限制。")
        return response
    else:
        print("内容超出 token 限制，正在拆分为多个块。")
        max_tokens_per_chunk = max_total_tokens - 10000
        chunks = split_html_content(html_content, max_tokens_per_chunk, model=model)
        result = []
        for i in chunks:
            prompt = f"""Backstory:
                        You are interacting with an HTML webpage that displays content resulting from a keyword search. The webpage contains various pieces of main content that need to be extracted and utilized.

                        Objective:

                        To extract all the main content from the current HTML webpage in the exact order it appears, and display it accordingly.

                        Specifics:

                        The content originates from a search result for a specific keyword.
                        All main content elements such as text, images, and links should be included.
                        The original order of content on the webpage must be preserved.
                        Exclude any irrelevant elements like advertisements or navigation menus.
                        Tasks:

                        Analyze the HTML structure of the webpage.
                        Identify and extract all main content elements.
                        Organize the extracted content in the sequence it appears on the page.
                        Prepare the content for display or further processing.
                        Actions:

                        Parse the HTML document to access the DOM structure.
                        Locate the containers or elements that hold the main content.
                        Extract the text, images, and links from these elements.
                        Maintain the sequence by organizing content as per their order in the HTML.
                        Format the extracted content for clear presentation.
                        Results:

                        A compiled list of all main content from the webpage, organized sequentially.
                        The content is ready for display or can be used for additional processing tasks.
                        The extracted data accurately reflects the information presented on the webpage after the keyword search. 

                        This is Html source {i}

                        Search Keyword: {search_text}
                        """
            response = use_llm_return_json(llm_client=llm_client, prompt=prompt, format_class=BestBuySearchText)
            result.append(response)

        return result

def use_llm_return_json(llm_client, prompt: str, format_class, supplement_prompt: str = None,
                        model_name: str = 'gpt-4', image_data: str = None) -> str:
    prompt_data = [
        {
            "type": "text",
            "text": prompt
        },
    ]

    if image_data is not None:
        prompt_data.append({
            "type": "image_url",
            "image_url": {
                "url": f"data:image/jpeg;base64,{image_data}"
            }
        })

    response = llm_client.beta.chat.completions.parse(
        model=model_name,
        messages=[
                        {
                            "role": "user",
                            "content": prompt_data
                        }
                    ],
        response_format=format_class,

    )
    return response.choices[0].message.parsed

if __name__ == '__main__':
    search_text = 'mac mini m4'
    html_source = login_bestbuy(search_text=search_text)
    clean_html_source = clean_html_js_and_style(html_source)
    # HACK 
    api_key = "sk-"
    client = OpenAI(api_key=api_key)
    result = process_large_html_content(html_content=clean_html_source, llm_client=client, search_text=search_text)
    print(result)
