import undetected_chromedriver as uc
import time
import requests
from bs4 import BeautifulSoup
from typing import List, Dict
import tiktoken
from pydantic import BaseModel
from typing import List, Optional
import json

# Define data models
class Media(BaseModel):
    images: List[str] = None
    videos: List[str] = None

class HtmlSearchTextChunk(BaseModel):
    url: str = None
    description: str = None
    media: List[Media] = None
    topic: str = None
    model_name: str = None
    price: str = None
    model_size: str = None

class HtmlSearchText(BaseModel):
    chunks: List[HtmlSearchTextChunk] = None

# Estimate token count
def estimate_tokens(content: str, model: str = 'gpt-4') -> int:
    encoding = tiktoken.encoding_for_model(model)
    return len(encoding.encode(content))

# Split HTML content into chunks
def split_html_content(html_content: str, max_tokens_per_chunk: int, model: str = 'gpt-4') -> List[str]:
    encoding = tiktoken.encoding_for_model(model)
    soup = BeautifulSoup(html_content, 'html.parser')
    chunks = []
    current_chunk = ''
    current_tokens = 0

    def process_node(node):
        nonlocal current_chunk, current_tokens, chunks

        if isinstance(node, str):
            text = node
            tokens = len(encoding.encode(text))
            if current_tokens + tokens > max_tokens_per_chunk:
                chunks.append(current_chunk)
                current_chunk = ''
                current_tokens = 0
            current_chunk += text
            current_tokens += tokens

        elif node.name:
            start_tag = f"<{node.name}"
            for attr, value in node.attrs.items():
                start_tag += f' {attr}="{value}"'
            start_tag += ">"
            end_tag = f"</{node.name}>"

            start_tag_tokens = len(encoding.encode(start_tag))
            end_tag_tokens = len(encoding.encode(end_tag))

            if current_tokens + start_tag_tokens > max_tokens_per_chunk:
                chunks.append(current_chunk)
                current_chunk = ''
                current_tokens = 0

            current_chunk += start_tag
            current_tokens += start_tag_tokens

            for child in node.children:
                process_node(child)

            if current_tokens + end_tag_tokens > max_tokens_per_chunk:
                chunks.append(current_chunk)
                current_chunk = ''
                current_tokens = 0
            current_chunk += end_tag
            current_tokens += end_tag_tokens

    for element in soup.body.children:
        process_node(element)

    if current_chunk.strip():
        chunks.append(current_chunk)

    return chunks

# Use DeepSeek API to parse HTML
def use_deepseek_return_json(prompt: str, api_key: str, model_name: str = 'deepseek-ai/DeepSeek-V2.5') -> str:
    url = "https://api.siliconflow.cn/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": model_name,
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ],
        "stream": False,
        "max_tokens": 512,
        "temperature": 0.7,
        "top_p": 0.7,
        "top_k": 50,
        "frequency_penalty": 0.5,
        "n": 1,
        "response_format": {"type": "text"},
        "tools": []
    }

    response = requests.post(url, json=payload, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"DeepSeek API call failed: {response.status_code}, {response.text}")
        return None

# Process large HTML content
def process_large_html_content(html_content: str, search_text: str, api_key: str, max_total_tokens: int = 32768, model: str = 'gpt-4'):
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
        response = use_deepseek_return_json(prompt=prompt, api_key=api_key)
        print("Content processed within token limit.")
        return response
    else:
        print("Content exceeds token limit, splitting into chunks.")
        max_tokens_per_chunk = max_total_tokens - 10000
        chunks = split_html_content(html_content, max_tokens_per_chunk, model=model)
        result = []
        for chunk in chunks:
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

                        This is Html source {chunk}

                        Search Keyword: {search_text}
                        """
            response = use_deepseek_return_json(prompt=prompt, api_key=api_key)
            if response:
                result.append(response)
            time.sleep(1)  # Add delay to avoid rate limit

        return result

# Fetch HTML content using undetected_chromedriver
def fetch_html_with_undetected_chromedriver(search_text: str, page: int = 1) -> str:
    driver = uc.Chrome()
    url = f"https://www.bronners.com/search?page={page}&keywords={search_text}"
    driver.get(url)
    time.sleep(5)
    html_content = driver.page_source
    driver.quit()
    return html_content

# Main process
if __name__ == '__main__':
    search_text = "Christmas ornaments"
    api_key = "sk-xubbnxwynyifmltibdrljlwoejjlxixhdwlwajmchzikgkga"

    html_content = fetch_html_with_undetected_chromedriver(search_text)
    result = process_large_html_content(html_content=html_content, search_text=search_text, api_key=api_key)

    # Save the result to a JSON file
    if result:
        with open("parsed_results.json", "w", encoding="utf-8") as json_file:
            json.dump(result, json_file, ensure_ascii=False, indent=4)
        print("Parsed results saved to 'parsed_results.json'.")
    else:
        print("No valid parsed results obtained.")
