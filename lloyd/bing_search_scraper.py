# file: bing_search_scraper.py

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
    # Initialize a list to hold all the URLs from multiple pages
    all_urls = []

    for page in range(1, pages + 1):
        urls = get_bing_organic_links(query, page)
        if urls:
            all_urls.extend(urls)
        else:
            break
        time.sleep(2)  # Be polite and delay before making another request

    return all_urls

def get_bing_organic_links(query, page=1):
    # Setup Selenium WebDriver with UTF-8 encoding in mind
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    # Format the query to replace spaces with '+'
    formatted_query = query.replace(' ', '+')
    
    # Calculate the `first` parameter value based on the page number
    start_index = (page - 1) * 10 + 1  # Page 1 -> first=1, Page 2 -> first=11, etc.
    
    # Bing search URL with pagination
    url = f'https://www.bing.com/search?q={formatted_query}&first={start_index}'
    
    # Use Selenium to fetch the page
    driver.get(url)
    
    try:
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'li.b_algo')))
    except TimeoutException:
        print("Element not found, printing page source for debugging.")
        print(driver.page_source)  # Print the page source for diagnosis
        driver.quit()
        raise
    
    # Fetch page source and close driver
    page_source = driver.page_source
    driver.quit()
    
    # Parse the page source with BeautifulSoup, ensuring UTF-8 encoding
    soup = BeautifulSoup(page_source, 'html.parser', from_encoding='utf-8')
    
    # Find all organic search result links
    organic_links = []
    for a_tag in soup.find_all('a', href=True):
        href = a_tag['href']
        # Filter out non-organic links (ads, Bing's internal links, etc.)
        if href.startswith('http') and not 'bing.com' in href:
            organic_links.append(href)
    
    # Apply the filter to remove unwanted URLs
    filtered_links = filter_bing_results(organic_links)
    return filtered_links

def filter_bing_results(urls):
    filtered_urls = []
    for url in urls:
        if not any(pattern in url for pattern in ignore_patterns):
            filtered_urls.append(url)
    
    return filtered_urls

def save_urls_to_file(urls, filename='output.txt'):
    # Save the URLs to a file, ensuring UTF-8 encoding
    with open(filename, 'w', encoding='utf-8') as f:
        for url in urls:
            f.write(url + '\n')

# Example usage
if __name__ == "__main__":
    search_query = "melhorar website"
    urls = get_search_result_urls(search_query, pages=5)
    save_urls_to_file(urls)
