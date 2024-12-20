import asyncio
import os
import time
from pydantic import BaseModel
from crawl4ai import AsyncWebCrawler
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import trafilatura
from typing import List
from openai import OpenAI
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError, Error as PlaywrightError


api_key = " "
client = OpenAI(api_key=api_key)
class InputsBoxSelector(BaseModel):
    intput_box_selector: str

def request_url(url:str,time_out:int=3):
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # 无头模式
    options.add_argument('--disable-gpu')  # 禁用GPU
    options.add_argument('--start-maximized')  # 最大化窗口
    service = Service()

    # 初始化Chrome浏览器
    driver = webdriver.Chrome(service=service, options=options)
    driver.get(url)
    wait = WebDriverWait(driver, time_out)
    wait.until(lambda d: d.execute_script('return document.readyState') == 'complete')

    # 获取当前页面的HTML内容
    html = driver.page_source

    # 关闭浏览器
    driver.quit()

    return html
def click_chrome_selector(url: str, selector: str, second_selector:str=None,search_text: str='',is_send_text:bool=True,time_out:int=10,wait_click_time_out:int=5) -> str:
    options = webdriver.ChromeOptions()
    options.add_argument(
        'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36')

    # options.add_argument('--headless')  # 无头模式
    options.add_argument('--disable-gpu')  # 禁用GPU
    options.add_argument('--start-maximized')  # 最大化窗口
    options.page_load_strategy = 'eager'
    # 创建一个Service实例
    service = Service()

    # 初始化Chrome浏览器
    driver = webdriver.Chrome(service=service, options=options)
    driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
        'source': 'Object.defineProperty(navigator, "webdriver", {get: () => undefined})'
    })
    driver.get(url)

    # 显式等待元素出现并进行操作
    wait = WebDriverWait(driver, time_out)
    search_box = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, selector)))
    search_box.click()
    time.sleep(wait_click_time_out)
    if is_send_text and second_selector is None:
        search_box.send_keys(search_text)
        search_box.send_keys(Keys.RETURN)
        print('点击过后发送文本')
    if second_selector is not None:
        search_input = wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, second_selector))
        )
        search_input.send_keys(search_text)
        search_input.send_keys(Keys.RETURN)
    wait_time = WebDriverWait(driver, wait_click_time_out)
    # 等待页面加载完成
    wait.until(lambda d: d.execute_script('return document.readyState') == 'complete')

    # 获取当前页面的HTML内容
    html = driver.page_source

    # 关闭浏览器
    driver.quit()

    return html

class FindSearchBoxSelector(BaseModel):
    selector: List[str] = None

class Media(BaseModel):
    images:List[str] = None
    videos:List[str] = None


class HtmlSearchTextChunk(BaseModel):
    url:str = None
    description:str = None
    media:List[Media] = None

class HtmlSearchText(BaseModel):
    chunks:List[HtmlSearchTextChunk] = None

