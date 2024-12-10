import time
import json
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

def login_and_search(username: str, password: str, search_text: str):
    driver = uc.Chrome(headless=False)
    driver.get("https://www.bestbuy.com/identity/signin?token=tid%3A613cc6bf-b6c5-11ef-9fbe-06e75fa51e49")
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "fld-e"))
    )

    driver.find_element(By.ID, "fld-e").send_keys(username)
    driver.find_element(By.ID, "fld-p1").send_keys(password + Keys.RETURN)

    time.sleep(5)  

    skip_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button.c-button-link:nth-child(2)"))
    )
    skip_button.click()

    search_box = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "st"))
    )
    search_box.send_keys(search_text + Keys.RETURN)

    time.sleep(5)

    return driver.page_source, driver


# extractor
def extract_product_info(html_content: str):
    soup = BeautifulSoup(html_content, 'html.parser')

    description_tag = soup.select_one("#shop-sku-list-item-49989714 > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > h4:nth-child(2) > a:nth-child(1)")
    description = description_tag.text.strip() if description_tag else "N/A"

    model_info = {}
    model_tags = soup.select("#shop-sku-list-item-49989714 > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(3) > div:nth-child(1) > div:nth-child(1) > span")
    if len(model_tags) >= 2:
        model_info[model_tags[0].text.strip()] = model_tags[1].text.strip()
    other_tags = soup.select("#shop-sku-list-item-49989714 > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(3) > div:nth-child(1) > div:nth-child(2) > span")
    if len(other_tags) >= 2:
        model_info[other_tags[0].text.strip()] = other_tags[1].text.strip()

    price_tag = soup.select_one("#pricing-price-64676021 > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > span:nth-child(1)")
    price = price_tag.text.strip() if price_tag else "N/A"
    result = {
        "description": description,
        "model_info": model_info,
        "price": price
    }

    return result

if __name__ == "__main__":
    username = "juantan@onionmail.org"
    password = "b~U3zVHb.H*mt^!X24yd"
    search_text = "HP Laptop"
    html_source, driver = login_and_search(username, password, search_text)
    product_info = extract_product_info(html_source)
    print(json.dumps(product_info, indent=4))
