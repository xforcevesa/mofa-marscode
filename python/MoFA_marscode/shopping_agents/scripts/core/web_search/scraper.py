from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
import time
from .product_analysis_agent import ProductAnalysisAgent, prompt_template
import os
from typing import List
from .shopping_result import HtmlSearchTextChunk


class ProductScraper:
    """
    A product scraper that can fetch product cards from a given e-commerce site.

    Attributes:
        driver_path (str): Path to the ChromeDriver executable.
        headless (bool): Run browser in headless mode.
        wait_time (int): Maximum wait time for elements to load.
    """

    def __init__(self, driver_path: str, headless: bool = True, wait_time: int = 10):
        self.driver_path = driver_path
        self.headless = headless
        self.wait_time = wait_time
        self.driver = None

    def _setup_selenium_driver(self) -> webdriver.Chrome:
        """
        Private method to set up the Selenium WebDriver.
        """
        chrome_options = Options()
        if self.headless:
            chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--window-size=1920x1080")
        chrome_options.add_argument("log-level=3")

        service = Service(self.driver_path)
        driver = webdriver.Chrome(service=service, options=chrome_options)
        return driver

    def _scroll_to_load_content(self):
        """
        Private method to scroll through the page to load dynamic content.
        """
        last_height = self.driver.execute_script("return document.body.scrollHeight")
        while True:
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

    def fetch_product_cards(
        self, 
        url_template: str,
        query: str,
        site_name: str,
        selector_type: str,
        selector_value: str,
        scroll: bool = True
    ) -> list:
        """
        Fetches and extracts product cards from a given site.

        Args:
            url_template (str): URL template with a placeholder `{query}` for the search keyword.
            query (str): Search keyword to query.
            site_name (str): Name of the site for logging purposes.
            selector_type (str): The type of selector ('class', 'data-testid', etc.).
            selector_value (str): The value of the selector to match product cards.
            scroll (bool): Whether to enable scrolling for dynamic content loading.

        Returns:
            list: List of product card HTML content.
        """
        url = url_template.format(query=query)
        self.driver = self._setup_selenium_driver()

        try:
            print(f"[INFO] Fetching results from {site_name}: {url}")
            self.driver.get(url)
            WebDriverWait(self.driver, self.wait_time).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )

            if scroll:
                print("[INFO] Scrolling to load dynamic content...")
                self._scroll_to_load_content()

            # Construct the XPATH selector based on selector type
            if selector_type == "class":
                card_selector = f"//*[contains(@class, '{selector_value}')]"
            elif selector_type == "data-testid":
                card_selector = f"//*[@data-testid='{selector_value}']"
            else:
                raise ValueError(f"Unsupported selector type: {selector_type}")

            print(f"[DEBUG] Using selector: {card_selector}")
            try:
                WebDriverWait(self.driver, self.wait_time).until(
                    EC.presence_of_all_elements_located((By.XPATH, card_selector))
                )
            except TimeoutException:
                print(f"[INFO] No product cards found for query '{query}' on {site_name}. Returning empty list.")
                return []
            card_elements = self.driver.find_elements(By.XPATH, card_selector)
            print(f"[INFO] Found {len(card_elements)} product cards on {site_name}.")
            return [card.get_attribute("outerHTML") for card in card_elements]

        except Exception as e:
            print(f"[ERROR] Failed to fetch product cards from {site_name}: {type(e).__name__} - {str(e)}")
            return []
        finally:
            if self.driver:
                self.driver.quit()
                self.driver = None

    def format_product_cards(self, card_html_list: list) -> str:
        """
        Format the product card HTML for better readability and remove unnecessary tags/attributes.
        """
        soup = BeautifulSoup("".join(card_html_list), "html.parser")
        # Remove script and style tags
        for tag in soup(["script", "style"]):
            tag.decompose()
        # Clean up inline styles
        for element in soup.find_all(True):
            if "style" in element.attrs:
                del element.attrs["style"]
        return soup.prettify()

    def save_to_file(self, content: str, filename: str):
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

    def add_url_prefix(self, chunks: List[HtmlSearchTextChunk], prefix: str) -> List[HtmlSearchTextChunk]:
        """
        Add a URL prefix to all HtmlSearchTextChunk objects in the list.

        Args:
            chunks (List[HtmlSearchTextChunk]): List of HtmlSearchTextChunk objects.
            prefix (str): The prefix to be added to the URL field.

        Returns:
            List[HtmlSearchTextChunk]: Updated list with prefixed URLs.
        """
        for chunk in chunks:
            if chunk.url and not chunk.url.startswith("http"):
                chunk.url = f"{prefix}{chunk.url}"
        return chunks

    def scrape(
        self,
        url_template: str,
        query: str,
        site_name: str,
        selector_type: str,
        selector_value: str,
        analysis_agent: ProductAnalysisAgent,
        model_name: str,
        max_tokens: int,
        prompt_template: str,
        scroll: bool = True,
        save: bool = False,
        limit_num:int=10,
    ):
        """
        High-level method to perform the scraping, formatting, optional saving, and analysis.

        Args:
            url_template (str): URL template with `{query}` placeholder.
            query (str): Search keyword.
            site_name (str): Name of the site.
            selector_type (str): 'class' or 'data-testid'.
            selector_value (str): Selector value to locate product cards.
            analysis_agent (ProductAnalysisAgent): The agent to process product cards.
            model_name (str): The model name used by the analysis agent.
            max_tokens (int): Maximum tokens for analysis.
            prompt_template (str): Template for product analysis prompt.
            scroll (bool): Whether to scroll.
            save (bool): Whether to save the formatted HTML.
        """
        cards = self.fetch_product_cards(
            url_template=url_template,
            query=query,
            site_name=site_name,
            selector_type=selector_type,
            selector_value=selector_value,
            scroll=scroll
        )
        if len(cards)>limit_num:
            cards = cards[:limit_num]

        if cards:
            formatted = self.format_product_cards(cards)
            if save:
                filename = f"{site_name.replace(' ', '')}_{query}_cards.html"
                self.save_to_file(formatted, filename)
            results = analysis_agent.process_cards(cards, model_name, max_tokens, prompt_template, query)
            print(f"[INFO] {site_name} Results:")
            print(results)
            return results
        else:
            return None

