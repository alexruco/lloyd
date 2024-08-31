# bing_organic_results_selenium.py

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
from ignore_patterns_list import ignore_patterns
from datetime import datetime

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


def get_bing_organic_links(query, page=1):
    # Setup Selenium WebDriver
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
    
    page_source = driver.page_source
    
    driver.quit()  # Close the browser
    
    # Parse the page source with BeautifulSoup
    soup = BeautifulSoup(page_source, 'html.parser')
    
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

def process_links(links_by_page):
    # Dictionary to store the minimum position for each URL
    url_min_position = {}
    position_counter = 1
    
    for page_number, links in links_by_page.items():
        for link in links:
            if link not in url_min_position:
                url_min_position[link] = position_counter
            position_counter += 1
    
    # Convert dictionary to a list of tuples and sort by the position
    sorted_url_min_position = sorted(url_min_position.items(), key=lambda x: x[1])
    
    return sorted_url_min_position

def fetch_pages_content(urls_with_positions, max_position):
    # Setup Selenium WebDriver
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    results = {}
    
    for url, position in urls_with_positions:
        if position > max_position:
            break
        
        # Fetch the page
        driver.get(url)
        time.sleep(2)  # Let the page load completely
        page_source = driver.page_source
        
        # Parse the page source with BeautifulSoup
        soup = BeautifulSoup(page_source, 'html.parser')
        
        # Extract title
        title = soup.title.string if soup.title else "No title"
        
        # Try to extract meta description
        meta_description = ""
        meta_tag = soup.find("meta", attrs={"name": "description"})
        if meta_tag:
            meta_description = meta_tag.get("content", "")
        
        # If no meta description, try to extract headers and first paragraph
        if not meta_description:
            headers = []
            for header_tag in ['h1', 'h2', 'h3']:
                header = soup.find(header_tag)
                if header:
                    headers.append(header.get_text(strip=True))
            
            first_paragraph = ""
            first_p_tag = soup.find('p')
            if first_p_tag:
                first_paragraph = first_p_tag.get_text(strip=True)
            
            # Combine headers and first paragraph as an alternative to meta description
            meta_description = " ".join(headers + [first_paragraph]).strip()
        
        # Store the result in a dictionary keyed by URL
        results[url] = {
            "position": position,
            "title": title,
            "meta_description": meta_description
        }
    
    driver.quit()  # Close the browser
    
    return results

def search_and_fetch_content(search_term, max_position):
    # Initialize data structure to hold links by page
    links_by_page = {}
    
    # Scrape multiple pages of Bing search results
    for page in range(1, 6):  # Modify this range if you want to scrape more/less pages
        links = get_bing_organic_links(search_term, page)
        if links:
            links_by_page[page] = links
        else:
            break
        
        # Be polite and delay before making another request
        time.sleep(2)
    
    # Process the collected links to get their positions
    processed_links = process_links(links_by_page)
    
    # Fetch content from pages up to the specified max position
    page_content = fetch_pages_content(processed_links, max_position)
    
    return page_content
