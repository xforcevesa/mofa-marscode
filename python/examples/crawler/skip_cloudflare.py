import base64
import random
import time
from typing import List

from bs4 import BeautifulSoup
from openai import OpenAI
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError, Error as PlaywrightError
from pydantic import BaseModel

import cv2
import numpy as np
class CloudflareAnalysis(BaseModel):
    x: str
    y: str
    is_cloudflare: bool

def clean_html_js_and_style(html_content: str) -> str:
    soup = BeautifulSoup(html_content, 'html.parser')
    for tag in soup(['script', 'style']):
        tag.decompose()
    clean_html = str(soup)
    return clean_html

userAgentStrings = [
  'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.2227.0 Safari/537.36',
  'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
  'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.3497.92 Safari/537.36',
  'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
]


def find_button_contour(image_path: str):
    # 加载图像
    image = cv2.imread(image_path)

    # 转换为灰度图像
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # 应用二值化
    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)

    # 寻找轮廓
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # 假设按钮是最大的轮廓
    button_contour = max(contours, key=cv2.contourArea)

    # 获取边界框
    x, y, w, h = cv2.boundingRect(button_contour)
    center_x = x + w // 2
    center_y = y + h // 2
    return center_x, center_y
# def use_llm_return_json(llm_client, prompt: str, format_class, supplement_prompt:str=None, model_name:str='gpt-4o-mini', image_data:str=None) -> str:
#     """使用 LLm 进行Html文本解读"""
#     messages = [
#         {"role": "system",
#          "content": "You are a professional html parser"},
#         {"role": "user", "content": prompt},
#     ]
#     if supplement_prompt is not None:
#         messages.append({"role": "user", "content": supplement_prompt})
#     if image_data is not None:
#         image = {
#             "type": "image_url",
#             "image_url": {
#                 "url": f"data:image/jpeg;base64,{image_data}"
#             }
#         }
#         messages.append(image)
#     completion = llm_client.beta.chat.completions.parse(
#         model=model_name,
#         messages=messages,
#         response_format=format_class,)
#     return completion.choices[0].message.parsed

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

def encode_image(image_path:str):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')
def skip_cloudflare(llm_client,playwright_page,prompt:str=None,image_data:str=None):
    if prompt is None:
        prompt = f""" Context: You are provided with a screenshot of a webpage. The task is to analyze this image to determine if the webpage is a Cloudflare verification page. If it is, you need to identify the region or element representing the human verification button or window that requires user interaction.
        Output:
        
        Confirm whether the provided image represents a Cloudflare verification page (e.g., "Yes" or "No").
        If confirmed as a Cloudflare verification page, provide the pixel coordinates (x, y) or a description of the region that indicates the interactive verification button or window.
        Structure:
        
        Start with a statement confirming if the webpage is a Cloudflare verification page.
        If "Yes," identify and specify the pixel coordinates or detailed description of the interactive element to be clicked.
        Tone: The response should be technical, precise, and easy to follow.
        
        Audience: This prompt is designed for automation engineers and web developers who need to identify and interact with specific elements on Cloudflare verification pages.
        
        Requirements:
        
        Analyze the provided screenshot for typical Cloudflare verification indicators, such as phrases like "Checking your browser" or visual elements like a verification window.
        Identify the area or element that users would interact with (e.g., a "I'm not a robot" button or checkbox).
        Ensure the output specifies the location (coordinates) of the relevant interactive element for Playwright to use in automated clicking.
        Time: Generate the response within a reasonable timeframe to facilitate real-time automation tasks.
        
        Prompt: Given the following screenshot of a webpage:
        
        Confirm whether this page is a Cloudflare verification page.
        If it is, identify and return the pixel coordinates or a description of the interactive element (e.g., button or verification window) that requires user interaction.
        Insert screenshot here
        
        Example Analysis:
        
        Confirmation: "Yes"
        Verification element identified at coordinates: x=300, y=450
        """

    cloudflare_analysis = use_llm_return_json(llm_client,prompt=prompt,format_class=CloudflareAnalysis,image_data=image_data)
    if cloudflare_analysis.is_cloudflare:
        playwright_page.mouse.click(int(cloudflare_analysis.x), int(cloudflare_analysis.y))

        return playwright_page
    else:
        return False

def click_playwright_selector(llm_client,
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
        browser = p.chromium.launch(headless=False,
                                    args=[
                                        "--disable-blink-features=AutomationControlled",
                                        "--disable-infobars",
                                        "--no-sandbox",
                                        "--disable-setuid-sandbox",
                                        "--disable-dev-shm-usage"
                                    ],
                                    # executable_path='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
                                    )  # 调试时设置为 False
        context = browser.new_context(
            ignore_https_errors=True,
            bypass_csp=True,
            viewport={"width": 1280, "height": 720},
            user_agent = random.choice(userAgentStrings),
            extra_http_headers={
                "Accept-Language": "en-US,en;q=0.9",
                "Upgrade-Insecure-Requests": "1",
                "DNT": "1"
            }

        )
        page = context.new_page()
        page.add_init_script("""
            // Remove the `navigator.webdriver` property
            Object.defineProperty(navigator, 'webdriver', { get: () => undefined });

            // Mock plugins and languages
            Object.defineProperty(navigator, 'plugins', {
                get: () => [1, 2, 3],
            });

            Object.defineProperty(navigator, 'languages', {
                get: () => ['en-US', 'en'],
            });

            // Override the user agent to remove headless browser indicators
            Object.defineProperty(navigator, 'userAgent', {
                get: () => navigator.userAgent.replace('Headless', ''),
            });

            // Mock platform
            Object.defineProperty(navigator, 'platform', {
                get: () => 'MacIntel',
            });
        """)

        try:
            page.goto(url, wait_until='domcontentloaded', timeout=time_out)
            time.sleep(10)
            cloudflare_image_path = 'cloudflare.png'
            page.screenshot(path=cloudflare_image_path)
            x,y = find_button_contour(image_path=cloudflare_image_path)
            page.mouse.click(x, y)

            # cloudflare_page = skip_cloudflare(playwright_page=page,html_content=page.content(),llm_client=llm_client,prompt=None)
            # if cloudflare_page: page = cloudflare_page

            # page.screenshot(path='before_click.png')  # 截图用于调试
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
url = 'https://stackoverflow.com/'
selector = '#search > div > input'
search_text='dora-rs'
api_key = " "
client = OpenAI(api_key=api_key)

click_playwright_selector(llm_client=client,url=url,selector=selector,search_text=search_text)