def christmaslightsetc_scraper(search_keyword:str,driver_path:str=None,save:bool=False,limit_num:int=10,api_key:str=os.getenv("API_KEY")):

    # api_key = os.getenv("API_KEY")
    agent = ProductAnalysisAgent(
        api_key=api_key,
    )

    scraper = ProductScraper(driver_path=driver_path, headless=True, wait_time=10)
    """
    # Balsam Hill
    balsamhill_template = "https://www.balsamhill.com/search?text={query}&sort=relevanceSort"
    balsamhill_results = scraper.scrape(
        url_template=balsamhill_template,
        query=args.search_keyword,
        site_name="Balsam Hill",
        selector_type="class",
        selector_value="productCard_product-listing-card-wrapper__",
        analysis_agent=agent,
        model_name="gpt-4o-mini",
        max_tokens=32000,
        prompt_template=prompt_template,
        scroll=True,
        save=args.save
    )
    """

    # Christmas Lights Etc
    christmaslightsetc_template = "https://www.christmaslightsetc.com/browse/?q={query}"
    christmaslightsetc_results = scraper.scrape(
        url_template=christmaslightsetc_template,
        query=search_keyword,
        site_name="Christmas Lights Etc",
        selector_type="class",
        selector_value="thumbnail pBox",
        analysis_agent=agent,
        model_name="gpt-4o-mini",
        max_tokens=120000,
        prompt_template=prompt_template,
        scroll=True,
        save=save,limit_num=limit_num
    )
    if christmaslightsetc_results:
        # Add URL prefix for Christmas Lights Etc
        christmaslightsetc_results.chunks = scraper.add_url_prefix(
            christmaslightsetc_results.chunks,
            "https://www.christmaslightsetc.com"
        )
        print("[INFO] Christmas Lights Etc Results with updated URLs:")
        print(christmaslightsetc_results)
        return christmaslightsetc_results
    return ''
