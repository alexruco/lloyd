#fetch_content.py

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
from selenium.common.exceptions import WebDriverException

def fetch_content_from_url(url, text_limit=2000, retries=3):
    # Retry logic to handle intermittent WebDriver issues
    attempt = 0
    while attempt < retries:
        try:
            return _fetch_content(url, text_limit)
        except WebDriverException as e:
            print(f"Attempt {attempt + 1} failed: {str(e)}")
            attempt += 1
            time.sleep(5)
    raise WebDriverException(f"Failed to fetch the content after {retries} attempts")

def _fetch_content(url, text_limit):
    # Setup Selenium WebDriver with extended timeout options and optimizations
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.set_page_load_timeout(60)  # Increase page load timeout

    # Fetch the page content
    driver.get(url)
    time.sleep(5)  # Increase sleep time to ensure the page loads completely
    page_source = driver.page_source
    driver.quit()  # Close the browser

    # Parse the page source with BeautifulSoup
    soup = BeautifulSoup(page_source, 'html.parser')
    
    # Extract title
    title = soup.title.string if soup.title else "No title"
    
    # Try to extract meta description
    meta_description = ""
    meta_tag = soup.find("meta", attrs={"name": "description"})
    if meta_tag:
        meta_description = meta_tag.get("content", "")
    
    # Try to extract the main article content
    article_text = ""
    
    # Attempt to find the main content using common tags/attributes
    article_tag = soup.find('article')
    if article_tag:
        article_text = article_tag.get_text(separator=' ', strip=True)
    else:
        # Fall back to searching for a main content div
        main_content_div = soup.find('div', class_="main-content")
        if main_content_div:
            article_text = main_content_div.get_text(separator=' ', strip=True)
        else:
            # Fall back to getting text from all paragraphs in the body, assuming no specific structure is found
            paragraphs = soup.find_all('p')
            article_text = " ".join(p.get_text(separator=' ', strip=True) for p in paragraphs)
    
    # Truncate the article text to the specified text_limit
    article_text = article_text[:text_limit].strip()

    return {
        "url": url,
        "title": title,
        "meta_description": meta_description,
        "text_content": article_text  # Return the main content text
    }