def extract_search_related_elements(html_content: str) -> List[BeautifulSoup]:
    """
    提取 HTML 内容中可能与搜索功能相关的所有元素。

    参数：
        html_content (str): 要解析的 HTML 文本内容。

    返回：
        List[BeautifulSoup]: 一个包含所有可能与搜索相关的元素的列表。
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    search_elements = []

    # 定义要检查的标签
    tags_to_search = ['input', 'button', 'svg', 'div', 'span', 'form', 'textarea']

    # 搜索所有指定标签的元素
    for tag in tags_to_search:
        elements = soup.find_all(tag)
        for elem in elements:
            if is_search_related(elem):
                search_elements.append(elem)

    return search_elements

def is_search_related(element: BeautifulSoup) -> bool:
    """
    判断给定的元素是否可能与搜索功能相关。

    参数：
        element (BeautifulSoup): 要判断的元素。

    返回：
        bool: 如果元素可能与搜索功能相关，返回 True；否则返回 False。
    """
    SEARCH_KEYWORDS = ['search', '搜索', 'query', '查找', '查询', 'icon-search', 'icon_search','検索','Search']

    # 检查元素的属性
    for attr in ['name', 'id', 'class', 'placeholder', 'aria-label', 'title']:
        attr_value = element.get(attr)
        if attr_value:
            if isinstance(attr_value, list):
                attr_values = ' '.join(attr_value).lower()
            else:
                attr_values = str(attr_value).lower()
            for keyword in SEARCH_KEYWORDS:
                if keyword in attr_values:
                    return True

    # 特殊处理 <input> 标签的 type 属性
    if element.name == 'input':
        input_type = element.get('type', '').lower()
        if input_type in ['search', 'text']:
            return True

    return False

def get_css_selector(element: BeautifulSoup) -> str:
    """
    获取元素的 CSS 选择器路径。

    参数：
        element (BeautifulSoup): 目标元素。

    返回：
        str: 元素的 CSS 选择器路径。
    """
    path = []
    while element and element.name != '[document]':
        selector = element.name
        if element.get('id'):
            selector += f"#{element.get('id')}"
        elif element.get('class'):
            classes = '.'.join(element.get('class'))
            selector += f".{classes}"
        else:
            siblings = element.find_previous_siblings(element.name)
            index = len(siblings) + 1
            selector += f":nth-of-type({index})"
        path.insert(0, selector)
        element = element.parent
    return ' > '.join(path)

def get_css_selector_with_google(tag):
    """
    获取 BeautifulSoup 标签的唯一 CSS 选择器
    """
    selector = []
    while tag is not None and tag.name != '[document]':
        sibling = tag.previous_sibling
        nth = 1
        while sibling:
            if sibling.name == tag.name:
                nth += 1
            sibling = sibling.previous_sibling
        if tag.get('id'):
            selector_part = f"{tag.name}#{tag['id']}"
            selector.insert(0, selector_part)
            break  # ID 是唯一的，后续的选择器可以省略
        else:
            if tag.get('class'):
                classes = ".".join(tag.get('class'))
                selector_part = f"{tag.name}.{classes}"
            else:
                selector_part = tag.name
            # 添加 :nth-of-type(n) 以确保选择器的唯一性
            selector_part += f":nth-of-type({nth})"
            selector.insert(0, selector_part)
        tag = tag.parent
    return " > ".join(selector)
def find_search_elements_in_html(html_content: str,is_google_url:bool=False) -> List[str]:
    """
    入口函数，查找 HTML 内容中可能与搜索功能相关的元素，并返回其 CSS 选择器路径列表。

    参数：
        html_content (str): 要解析的 HTML 文本内容。

    返回：
        List[str]: 可能与搜索功能相关的元素的 CSS 选择器路径列表。
    """
    search_elements = extract_search_related_elements(html_content)
    if is_google_url:
        selectors = [get_css_selector_with_google(elem) for elem in search_elements]
    else:
        selectors = [get_css_selector(elem) for elem in search_elements]
    # selectors = [i for i in selectors if i in ]
    selectors_data = []
    # if is_google_url == False:
    #     for i in selectors:
    #         for key_word in ['search', '搜索', 'query', '查找', '查询', 'icon-search', 'icon_search','検索','Search']:
    #             if key_word in i :
    #                 selectors_data.append(i)
    return selectors

def load_prompt(prompt_type: str,html_code:str,keyword:str=None):
    prompt = ''
    if prompt_type == "search_box":
        prompt = f"""
        Please parse the following HTML web page code:
        HTML web page code:
        {html_code}

        1. C - Context
        "You will search for search box elements in the provided HTML web page code. The page may contain multiple `input` elements used for different functions, including search, form filling, etc."

        2. O - Objective
        "The objective is to find all `input` elements in the HTML web page code where the `id` or `class` attribute contains the keyword `'search'`, to help identify the search boxes on the page."

        3. S - Style
        "The output should be technical and concise to facilitate subsequent programming and data processing."

        4. T - Tone
        "The tone should be professional and direct, providing clear and task-related results."

        5. A - Audience
        "The target audience is developers or data engineers who want to automatically locate and use the search box on the page."

        6. R - Response
        "The output should be a JSON object containing a list of strings (`list[str]`), where each string is the CSS selector path of the matching `input` element. If no matching elements are found, return an empty JSON object."
        """

    if prompt_type == "search_text":
        prompt = f'''
        Backstory:
        "You are developing an automated system to extract information related to a specific keyword from web pages. The keyword for this task is '{keyword}'. The goal is to filter out all links, content summaries, and key media content related or similar to '{keyword}' from the provided HTML web page code. Since the web content may not directly contain the exact keyword, you need to look for content associated with or similar in meaning to the keyword."

        Objective:
        "Based on the provided HTML web page code, extract all information related or similar to the keyword '{keyword}' and output it in a structured JSON format. This information includes related or similar links (URLs), content summaries for each link, and related media content such as image and video links."

        Specifics:
        "- Extract content directly related to or similar in meaning to the keyword '{keyword}'.
        - Allow matching of keyword variants, synonyms, or related topics.
        - Related links should include the full URL.
        - Content summaries should be concise and accurately describe the link content.
        - Related media content includes image URLs and video links.
        - The output JSON structure should be clear and without redundant information, facilitating subsequent programming and data processing. The corresponding content should have clear descriptions and explanations."

        Tasks:
        "1. Parse the provided HTML web page code.
        2. Find all elements directly related or similar to the keyword '{keyword}', including links, headings, paragraphs, etc.
        3. Extract the URLs, content summaries, and related media content of these elements.
        4. Ensure the extracted information is accurate and comprehensive, including content related or similar to the keyword.
        5. Organize the extracted information into a structured JSON format."

        Actions:
        "1. Parse the HTML web page code.
        2. Use the keyword '{keyword}' along with its synonyms and related terms to search for matching content.
        3. Find elements containing related keywords such as links (<a> tags), headings (e.g., <h1> to <h6> tags), paragraphs (<p> tags), etc.
        4. For each found element, extract its content, related links, and media resources (e.g., src attributes of <img> and <video> tags).
        5. Organize all extracted information into a JSON object as required."

        Results:
        "Generate a JSON object containing all information related or similar to '{keyword}'. This object should include a field 'results', which is a list where each item contains the following subfields:
        - 'url': The full URL of the related link. If it does not exist, it should be an empty string.
        - 'description': A summary or abstract related to the content. If it does not exist, it should be an empty string.
        - 'media': A sub-object containing related media content, including:
            - 'images': A list of image URLs. If there are no images, it should be an empty list.
            - 'videos': A list of video links. If there are no videos, it should be an empty list.

        Ensure that the output JSON object is clean, without unnecessary HTML tags or script code, and contains only plain text information and valid media links."

        HTML web page code:
        {html_code}
        '''
    return prompt

def clean_html(html_content: str) -> str:
    soup = BeautifulSoup(html_content, 'html.parser')
    for tag in soup(['script', 'style']):
        tag.decompose()
    clean_html = str(soup)
    return clean_html

def split_html(text: str, max_length: int = 15000) -> List[str]:
    """
    将文本分割成不超过max_length字符的块，尽量在HTML标签边界处分割。

    参数：
        text (str): 要分割的文本。
        max_length (int): 每块的最大字符数。

    返回：
        List[str]: 分割后的文本块列表。
    """
    chunks = []
    start = 0
    text_length = len(text)

    while start < text_length:
        end = start + max_length
        if end >= text_length:
            chunks.append(text[start:])
            break
        # 尽量在最近的闭合标签处分割
        close_tag_pos = text.rfind('</', start, end)
        if close_tag_pos == -1 or close_tag_pos < start:
            # 如果找不到合适的分割点，则强制分割
            chunks.append(text[start:end])
            start = end
        else:
            # 在最近的闭合标签处分割
            close_tag_end = text.find('>', close_tag_pos, end)
            if close_tag_end == -1:
                # 如果找不到闭合标签的结束符，则强制分割
                chunks.append(text[start:end])
                start = end
            else:
                chunks.append(text[start:close_tag_end + 1])
                start = close_tag_end + 1

    return chunks

# def use_llm(prompt: str) -> str:
#     """使用 LLm 进行Html文本解读"""
#
#     response = client.chat.completions.create(
#         model="gpt-4o-mini",
#         messages=[
#             {
#                 "role": "user",
#                 "content": [
#                     {"type": "text", "text": prompt},
#                 ]
#             }
#         ],
#     )
#     return response.choices[0].message.content


def click_playwright_selector(
        url: str,
        selector: str,
        second_selector: str = None,
        search_text: str = '',
        is_send_text: bool = True,
        time_out: int = 20000,  # 毫秒，增加超时时间
        wait_click_time_out: int = 5000  # 毫秒
) -> str:
    """
    使用 Playwright 打开指定 URL，点击元素，发送文本（可选），并返回页面 HTML 内容。
    """
    html = ""
    # 启用 Playwright 的详细日志（可选）

    with sync_playwright() as p:
        # 启动 Chromium 浏览器（无头模式）
        browser = p.chromium.launch(headless=False)  # 调试时设置为 False
        context = browser.new_context(
            viewport={"width": 1920, "height": 1080},
            ignore_https_errors=True,
            bypass_csp=True
        )
        page = context.new_page()

        try:
            page.goto(url, wait_until='domcontentloaded', timeout=time_out)
            # page.screenshot(path='before_click.png')  # 截图用于调试
            time.sleep(wait_click_time_out//1000)
            # 等待并点击第一个选择器
            page.wait_for_selector(selector, state='visible', timeout=time_out)
            page.click(selector)

            if is_send_text:
                if second_selector is None:
                    # 检查 selector 是否指向可编辑元素

                    page.fill(selector, search_text)
                    page.press(selector, 'Enter')
                else:
                    # 等待第二个选择器出现
                    page.wait_for_selector(second_selector, state='visible', timeout=time_out)
                    # 检查 second_selector 是否指向可编辑元素

                    page.fill(second_selector, search_text)
                    page.press(second_selector, 'Enter')

                # 使用 Playwright 的等待方法代替 time.sleep
                page.wait_for_timeout(wait_click_time_out)

            # 等待页面加载完成，使用 'load' 状态
            page.wait_for_load_state('load', timeout=time_out)
            # 获取页面的 HTML 内容
            html = page.content()

        except PlaywrightTimeoutError as e:
            print(f"等待元素超时: {e}")
            page.screenshot(path='timeout_error.png')  # 截图失败时的页面状态
        except PlaywrightError as e:
            print(f"Playwright 错误: {e}")
            page.screenshot(path='playwright_error.png')  # 截图其他错误时的页面状态
        except Exception as e:
            print(f"其他错误: {e}")
            page.screenshot(path='general_error.png')  # 截图其他错误时的页面状态
        finally:
            browser.close()

    return html

def use_llm_return_json(prompt: str,format_class,supplement_prompt:str=None,model_name:str='gpt-4o') -> str:
    """使用 LLm 进行Html文本解读"""
    messages = [
        {"role": "system",
         "content": "You are a professional html parser"},
        {"role": "user", "content": prompt},

    ]
    if supplement_prompt is not None:
        messages.append({"role": "user", "content": supplement_prompt})
    completion = client.beta.chat.completions.parse(
        model=model_name,
        messages=messages,
        response_format=format_class,)


    return completion.choices[0].message.parsed


async def load_url(url:str):
    async with AsyncWebCrawler(verbose=True) as crawler:
        wait_for = """() => {
                    return new Promise(resolve => setTimeout(resolve, 3000));
                }"""
        result = await crawler.arun(url=url, magic=True, simulate_user=True, override_navigator=True,wait_fo=wait_for)
        if result.status_code == 200:
            # 如果您需要进一步处理HTML内容，可以在这里进行
            # 例如，使用LLM或其他解析方法
            return result.html
        else:
            raise Exception(f"Error loading URL: {url}")



def find_search_box(html_content:str,is_google_url:bool=False):
    search_box_html_result = []
    if len(html_content) <= llm_max_token:
        search_box_prompt = load_prompt(prompt_type='search_box', html_code=html_content)
        search_box_html = use_llm_return_json(prompt=search_box_prompt, format_class=FindSearchBoxSelector)
        search_box_html_result = search_box_html.selector
    else:
        selectors = find_search_elements_in_html(html_content,is_google_url=is_google_url)
        if selectors:
            search_box_html_result = list(set(selectors))
    return search_box_html_result

if __name__ == "__main__":
    # url = 'https://pypi.org/'
    # url = 'https://google.com/'
    # url = 'https://github.com/search'
    url = 'https://www.bing.com/'
    # search_text = 'mofa github'
    # search_text = '考试'
    is_google_url = False
    if url in ['https://google.com/', 'https://google.com']: is_google_url = True


    search_text = 'opea'

    llm_max_token = 124000
    data = []
    html_content = asyncio.run(load_url(url=url))
    search_box_html_result = find_search_box(html_content,is_google_url=is_google_url)
    new_search_box = []

    if len(search_box_html_result)>0:
        use_search_box = []
        for search_box_selector in search_box_html_result:
            if 'svg' in search_box_selector.split('>')[-1]:
                html_doc = click_chrome_selector(url=url, selector=search_box_selector, search_text=search_text,
                                                 is_send_text=False)
                svg_search_box = find_search_box(html_doc)
                new_search_box = [search_box_selector + '|' + i for i in list(set(svg_search_box + new_search_box)) if i not in list(set(use_search_box+search_box_html_result)) ]
                continue
            use_search_box.append(search_box_selector)
            try:
                # html_doc = click_chrome_selector(url=url, selector=search_box_selector,search_text=search_text)
                html_doc = click_playwright_selector(url=url, selector=search_box_selector,search_text=search_text)
                html_doc = clean_html(html_content=html_doc)
                if html_doc == '' or html_doc == ' ': continue
                html_prompt = load_prompt(prompt_type='search_text', html_code=html_doc, keyword=search_text)
                llm_html_result = use_llm_return_json(prompt=html_prompt, format_class=HtmlSearchText,supplement_prompt=trafilatura.extract(html_doc))
                data+=llm_html_result.chunks
            except Exception as e :
                print(search_box_selector,'---------------  \n')
                continue
    if len(new_search_box)>0:
        for search_box_selector in new_search_box:
            try:
                html_doc = click_chrome_selector(url=url, selector=search_box_selector.split('|')[0],second_selector=search_box_selector.split('|')[1], search_text=search_text)
                html_doc = clean_html(html_content=html_doc)
                html_prompt = load_prompt(prompt_type='search_text', html_code=html_doc, keyword=search_text)
                llm_html_result = use_llm_return_json(prompt=html_prompt, format_class=HtmlSearchText,
                                                      supplement_prompt=trafilatura.extract(html_doc))
                data += llm_html_result.chunks
            except Exception as e :
                print(search_box_selector,'---------------  \n')
                continue
    # html_prompt = load_prompt(prompt_type='search_text', html_code=html_content, keyword=search_text)
    # homepage_introduction = use_llm_return_json(prompt=html_prompt, format_class=HtmlSearchText,
    #                                       supplement_prompt=trafilatura.extract(html_content))
    # data += homepage_introduction.chunks
    print(data)



