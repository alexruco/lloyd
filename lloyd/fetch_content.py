from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time

def fetch_content_from_url(url, text_limit=2000):
    # Setup Selenium WebDriver
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    # Fetch the page content
    driver.get(url)
    time.sleep(2)  # Let the page load completely
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
