from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import argparse
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
from product_analysis_agent import ProductAnalysisAgent, prompt_template
from dotenv import load_dotenv
import os
from typing import List
from shopping_result import HtmlSearchTextChunk

def setup_selenium_driver(driver_path: str, headless: bool = True) -> webdriver.Chrome:
    """
    Set up the Selenium WebDriver.

    Args:
        driver_path (str): Path to the ChromeDriver executable.
        headless (bool): Whether to run in headless mode.

    Returns:
        webdriver.Chrome: Configured WebDriver instance.
    """
    chrome_options = Options()
    if headless:
        chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920x1080")
    chrome_options.add_argument("log-level=3")

    service = Service(driver_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

def fetch_product_cards(driver_path: str, url_template: str, query: str, site_name: str, card_class_prefix: str, scroll: bool = True, wait_time: int = 10) -> list:
    """
    Fetches and extracts product cards based on a class prefix.

    Args:
        driver_path (str): Path to the ChromeDriver executable.
        url_template (str): URL template for the search query.
        query (str): Search keyword to query.
        site_name (str): Name of the site for logging purposes.
        card_class_prefix (str): Class prefix to match the product cards.
        scroll (bool): Whether to enable scrolling for dynamic content loading.
        wait_time (int): Maximum wait time for elements to load.

    Returns:
        list: List of product card HTML content.
    """
    url = url_template.format(query=query)
    driver = setup_selenium_driver(driver_path, headless=True)

    try:
        print(f"[INFO] Fetching results from {site_name}: {url}")
        driver.get(url)
        WebDriverWait(driver, wait_time).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )

        if scroll:
            print("[INFO] Scrolling to load dynamic content...")
            last_height = driver.execute_script("return document.body.scrollHeight")
            while True:
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)
                new_height = driver.execute_script("return document.body.scrollHeight")
                if new_height == last_height:
                    break
                last_height = new_height
                
        # Debugging: Check if the page source contains product cards
        print("[DEBUG] Checking page source for product cards...")
        page_source = driver.page_source
        print("[DEBUG] Page source length:", len(page_source))

        # Locate product cards using XPath
        card_selector = f"//*[contains(@class, '{card_class_prefix}')]"
        print(f"[DEBUG] Using selector: {card_selector}")
        WebDriverWait(driver, wait_time).until(
            EC.presence_of_all_elements_located((By.XPATH, card_selector))
        )
        card_elements = driver.find_elements(By.XPATH, card_selector)
        print(f"[INFO] Found {len(card_elements)} product cards on {site_name}.")
        return [card.get_attribute("outerHTML") for card in card_elements]

    except Exception as e:
        print(f"[ERROR] Failed to fetch product cards from {site_name}: {type(e).__name__} - {str(e)}")
        return []
    finally:
        driver.quit()

def format_product_cards(card_html_list: list) -> str:
    soup = BeautifulSoup("".join(card_html_list), "html.parser")
    # Remove unnecessary script or style tags
    for tag in soup(["script", "style"]):
        tag.decompose()
    # Clean up white spaces and inline styles
    for element in soup.find_all(True):
        if "style" in element.attrs:
            del element.attrs["style"]
    # Format the HTML content for readability
    return soup.prettify()

def save_to_file(content: str, filename: str):
    """
    Saves the given content to a file.

    Args:
        content (str): Content to save.
        filename (str): Filename to save the content to.
    """
    try:
        with open(filename, "w", encoding="utf-8") as file:
            file.write(content)
        print(f"[INFO] Content saved to {filename}")
    except IOError as e:
        print(f"[ERROR] Failed to save content to {filename}: {e}")
        
def add_url_prefix(chunks: List[HtmlSearchTextChunk], prefix: str) -> List[HtmlSearchTextChunk]:
    """
    Add a URL prefix to all HtmlSearchTextChunk objects in the list.

    Args:
        chunks (List[HtmlSearchTextChunk]): List of HtmlSearchTextChunk objects.
        prefix (str): The prefix to be added to the URL field.

    Returns:
        List[HtmlSearchTextChunk]: Updated list of HtmlSearchTextChunk objects with prefixed URLs.
    """
    for chunk in chunks:
        if chunk.url and not chunk.url.startswith("http"):
            chunk.url = f"{prefix}{chunk.url}"
    return chunks

if __name__ == "__main__": # python search.py --driver-path /usr/bin/chromedriver --search-keyword "cup"
    parser = argparse.ArgumentParser(description="Fetch product cards using Selenium.")
    parser.add_argument("--driver-path", required=True, help="Path to the ChromeDriver executable.")
    parser.add_argument("--search-keyword", default="lights", help="Search keyword to query.")
    parser.add_argument("--save", "-s", action="store_true", help="Save formatted HTML to files.")
    args = parser.parse_args()
    
    
    # Initialize the ProductAnalysisAgent
    load_dotenv()
    api_key = os.getenv("API_KEY")
    agent = ProductAnalysisAgent(
        api_key=api_key,
        # base_url="https://api.siliconflow.cn/v1",
    )

    """
    # Balsam Hill
    balsamhill_template = "https://www.balsamhill.com/search?text={query}&sort=relevanceSort"
    balsamhill_card_class_prefix = "productCard_product-listing-card-wrapper__"
    balsamhill_cards = fetch_product_cards(
        args.driver_path, balsamhill_template, args.search_keyword, "Balsam Hill", balsamhill_card_class_prefix, scroll=True
    )
    if balsamhill_cards:
        formatted_balsamhill = format_product_cards(balsamhill_cards)
        if args.save:
            save_to_file(formatted_balsamhill, f"balsamhill_{args.search_keyword}_cards.html")
        balsamhill_results = agent.process_cards(balsamhill_cards, "gpt-4o-mini", 32000, prompt_template, args.search_keyword)
        print("[INFO] Balsam Hill Results:")
        print(balsamhill_results)
    """
    
    # Christmas Lights Etc
    christmaslightsetc_template = "https://www.christmaslightsetc.com/browse/?q={query}"
    christmaslightsetc_card_class = "thumbnail pBox"
    christmaslightsetc_cards = fetch_product_cards(
        args.driver_path, christmaslightsetc_template, args.search_keyword, "Christmas Lights Etc", christmaslightsetc_card_class, scroll=True
    )
    if christmaslightsetc_cards:
        formatted_christmaslightsetc = format_product_cards(christmaslightsetc_cards)
        if args.save:
            save_to_file(formatted_christmaslightsetc, f"christmaslightsetc_{args.search_keyword}_cards.html")
        christmaslightsetc_results = agent.process_cards(christmaslightsetc_cards, "gpt-4o-mini", 32000, prompt_template, args.search_keyword)
        # Add URL prefix for Christmas Lights Etc
        christmaslightsetc_results.chunks = add_url_prefix(
            christmaslightsetc_results.chunks, 
            "https://www.christmaslightsetc.com"
        )
        print("[INFO] Christmas Lights Etc Results:")
        print(christmaslightsetc_results)
    
        