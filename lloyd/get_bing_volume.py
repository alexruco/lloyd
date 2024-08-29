import requests
from bs4 import BeautifulSoup
import re
import time

def get_bing_search_results_count(query):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    formatted_query = query.replace(' ', '+')
    url = f'https://www.bing.com/search?q={formatted_query}'
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        
        result_stats = soup.find('span', class_='sb_count')
        
        if result_stats:
            results_text = result_stats.get_text()
            print(f"Raw result stats text: {results_text}")  # Debugging line
            
            results_number = re.findall(r'\d+', results_text.replace(',', ''))
            
            if results_number:
                return int(''.join(results_number))
            else:
                print("Could not parse the number of results from the text.")
                return None
        else:
            alt_result_stats = soup.find('div', class_='sb_count')
            if alt_result_stats:
                results_text = alt_result_stats.get_text()
                print(f"Alternative result stats text: {results_text}")  # Debugging line

                results_number = re.findall(r'\d+', results_text.replace(',', ''))
                
                if results_number:
                    return int(''.join(results_number))
                else:
                    print("Could not parse the number of results from the alternative text.")
                    return None
            else:
                print("Could not find result stats on the page.")
                return None
    else:
        print(f"Request failed with status code {response.status_code}.")
        return None

def filter_bing_results(urls):
    ignore_patterns = [
        "go.microsoft.com/fwlink",
        "bing.com",
        "microsoft.com",
        "msn.com"
    ]
    
    filtered_urls = []
    for url in urls:
        if not any(pattern in url for pattern in ignore_patterns):
            filtered_urls.append(url)
    
    return filtered_urls

def scrape_bing_results(query):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    formatted_query = query.replace(' ', '+')
    url = f'https://www.bing.com/search?q={formatted_query}'
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        results = []
        
        for link in soup.find_all('a', href=True):
            url = link['href']
            results.append(url)
        
        filtered_results = filter_bing_results(results)
        return filtered_results
    else:
        print(f"Request failed with status code {response.status_code}.")
        return []

# Example usage
if __name__ == "__main__":
    query = "Python programming"
    filtered_results = scrape_bing_results(query)
    
    if filtered_results:
        print(f"Filtered search results for '{query}':")
        for url in filtered_results:
            print(url)
    else:
        print("No valid search results found.")
    
    time.sleep(2)
