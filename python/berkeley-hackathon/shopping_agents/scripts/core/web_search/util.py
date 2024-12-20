import json

import tiktoken
from typing import List, Optional, Dict
from pydantic import BaseModel, Field
from bs4 import BeautifulSoup, NavigableString, Tag
from typing import List
from bs4 import BeautifulSoup

from pydantic import BaseModel

class Media(BaseModel):
    images: Optional[List[str]] = Field(
        None,
        description="List of image URLs related to the product."
    )
    videos: Optional[List[str]] = Field(
        None,
        description="List of video URLs related to the product."
    )

class ReviewBreakdown(BaseModel):
    positive: Optional[int] = Field(
        None,
        description="Number of positive reviews."
    )
    neutral: Optional[int] = Field(
        None,
        description="Number of neutral reviews."
    )
    negative: Optional[int] = Field(
        None,
        description="Number of negative reviews."
    )

class HtmlSearchTextChunk(BaseModel):
    url: Optional[str] = Field(
        None,
        description="The product or item's URL."
    )
    product_id: Optional[str] = Field(
        None,
        description="A unique identifier for the product."
    )
    sku: Optional[str] = Field(
        None,
        description="The Stock Keeping Unit (SKU) for the product."
    )
    model: Optional[str] = Field(
        None,
        description="The model name or number of the product."
    )
    title: Optional[str] = Field(
        None,
        description="The product's title or name."
    )
    description: Optional[str] = Field(
        None,
        description="A detailed description of the product."
    )
    short_description: Optional[str] = Field(
        None,
        description="A brief summary or short description of the product."
    )
    brand: Optional[str] = Field(
        None,
        description="The brand name of the product."
    )
    category: Optional[str] = Field(
        None,
        description="The category under which the product is listed."
    )
    category_hierarchy: Optional[List[str]] = Field(
        None,
        description="A hierarchical list representing the category path, e.g., ['Electronics','Phones','Smartphones']."
    )
    price: Optional[float] = Field(
        None,
        description="The current price of the product."
    )
    currency: Optional[str] = Field(
        None,
        description="The currency code for the product's price, e.g., 'USD', 'CNY'."
    )
    original_price: Optional[float] = Field(
        None,
        description="The original or list price before any discounts."
    )
    discount_info: Optional[str] = Field(
        None,
        description="Information about any discounts or promotions available."
    )
    availability: Optional[str] = Field(
        None,
        description="The stock or availability status of the product."
    )
    rating: Optional[float] = Field(
        None,
        description="The average rating of the product, typically on a scale like 1-5."
    )
    reviews_count: Optional[int] = Field(
        None,
        description="The total number of reviews received by the product."
    )
    reviews_breakdown: Optional[ReviewBreakdown] = Field(
        None,
        description="A breakdown of reviews into positive, neutral, and negative counts."
    )
    seller_info: Optional[str] = Field(
        None,
        description="Information about the seller or vendor offering the product."
    )
    attributes: Optional[Dict[str, str]] = Field(
        None,
        description="Additional attributes of the product, e.g. {'Color':'Black','Storage':'128GB'}."
    )
    specifications: Optional[Dict[str, str]] = Field(
        None,
        description="Technical or detailed specifications of the product, e.g. {'Screen Size':'6.5 inches','Battery':'4000mAh'}."
    )
    media: Optional[Media] = Field(
        None,
        description="Media-related information, including images and videos."
    )
    shipping_info: Optional[str] = Field(
        None,
        description="Information related to shipping, e.g., 'Free shipping' or delivery time estimates."
    )
    warranty_info: Optional[str] = Field(
        None,
        description="Warranty details provided with the product."
    )
    tags: Optional[List[str]] = Field(
        None,
        description="List of tags or keywords associated with the product."
    )

class HtmlSearchText(BaseModel):
    chunks: Optional[List[HtmlSearchTextChunk]] = Field(
        None,
        description="A list of structured product search result items."
    )

