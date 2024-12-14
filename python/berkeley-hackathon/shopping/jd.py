import undetected_chromedriver as uc
import time
from openai import OpenAI
from util import *

def read_cookie_request_url(url:str='https://www.jd.com/',search_text:str='mac mini4 '):


    options = uc.ChromeOptions()
    # options.add_argument(
    #     "--user-data-dir=/Users/chenzi/Library/Application Support/Google/Chrome/Default")  # 替换为你的用户数据目录
    # options.add_argument("--profile-directory=Default")  # 使用默认配置文件

    # driver = uc.Chrome(headless=False, use_subprocess=False, options=options)
    driver = uc.Chrome(headless=False, use_subprocess=False,)
    driver.get(url)
    time.sleep(5)
    input_search_selector = '#key'
    input_search_button_selector = '#search > div > div.form.hotWords > button'

    driver.find_element(by='css selector', value=input_search_selector).send_keys(search_text)
    driver.find_element(by='css selector', value=input_search_button_selector).click()
    time.sleep(10)
    html_context = driver.page_source
    driver.quit()
    return html_context

if __name__ == '__main__':
    # login_jd()
    home_page_url = 'https://www.jd.com/'
    search_text = "mac mini 4 "
    html_source = read_cookie_request_url(url=home_page_url,search_text=search_text)
    # clena_html_source = clean_html_js_and_style(html_source)
    api_key = "sk-"
    llm_client = OpenAI(api_key=api_key)
    result = shopping_html_structure(llm_client=llm_client,html_content=html_source,search_text=search_text)
    print(result)
    # result = process_large_html_content(html_content=clena_html_source,llm_client=client,search_text=search_text)
    # print(result)




