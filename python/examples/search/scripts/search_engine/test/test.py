from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random

def amazon_crawler_with_selenium(search_term, timeout=1, max_attempts=3):
    #driver = webdriver.Chrome()  # 确保你有相应的Chrome驱动程序
    
    try:
        for attempt in range(max_attempts):
            try:
                driver = webdriver.Chrome()  # 确保你有相应的Chrome驱动程序
                #driver.get(f"https://www.amazon.com/s?k={search_term}")
                #https://www.amazon.com/s?field-keywords=%E6%B4%97%E5%8F%91%E6%B6%B2&ref=cs_503_search
                driver.get(f"https://www.amazon.com/s?field-keywords={search_term}&ref=cs_503_search")
                # 等待页面加载
                WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.s-result-item")))
                
                # 滚动页面加载内容
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(0.1)

                items = driver.find_elements(By.CSS_SELECTOR, "div.s-result-item")
                # 忽略第一个和最后三个元素
                items = items[1:-3] if len(items) > 3 else []
                
                products = []
                for item in items:
                    
                    try:
                        # 从图片的 alt 属性中提取商品名称
                        name = item.find_element(By.CSS_SELECTOR, ".s-image").get_attribute("alt")
                    except:
                        name = "N/A"

                    try:
                        # 提取价格
                        price = item.find_element(By.CSS_SELECTOR, '[class="a-offscreen"]').get_attribute("textContent")
                    except Exception as e:
                        print(f"Error extracting price: {e}")
                        price = "N/A"
                    #<span class="a-icon-alt">4.6 颗星，最多 5 颗星</span>
                    try:
                        # 提取价格
                        rating = item.find_element(By.CSS_SELECTOR, '[class="a-icon-alt"]').get_attribute("textContent")
                    except Exception as e:
                        print(f"Error extracting price: {e}")
                        rating = "N/A"
                    try:
                        # 提取链接
                        href = item.find_element(By.CSS_SELECTOR, '[class="a-link-normal s-line-clamp-2 s-link-style a-text-normal"]').get_attribute("href")
                    except Exception as e:
                        print(f"Error extracting price: {e}")
                        href = "N/A"
                    #<a class="a-link-normal s-line-clamp-2 s-link-style a-text-normal" href="/-/zh_TW/Razer-Basilisk-%E5%8F%AF%E8%87%AA%E8%A8%82%E4%BA%BA%E9%AB%94%E5%B7%A5%E5%AD%B8%E9%81%8A%E6%88%B2%E6%BB%91%E9%BC%A0-%E6%9C%80%E5%BF%AB%E7%9A%84%E9%81%8A%E6%88%B2%E6%BB%91%E9%BC%A0%E9%96%8B%E9%97%9C-HyperScroll/dp/B09C13PZX7/ref=sr_1_1?crid=32EHV3ZS7LMOX&amp;dib=eyJ2IjoiMSJ9.Skc8JUXV1jAk34eXQfiFzJFUtNZ54Nku_AWC2A3MERxC_g1I5Q78Dd-HvjR9e9u-DG3beDyDazZbxyQqgqOszUQH8s0o62mgEliXyW8xr3EXn2oF6EcgAiSdpwaVXgkV7dBtwky4KuuBMo53lGaZLSaKMQpKtyqW8rzToQFDRWkAArpp4oceGf54FFfZht_rwTZ3nNPKI_U37Qr4rL2fsmt9_-YUs8Enb5ZqWT5ePS4.WMq3WU2DDiV0GJIxNYlJxuCJVzGPv6nBNUJO_Ym6uaA&amp;dib_tag=se&amp;keywords=%E9%BC%A0%E6%A0%87&amp;qid=1734004403&amp;sprefix=shu%27biao%2Caps%2C540&amp;sr=8-1"><h2 aria-label="Razer Basilisk V3 可自訂人體工學遊戲滑鼠:最快的遊戲滑鼠開關 - Chroma RGB 照明 - 26K DPI 光學感測器 - 11 個可編程按鈕 - HyperScroll 傾斜滾輪 - 經典黑色" class="a-size-medium a-spacing-none a-color-base a-text-normal"><span>Razer Basilisk V3 可自訂人體工學遊戲滑鼠:最快的遊戲滑鼠開關 - Chroma RGB 照明 - 26K DPI 光學感測器 - 11 個可編程按鈕
                    products.append({
                        'name': name,
                        'price': price,
                        'rating': rating,
                        'href': href
                    })
                
                return products
            except Exception as e:
                
                print(f"尝试 {attempt + 1} 次失败: {str(e)}")
                if attempt < max_attempts - 1:
                    time.sleep(random.uniform(0.1, 3))  # 随机等待时间重试
                    driver.quit()
                else:
                    print("多次尝试后仍然失败，可能需要检查网络连接或更换策略。")
                    return []
    finally:
        print("关闭浏览器...")
        driver.quit()

if __name__ == "__main__":
    search_term = input("请输入搜索关键词: ")
    products = amazon_crawler_with_selenium(search_term)
    if products:
        print(f"成功获取到 {len(products)} 个商品信息：")
        for product in products:
            print(f"商品名称: {product['name']}")
            print(f"价格: {product['price']}")
            print(f"评级: {product['rating']}")
            print(f"链接: {product['href']}")
            print("---")
    else:
        print("未能成功获取商品信息。")