def split_html_content(html_content, max_tokens_per_chunk, model='gpt-4'):
    """
    将 HTML 内容拆分为多个块，确保不破坏 HTML 标签结构，每个块的 token 数不超过最大限制。
    """
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
            # 获取开始标签和结束标签
            start_tag = f'<{node.name}'
            for attr, value in node.attrs.items():
                if isinstance(value, list):
                    value = ' '.join(value)
                start_tag += f' {attr}="{value}"'
            start_tag += '>'
            end_tag = f'</{node.name}>'

            start_tag_tokens = len(encoding.encode(start_tag))
            end_tag_tokens = len(encoding.encode(end_tag))

            # 保存当前块的状态
            prev_chunk = current_chunk
            prev_tokens = current_tokens

            # 尝试添加开始标签
            if current_tokens + start_tag_tokens > max_tokens_per_chunk:
                if current_chunk.strip():
                    chunks.append(current_chunk)
                current_chunk = ''
                current_tokens = 0

            current_chunk += start_tag
            current_tokens += start_tag_tokens

            # 递归处理子节点
            for child in node.contents:
                process_node(child)

            # 尝试添加结束标签
            if current_tokens + end_tag_tokens > max_tokens_per_chunk:
                if current_chunk.strip():
                    current_chunk += end_tag
                    chunks.append(current_chunk)
                else:
                    # 如果开始标签和结束标签本身就超过限制，强制添加
                    current_chunk = start_tag + end_tag
                    chunks.append(current_chunk)
                current_chunk = ''
                current_tokens = 0
            else:
                current_chunk += end_tag
                current_tokens += end_tag_tokens

    # 从 body 开始遍历，如果没有 body，则遍历整个文档
    root = soup.body if soup.body else soup
    for element in root.contents:
        process_node(element)

    if current_chunk.strip():
        chunks.append(current_chunk)

    return chunks

def estimate_tokens(content, model='gpt-4'):
    """
    Estimate the number of tokens in the content using the specified model's tokenizer.
    """
    # Initialize the encoding for the given model
    encoding = tiktoken.encoding_for_model(model)
    # Encode the content and count the tokens
    return len(encoding.encode(content))


def process_large_html_content(llm_client,html_content:str,search_text:str='',max_total_tokens=128000, model='gpt-4'):
    """
    处理大型 HTML 内容，确保每个块的 token 数不超过最大限制。
    """
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
        response = use_llm_return_json(llm_client=llm_client, prompt=prompt, format_class=HtmlSearchText)
        print("处理内容未超出 token 限制。")
        # 在这里添加您的处理逻辑
        return response
    else:
        print("内容超出 token 限制，正在拆分为多个块。")
        # 预留一些 tokens 以防止意外超出限制
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
            response = use_llm_return_json(llm_client=llm_client, prompt=prompt, format_class=HtmlSearchText)
            result.append(response)

        return result

def use_llm_return_json(llm_client, prompt: str, format_class, supplement_prompt: str = None,
                        model_name: str = 'gpt-4o-mini', image_data: str = None) -> str:
    """使用 LLM 进行Html文本解读"""
    prompt_data = [
        {
            "type": "text",
            "text": prompt
        },
    ]

    if image_data is not None:
        # 确保图像消息也包含content字段，即使它是一个空字符串
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
def clean_html_js_and_style(html_content: str) -> str:
    soup = BeautifulSoup(html_content, 'html.parser')
    for tag in soup(['script', 'style']):
        tag.decompose()
    clean_html = str(soup)
    return clean_html

def shopping_html_structure(llm_client,html_content:str,search_text:str)->str:
    all_result = []
    if isinstance(html_content,str):
        clean_html_source = clean_html_js_and_style(html_content = html_content)
        result = process_large_html_content(html_content=clean_html_source, llm_client=llm_client, search_text=search_text)
        if isinstance(result,list):
            if len(result)>0:
                for i in result: all_result.append(i.json())
            else:
                all_result.append('')
        else:
            all_result.append(result.json())

    return ' ||| '.join(all_result)


def read_website(file_path:str='webpage.json')->str:
    with open(file_path,'r') as f:
        data = json.load(f)
    return data
