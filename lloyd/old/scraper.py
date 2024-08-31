# scraper.py

import random
import requests
from bs4 import BeautifulSoup

# List of common User-Agent strings
user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/91.0.864.64',
    'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0',
]

def scrape_duckduckgo(query):
    search_url = f"https://html.duckduckgo.com/html?q={query}"
    headers = {
        'User-Agent': random.choice(user_agents)
    }
    
    response = requests.get(search_url, headers=headers)
    
    if response.status_code != 200:
        print(f"Failed to retrieve search results. Status code: {response.status_code}")
        return []
    
    soup = BeautifulSoup(response.text, 'html.parser')
    results = []
    for link in soup.find_all('a', class_='result__a', href=True):
        url = link['href']
        results.append(url)
    
    return results

def extract_text_from_url(url):
    headers = {
        'User-Agent': random.choice(user_agents)
    }
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            print(f"Failed to retrieve content from {url}. Status code: {response.status_code}")
            return ""
    except requests.exceptions.RequestException as e:
        print(f"Error accessing {url}: {e}")
        return ""
    
    soup = BeautifulSoup(response.text, 'html.parser')
    text = ' '.join([p.get_text() for p in soup.find_all('p')])
    return text
