# bing_organic_results.py

import requests
from bs4 import BeautifulSoup
import time

def get_bing_organic_links(query, page=1):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.3'
    }
    
    # Format the query to replace spaces with '+'
    formatted_query = query.replace(' ', '+')
    
    # Calculate the `first` parameter value based on the page number
    start_index = (page - 1) * 10 + 1  # Page 1 -> first=1, Page 2 -> first=11, etc.
    
    # Bing search URL with pagination
    url = f'https://www.bing.com/search?q={formatted_query}&first={start_index}'
    
    # Print the URL for debugging
    print(f"Debug: Fetching page {page} with URL: {url}")
    
    # Send GET request to Bing
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        
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
    else:
        print(f"Request failed with status code {response.status_code}.")
        return None

def filter_bing_results(urls):
    ignore_patterns = [
        "go.microsoft.com/fwlink",
        "bing.com",
        "microsoft.com",
        "msn.com",
        "javascript:void(0);",
        "/search?q=",
        "/images/search?",
        "/videos/search?",
        "/maps?q=",
        "/news/search?q=",
        "/shop?q=",
        "/travel/search?q=",
        "/rewards/dashboard",
        "/homes?FORM=000060",
        "/bp/verify?FORM=000061",
        "/?FORM=Z9FD1",
        "#",
    ]
    
    filtered_urls = []
    for url in urls:
        if not any(pattern in url for pattern in ignore_patterns):
            filtered_urls.append(url)
    
    return filtered_urls

# Example usage
if __name__ == "__main__":
    query = "alex ruco"
    all_links = []
    
    for page in range(1, 6):  # Scrape first 5 pages
        links = get_bing_organic_links(query, page)
        
        if links:
            print(f"\nOrganic links for '{query}' on Bing (Page {page}):")
            for link in links:
                print(link)
            all_links.extend(links)
        else:
            print(f"Could not retrieve organic links for page {page}.")
        
        # Be polite and delay before making another request
        time.sleep(2)
    
    # Output all collected links
    print("\nAll collected links:")
    for link in all_links:
        print(link)
