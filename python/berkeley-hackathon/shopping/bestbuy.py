import undetected_chromedriver as uc
import time
import random
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from typing import List, Dict
import json

def search_bestbuy(search_text: str, url: str = 'https://www.bestbuy.com/'):
    """
    使用 Selenium 模拟用户在 BestBuy 网站上搜索产品，并返回搜索结果页面的 HTML 源代码。
    """
    driver = uc.Chrome(headless=False, use_subprocess=False)
    driver.get(url)
    print("Waiting for user to click")
    time.sleep(random.choice([1, 6]))

    try:
        # 选择 America
        WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'body > div.page-container > div > div > div > div:nth-child(1) > div.country-selection > a.us-link > img'))
        ).click()

        # 等待搜索框加载
        search_box = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.ID, 'gh-search-input'))
        )
        search_box.send_keys(search_text)  # 输入搜索关键词

        # 点击搜索按钮
        search_button = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '.header-search-icon > svg:nth-child(1)'))
        )
        search_button.click()

        # 增加等待时间
        time.sleep(20)  # 增加等待时间，确保页面完全加载

        # 打印当前页面的 URL
        print("Current URL after search:", driver.current_url)

        # 获取页面源代码
        html_source = driver.page_source
        print("Page source retrieved successfully.")

    except Exception as e:
        # 捕获完整的错误信息
        print("Error occurred:", e)
        print("Error message:", e.msg if hasattr(e, 'msg') else "No detailed message available")
        print("Current URL:", driver.current_url)  # 打印当前页面的 URL
        print("Page source:", driver.page_source)  # 打印页面源代码
        html_source = None

    finally:
        driver.close()
        return html_source

def extract_product_info(html_content: str) -> List[Dict]:
    """
    从 HTML 内容中提取产品信息，并保存为 JSON 格式。
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    products = []

    # 查找所有产品项
    product_items = soup.select('#shop-sku-list-item-49989714')

    for item in product_items:
        product = {}

        # 提取 description
        description_tag = item.select_one(
            'div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > h4:nth-child(2) > a:nth-child(1)'
        )
        if description_tag:
            product['description'] = description_tag.text.strip()

        # 提取 model 和 value
        model_info = {}
        model_tags = item.select(
            'div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(3) > div:nth-child(1) > div:nth-child(1) > span'
        )
        if len(model_tags) >= 2:
            model_info[model_tags[0].text.strip()] = model_tags[1].text.strip()
        product['model'] = model_info

        # 提取 price
        price_tag = soup.select_one(
            '#pricing-price-64676021 > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > span:nth-child(1)'
        )
        if price_tag:
            product['price'] = price_tag.text.strip()

        products.append(product)

    return products

def split_html_content(html_content: str) -> List[Dict]:
    """
    处理 HTML 内容，提取产品信息并返回 JSON 格式的数据。
    """
    # 提取产品信息
    products = extract_product_info(html_content)

    # 返回 JSON 格式的数据
    return products

# 主函数
if __name__ == '__main__':
    search_text = 'laptop'  # 搜索关键词
    html_source = search_bestbuy(search_text=search_text)

    if html_source:
        # 处理 HTML 内容
        result = split_html_content(html_source)
        print(json.dumps(result, indent=4))
    else:
        print("Failed to retrieve HTML source.")