def notonthehighstreet_scraper(search_keyword:str,driver_path:str=None,save:bool=False,limit_num:int=10,api_key:str=os.getenv("API_KEY")):
    agent = ProductAnalysisAgent(
        api_key=api_key,
    )

    scraper = ProductScraper(driver_path=driver_path, headless=True, wait_time=10)
    notonthehighstreet_template = "https://www.notonthehighstreet.com/search?term={query}"
    notonthehighstreet_results = scraper.scrape(
        url_template=notonthehighstreet_template,
        query=search_keyword,
        site_name="Not On The High Street",
        selector_type="data-testid",
        selector_value="product-card",
        analysis_agent=agent,
        model_name="gpt-4o-mini",
        max_tokens=96000,
        prompt_template=prompt_template,
        scroll=True,
        save=save
    )
    if notonthehighstreet_results:
        # Add URL prefix for Not On The High Street
        notonthehighstreet_results.chunks = scraper.add_url_prefix(
            notonthehighstreet_results.chunks,
            "https://www.notonthehighstreet.com"
        )
        print("[INFO] Not On The High Street Results with updated URLs:")
        print(notonthehighstreet_results)
        return notonthehighstreet_results
    return ''

# if __name__ == "__main__": # python scraper.py --driver-path /usr/bin/chromedriver --search-keyword "cup" -s
#     parser = argparse.ArgumentParser(description="Fetch product cards using Selenium.")
#     parser.add_argument("--driver-path", default=None, help="Path to the ChromeDriver executable.")
#     parser.add_argument("--search-keyword", default="lights", help="Search keyword to query.")
#     parser.add_argument("--save", "-s", action="store_true", help="Save formatted HTML to files.")
#     args = parser.parse_args()
#
#     load_dotenv('.env.secret')
#     api_key = os.getenv("API_KEY")
#     agent = ProductAnalysisAgent(
#         api_key=api_key,
#     )
#
#     scraper = ProductScraper(driver_path=args.driver_path, headless=True, wait_time=10)
#     """
#     # Balsam Hill
#     balsamhill_template = "https://www.balsamhill.com/search?text={query}&sort=relevanceSort"
#     balsamhill_results = scraper.scrape(
#         url_template=balsamhill_template,
#         query=args.search_keyword,
#         site_name="Balsam Hill",
#         selector_type="class",
#         selector_value="productCard_product-listing-card-wrapper__",
#         analysis_agent=agent,
#         model_name="gpt-4o-mini",
#         max_tokens=32000,
#         prompt_template=prompt_template,
#         scroll=True,
#         save=args.save
#     )
#     """
#
#     # Christmas Lights Etc
#     christmaslightsetc_template = "https://www.christmaslightsetc.com/browse/?q={query}"
#     christmaslightsetc_results = scraper.scrape(
#         url_template=christmaslightsetc_template,
#         query=args.search_keyword,
#         site_name="Christmas Lights Etc",
#         selector_type="class",
#         selector_value="thumbnail pBox",
#         analysis_agent=agent,
#         model_name="gpt-4o-mini",
#         max_tokens=120000,
#         prompt_template=prompt_template,
#         scroll=True,
#         save=args.save
#     )
#     if christmaslightsetc_results:
#         # Add URL prefix for Christmas Lights Etc
#         christmaslightsetc_results.chunks = scraper.add_url_prefix(
#             christmaslightsetc_results.chunks,
#             "https://www.christmaslightsetc.com"
#         )
#         print("[INFO] Christmas Lights Etc Results with updated URLs:")
#         print(christmaslightsetc_results)
#     """
#     # Not On The High Street
#     notonthehighstreet_template = "https://www.notonthehighstreet.com/search?term={query}"
#     notonthehighstreet_results = scraper.scrape(
#         url_template=notonthehighstreet_template,
#         query=args.search_keyword,
#         site_name="Not On The High Street",
#         selector_type="data-testid",
#         selector_value="product-card",
#         analysis_agent=agent,
#         model_name="gpt-4o-mini",
#         max_tokens=32000,
#         prompt_template=prompt_template,
#         scroll=True,
#         save=args.save
#     )
#     if notonthehighstreet_results:
#         # Add URL prefix for Not On The High Street
#         notonthehighstreet_results.chunks = scraper.add_url_prefix(
#             notonthehighstreet_results.chunks,
#             "https://www.notonthehighstreet.com"
#         )
#         print("[INFO] Not On The High Street Results with updated URLs:")
#         print(notonthehighstreet_results)
#     """
    