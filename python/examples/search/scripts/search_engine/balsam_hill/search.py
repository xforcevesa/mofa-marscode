import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

def fetch_webpage(url):
    ua = UserAgent()
    headers = {
        'User-Agent': ua.random,
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive'
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        # 确保解码为文本
        response.encoding = response.apparent_encoding
        if 'text/html' in response.headers.get('Content-Type', ''):
            return response.text
        else:
            print("The response is not an HTML page.")
            return None
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None

def parse_and_save_content(html_content, output_file="output.html"):
    if not html_content:
        print("No content to save.")
        return

    # 使用 BeautifulSoup 解析 HTML
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # 保存为 UTF-8 编码的 HTML 文件
    with open(output_file, "w", encoding="utf-8") as file:
        file.write(soup.prettify())
    
    print(f"HTML content saved to {output_file}")

if __name__ == "__main__":
    url = "https://www.balsamhill.com/search?text=phone&sort=relevanceSort"
    html_content = fetch_webpage(url)

    if html_content:
        parse_and_save_content(html_content)
