from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import chromedriver_autoinstaller
import sys

# 映射要素名称到URL片段
ELEMENT_URL_MAP = {
    '雷达': ('%E6%B0%94%E8%B1%A1%E9%9B%B7%E8%BE%BE-radar', 'radar'),
    '卫星云图': ('%E5%8D%AB%E6%98%9F%E4%BA%91%E5%9B%BE-satellite', 'satellite'),
    'Radar+': ('Radar+-radarPlus', 'radarPlus'),
    '雨、雷暴': ('%E9%9B%A8%E3%80%81%E9%9B%B7%E6%9A%B4-rain', 'rain'),
    '温度': ('%E6%B8%A9%E5%BA%A6-temp', 'temp'),
    '云': ('%E4%BA%91-clouds', 'clouds'),
    '海浪': ('%E6%B5%B7%E6%B5%AA-waves', 'waves'),
    '降雨量': ('%E9%99%8D%E9%9B%A8%E9%87%8F-rainAccu?rainAccu,next3d', 'rainAccu,next3d'),
    # 添加更多要素名称和对应的URL片段
}

def download_windy_image(element_name, latitude, longitude, zoom_level, output_filename):
    # 自动下载和安装匹配的ChromeDriver
    chromedriver_autoinstaller.install()

    # 创建一个新的浏览器实例
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # 无头模式
    options.add_argument('--disable-gpu')  # 禁用GPU
    options.add_argument('--window-size=1920,1080')  # 设置窗口大小

    # 创建一个Service对象（不需要指定路径，chromedriver_autoinstaller已处理）
    service = Service()

    driver = webdriver.Chrome(service=service, options=options)

    # 根据要素名称生成URL片段
    url_elements = ELEMENT_URL_MAP.get(element_name)
    if not url_elements:
        print(f"未知的要素名称: {element_name}")
        return

    # 打开Windy.com的页面
    url = f'https://www.windy.com/zh/-{url_elements[0]}?{url_elements[1]},{latitude},{longitude},{zoom_level}'
    driver.get(url)

    # 等待页面加载完成
    wait = WebDriverWait(driver, 20)  # 增加等待时间
    element = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "leaflet-pane")))

    # 给一点额外的时间让地图完全加载
    time.sleep(5)

    # 保存快照
    driver.save_screenshot(output_filename)

    # 关闭浏览器
    driver.quit()

if __name__ == "__main__":
    if len(sys.argv) != 6:
        print("Usage: python script.py <element_name> <latitude> <longitude> <zoom_level> <output_filename>")
        sys.exit(1)

    element_name = sys.argv[1]
    latitude = sys.argv[2]
    longitude = sys.argv[3]
    zoom_level = sys.argv[4]
    output_filename = sys.argv[5]

    download_windy_image(element_name, latitude, longitude, zoom_level, output_filename)