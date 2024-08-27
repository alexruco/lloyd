import requests
from bs4 import BeautifulSoup
from collections import Counter
import re
import ssl
import nltk

# Bypass SSL verification if necessary
ssl._create_default_https_context = ssl._create_unverified_context

# Import necessary NLTK components
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# Ensure stopwords and punkt are downloaded
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('punkt_tab')

# Define the stopwords set
stop_words = set(stopwords.words('english'))

def filter_keywords(keywords):
    """
    Filter out stopwords and non-alphabetic tokens from the keywords list.
    """
    tokens = word_tokenize(" ".join([word for word, _ in keywords]))
    filtered_keywords = [word for word in tokens if word.lower() not in stop_words and word.isalpha()]
    return filtered_keywords

def scrape_duckduckgo(query):
    """
    Scrape DuckDuckGo search results for a given query.
    """
    # Prepare the search URL
    search_url = f"https://html.duckduckgo.com/html?q={query}"
    
    # Headers to mimic a real browser request
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    
    # Send the GET request to DuckDuckGo with headers
    response = requests.get(search_url, headers=headers)
    
    # Check if the request was successful
    if response.status_code != 200:
        print(f"Failed to retrieve search results. Status code: {response.status_code}")
        return []
    
    # Parse the HTML content
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Find all the result links in the search results
    results = []
    for link in soup.find_all('a', class_='result__a', href=True):
        url = link['href']
        # Filter out DuckDuckGo internal URLs
        if "duckduckgo.com" not in url:
            results.append(url)
    
    return results

def extract_keywords_from_url(url):
    """
    Extract and count keywords from the content of the given URL.
    """
    # Headers to mimic a real browser request
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    
    # Send the GET request to the website
    try:
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            print(f"Failed to retrieve content from {url}. Status code: {response.status_code}")
            return []
    except requests.exceptions.RequestException as e:
        print(f"Error accessing {url}: {e}")
        return []
    
    # Parse the HTML content
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Extract the text content from the website
    text = ' '.join(soup.stripped_strings)
    
    # Use a regex to extract words and count their occurrences
    words = re.findall(r'\b\w+\b', text.lower())
    word_counts = Counter(words)
    
    # Identify the most common keywords
    keywords = word_counts.most_common(40)  # Top 10 most common words
    return keywords

def analyze_competitors_for_keyword(keyword):
    """
    Analyze top competitor websites for a given keyword to identify their top keywords.
    """
    # Step 1: Get a list of URLs from DuckDuckGo search
    urls = scrape_duckduckgo(keyword)
    
    if not urls:
        print("No search results found.")
        return
    
    # Step 2: Scrape each URL to extract keywords
    for url in urls:
        print(f"\nAnalyzing {url}")
        keywords = extract_keywords_from_url(url)
        filtered_keywords = filter_keywords(keywords)
        if filtered_keywords:
            print("Top Keywords:")
            for word in filtered_keywords:
                print(f"{word}")
        else:
            print("No keywords found or failed to retrieve content.")
    
# Example usage
if __name__ == "__main__":
    keyword = "automated testing tool"
    analyze_competitors_for_keyword(keyword)
