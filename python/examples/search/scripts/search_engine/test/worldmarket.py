from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random

def worldmarket_crawler_with_selenium(search_term, timeout=10, max_attempts=3):
    firefox_options = Options()
    #firefox_options.add_argument("--headless")  # 如果在无头模式下运行
    
    try:
        for attempt in range(max_attempts):
            try:
                driver = webdriver.Firefox(options=firefox_options)
                driver.get(f"https://www.worldmarket.com/search?q={search_term}&search-button=&lang=en_US")
               
                # 等待页面加载
                WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.product.js-a-tile-data")))
                
                # 滚动页面加载内容
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)  # 增加等待时间，确保页面完全加载

                items = driver.find_elements(By.CSS_SELECTOR, "div.product.js-a-tile-data")
                # 忽略第一个和最后三个元素
                items = items[1:-3] if len(items) > 3 else []
                
                products = []
                for item in items:
                    try:
                        # 从图片的 alt 属性中提取商品名称
                        name = item.find_element(By.CSS_SELECTOR, ".tile-alt-image").get_attribute("alt")
                    except:
                        name = "N/A"

                    try:
                        # 提取价格
                        price_element = item.find_element(By.CSS_SELECTOR, 'div.price span.value')
                        price = price_element.get_attribute('content')
                    except Exception as e:
                        print(f"Error extracting price: {e}")
                        price = "N/A"

                    try:
                        # 提取评级
                        rating = item.get_attribute('data-rating')
                    except Exception as e:
                        print(f"Error extracting rating: {e}")
                        rating = "N/A"

                    try:
                        # 提取链接
                        href = item.find_element(By.CSS_SELECTOR, "h2.pdp-link a").get_attribute("href")
                    except Exception as e:
                        print(f"Error extracting link: {e}")
                        href = "N/A"

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
                    time.sleep(random.uniform(1, 3))  # 随机等待时间重试
                else:
                    print("多次尝试后仍然失败，可能需要检查网络连接或更换策略。")
                    return []
            finally:
                driver.quit()
    except Exception as e:
        print(f"发生未预期的错误: {str(e)}")
        return []

if __name__ == "__main__":
    search_term = input("请输入搜索关键词: ")
    products = worldmarket_crawler_with_selenium(search_term)
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