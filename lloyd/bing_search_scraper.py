# filename: bing_search_scraper.py

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
from ignore_patterns_list import ignore_patterns
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

def get_search_result_urls(query, pages=5):
    all_urls = set()  # Using a set to store unique URLs

    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    try:
        for page in range(1, pages + 1):
            urls = get_bing_organic_links(driver, query, page)
            if urls:
                all_urls.update(urls)  # Use update to add items to the set
            else:
                break
            time.sleep(2)
    finally:
        driver.quit()

    return list(all_urls)  # Convert the set back to a list

def get_bing_organic_links(driver, query, page=1):
    formatted_query = query.replace(' ', '+')
    start_index = (page - 1) * 10 + 1
    url = f'https://www.bing.com/search?q={formatted_query}&first={start_index}'

    driver.get(url)

    try:
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'li.b_algo')))
    except TimeoutException:
        print(f"Timeout while loading page {page} for query: {query}")
        return []
    
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'html.parser')

    organic_links = []
    for a_tag in soup.find_all('a', href=True):
        href = a_tag['href']
        if href.startswith('http') and not 'bing.com' in href:
            organic_links.append(href)

    filtered_links = filter_bing_results(organic_links)
    return filtered_links

def filter_bing_results(urls):
    filtered_urls = []
    for url in urls:
        if not any(pattern in url for pattern in ignore_patterns):
            filtered_urls.append(url)
    return filtered_urls
