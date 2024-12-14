from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random
from util import *
from selenium.common.exceptions import TimeoutException


def amazon_crawler_with_selenium(search_term:str, timeout=1, max_attempts=8):
    # driver = webdriver.Chrome()  # 确保你有相应的Chrome驱动程序

    try:
        for attempt in range(max_attempts):
            try:
                # driver = webdriver.Chrome()  # 确保你有相应的Chrome驱动程序
                options = webdriver.ChromeOptions()
                options.add_experimental_option("excludeSwitches", ["enable-automation"])
                options.add_experimental_option('useAutomationExtension', False)
                options.add_argument(
                    'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36')
                options.add_argument('--headless')
                options.add_argument("--log-level=3")  # 只显示错误信息
                driver = webdriver.Chrome(options=options)
                driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
                    "source": """Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
                })"""
                })
                # driver.set_window_size(1280, 720)
                # 生成随机的宽度和高度
                width = random.randint(188, 1920)
                height = random.randint(100, 1080)

                driver.set_window_size(width, height)
                # driver.get(f"https://www.amazon.com")
                # https://www.amazon.com/s?field-keywords=%E6%B4%97%E5%8F%91%E6%B6%B2&ref=cs_503_search
                if attempt == 0:
                    driver.get(f"https://www.amazon.com/s?k={search_term}")
                else:
                    driver.get(f"https://www.amazon.com/s?field-keywords={search_term}&ref=cs_503_search")
                # 等待页面加载
                # WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.s-result-item")))
                try:
                    # 等待页面加载
                    WebDriverWait(driver, timeout).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, "div.s-result-item")))
                    # 如果正常加载完成，执行原来的代码
                except TimeoutException:
                    # 如果没有正常加载出来，执行另外的代码
                    pass
                    # print("页面加载超时，执行备用逻辑")
                    # 这里可以添加备用逻辑的代码
                    # 例如：重新加载页面，或者执行其他操作
                # 如果页头中出现sorry，则重新加载页面
                print(driver.title)
                if "Sorry" in driver.title:
                    print("被拦住了，重新加载页面...")
                    driver.get("https://www.amazon.com/s?field-keywords={search_term}&ref=cs_503_search")
                    # 等待搜索框加载
                    search_box = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "e")))

                    # 输入搜索词
                    search_box.send_keys(search_term)
                    # 点击搜索按钮
                    search_button = driver.find_element(By.ID, "f")
                    search_button.click()
                    # 等待搜索结果页面加载
                    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".s-result-item")))
                    # time.sleep(1)

                # 滚动页面加载内容
                # driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(1)

                items = driver.find_elements(By.CSS_SELECTOR, "div.s-result-item")
                # 忽略第一个和最后三个元素
                items = items[1:-4] if len(items) > 3 else []

                products = []

                return driver.page_source
            except Exception as e:

                print(f"尝试 {attempt + 1} 次失败: {str(e)}")
                if attempt < max_attempts - 1:
                    time.sleep(random.uniform(1, 3))  # 随机等待时间重试
                    driver.quit()
                else:
                    print("多次尝试后仍然失败，可能需要检查网络连接或更换策略。")
                    return []
    finally:
        print("关闭浏览器...")
        driver.quit()


if __name__ == "__main__":
    data =  {'Home Theater System': ['Home Theater System, AV receiver, speakers, subwoofer, smart home cinema, budget 40000 RMB']}

    search_term = "AV receiver"
    html_source = amazon_crawler_with_selenium(search_term)
    all_result = []
    if isinstance(html_source,str):
        clean_html_source = clean_html_js_and_style(html_content = html_source)
        api_key = "sk-"
        client = OpenAI(api_key=api_key)
        result = process_large_html_content(html_content=clean_html_source, llm_client=client, search_text=search_term)
        for i in result: all_result.append(i.json())
