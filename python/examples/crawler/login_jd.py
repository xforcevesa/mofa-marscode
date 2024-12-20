import base64
import random
import time
from typing import List

from bs4 import BeautifulSoup
from openai import OpenAI
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError, Error as PlaywrightError
from pydantic import BaseModel
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import time
import json
import random
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


# def login_jd(llm_client,
#              url: str,
#              selector_data: dict,
#              search_text: str = '',
#              is_send_text: bool = True,
#              time_out: int = 20000,  # 毫秒，增加超时时间
#              wait_click_time_out: int = 5000  # 毫秒
#              ) -> str:
#     """
#     使用 Playwright 打开指定 URL，点击元素，发送文本（可选），并返回页面 HTML 内容。
#     """
#     html = ""
#     # 启用 Playwright 的详细日志（可选）
#
#     with sync_playwright() as p:
#         # 启动 Chromium 浏览器（无头模式）]
#         browser = p.chromium.launch(headless=False,
#                                     args=[
#                                         "--disable-blink-features=AutomationControlled",
#                                         "--disable-infobars",
#                                         "--no-sandbox",
#                                         "--disable-setuid-sandbox",
#                                         "--disable-dev-shm-usage"
#                                     ],
#                                     executable_path='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
#                                     )  # 调试时设置为 False
#         context = browser.new_context(
#             ignore_https_errors=True,
#             bypass_csp=True,
#             viewport={"width": 1280, "height": 720},
#             user_agent = random.choice(userAgentStrings),
#             extra_http_headers={
#                 "Accept-Language": "en-US,en;q=0.9",
#                 "Upgrade-Insecure-Requests": "1",
#                 "DNT": "1"
#             }
#
#         )
#         page = context.new_page()
#         page.add_init_script("""
#             // Remove the `navigator.webdriver` property
#             Object.defineProperty(navigator, 'webdriver', { get: () => undefined });
#
#             // Mock plugins and languages
#             Object.defineProperty(navigator, 'plugins', {
#                 get: () => [1, 2, 3],
#             });
#
#             Object.defineProperty(navigator, 'languages', {
#                 get: () => ['en-US', 'en'],
#             });
#
#             // Override the user agent to remove headless browser indicators
#             Object.defineProperty(navigator, 'userAgent', {
#                 get: () => navigator.userAgent.replace('Headless', ''),
#             });
#
#             // Mock platform
#             Object.defineProperty(navigator, 'platform', {
#                 get: () => 'MacIntel',
#             });
#         """)
#
#         try:
#             page.goto(url, wait_until='domcontentloaded', timeout=time_out)
#             time.sleep(10)
#
#             # 等待并点击第一个选择器
#             user_element_selector,pwd_element_selector = selector_data['user_element_selector'],selector_data['pwd_element_selector']
#
#             page.fill(user_element_selector, selector_data['user_element_data'])
#             page.fill(pwd_element_selector, selector_data['pwd_element_data'])
#             page.click(selector_data['login_button'])
#
#             page.wait_for_load_state('load', timeout=time_out)
#             # 获取页面的 HTML 内容
#             html = page.content()
#             cookies = context.cookies()
#             with open('cookies.json', 'w') as f:
#                 import json
#                 json.dump(cookies, f)
#             context.close()
#
#
#
#         except PlaywrightTimeoutError as e:
#             print(f"等待元素超时: {e}")
#             page.screenshot(path='timeout_error.png')  # 截图失败时的页面状态
#         except PlaywrightError as e:
#             print(f"Playwright 错误: {e}")
#             page.screenshot(path='playwright_error.png')  # 截图其他错误时的页面状态
#         except Exception as e:
#             print(f"其他错误: {e}")
#             page.screenshot(path='general_error.png')  # 截图其他错误时的页面状态
#         finally:
#             browser.close()
#     return html
def login_jd_selenium(url: str,
                      selector_data: dict,
                      search_text: str = '',
                      is_send_text: bool = True,
                      time_out: int = 20,  # 秒，增加超时时间
                      wait_click_time_out: int = 5  # 秒
                      ) -> str:
    """
    使用 Selenium 打开指定 URL，点击元素，发送文本（可选），并返回页面 HTML 内容。
    """
    html = ""
    cookies = []
    # 隐藏自动化特征的 Chrome 配置
    user_agent = random.choice([
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36",
    ])

    options = Options()
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--user-data-dir=/Users/chenzi/Library/Application Support/Google/Chrome/Default")  # 替换为你的用户数据目录
    # options.add_argument("--start-maximized")  # 启动时窗口最大化

    options.add_argument("--disable-infobars")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-setuid-sandbox")
    options.add_argument("--disable-gpu")
    options.add_argument(f"user-agent={user_agent}")



    # 配置服务路径
    service = Service()  # 替换为你的 ChromeDriver 路径
    driver = webdriver.Chrome(service=service, options=options)

    # 覆盖 `navigator.webdriver` 属性
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": """
            Object.defineProperty(navigator, 'webdriver', { get: () => undefined });
        """
    })

    try:
        # 打开指定的 URL
        driver.get(url)

        # 等待页面加载
        time.sleep(10)

        # 填写用户名和密码
        user_element_selector, pwd_element_selector = selector_data['user_element_selector'], selector_data['pwd_element_selector']

        user_input = driver.find_element(By.CSS_SELECTOR, user_element_selector)
        user_input.send_keys(selector_data['user_element_data'])

        pwd_input = driver.find_element(By.CSS_SELECTOR, pwd_element_selector)
        pwd_input.send_keys(selector_data['pwd_element_data'])

        # 点击登录按钮
        login_button = driver.find_element(By.CSS_SELECTOR, selector_data['login_button'])
        login_button.click()

        # 等待页面加载完成
        time.sleep(wait_click_time_out)

        # 获取页面 HTML 内容
        html = driver.page_source

        # 获取 cookies
        cookies = driver.get_cookies()
        with open("cookies.json", "w") as f:
            json.dump(cookies, f)

    except Exception as e:
        print(f"发生错误: {e}")
        driver.save_screenshot("selenium_error.png")  # 截取错误时的页面状态
    finally:
        driver.quit()

    return html
# url = 'https://stackoverflow.com/'
url = 'https://passport.jd.com/new/login.aspx'
selector = '#search > div > input'
search_text='apple 表带'
api_key = " "
client = OpenAI(api_key=api_key)
selector_data = {'user_element_selector':'#loginname','pwd_element_selector':'#nloginpwd',
                 'login_button':'#loginsubmit',
                 'user_element_data':'18583383212','pwd_element_data':'Tt66668888.'}
login_jd_selenium( url=url, selector_data=selector_data, search_text=search_text)