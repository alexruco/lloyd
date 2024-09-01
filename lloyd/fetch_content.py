#fetch_content.py

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
from selenium.common.exceptions import WebDriverException

def fetch_content_from_url(url, text_limit=2000, retries=3, delay=10):
    attempt = 0
    while attempt < retries:
        try:
            print(f"Fetching content from URL: {url} (Attempt {attempt + 1})")
            return _fetch_content(url, text_limit)
        except WebDriverException as e:
            print(f"Attempt {attempt + 1} failed: {str(e)}")
            attempt += 1
            time.sleep(delay)
        except Exception as ex:
            print(f"Unexpected error during fetch: {str(ex)}")
            break
    print(f"Failed to fetch content from {url} after {retries} attempts. Skipping...")
    return None  # Return None instead of raising an exception

def _fetch_content(url, text_limit):
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.set_page_load_timeout(60)

    driver.get(url)
    time.sleep(5)
    page_source = driver.page_source
    driver.quit()

    soup = BeautifulSoup(page_source, 'html.parser')
    
    title = soup.title.string if soup.title else "No title"
    
    meta_description = ""
    meta_tag = soup.find("meta", attrs={"name": "description"})
    if meta_tag:
        meta_description = meta_tag.get("content", "")
    
    article_text = ""
    article_tag = soup.find('article')
    if article_tag:
        article_text = article_tag.get_text(separator=' ', strip=True)
    else:
        main_content_div = soup.find('div', class_="main-content")
        if main_content_div:
            article_text = main_content_div.get_text(separator=' ', strip=True)
        else:
            paragraphs = soup.find_all('p')
            article_text = " ".join(p.get_text(separator=' ', strip=True) for p in paragraphs)
    
    article_text = article_text[:text_limit].strip()

    return {
        "url": url,
        "title": title,
        "meta_description": meta_description,
        "text_content": article_text
    }