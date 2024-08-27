# analyze_competitors_for_search_term.py

import requests
from bs4 import BeautifulSoup
from collections import Counter
import re
import ssl
import certifi
import nltk
from urllib.parse import urlparse
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import LatentDirichletAllocation as LDA

ssl._create_default_https_context = ssl._create_unverified_context

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# Ensure stopwords are downloaded
nltk.download('stopwords')
nltk.download('punkt')

stop_words = set(stopwords.words('english'))

def filter_search_terms(search_terms):
    filtered_terms = [
        " ".join([word for word in phrase.split() if word.lower() not in stop_words and word.isalpha()])
        for phrase in search_terms
    ]
    filtered_terms = [term for term in filtered_terms if term]
    return filtered_terms

def scrape_duckduckgo(query):
    search_url = f"https://html.duckduckgo.com/html?q={query}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
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
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
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
    text = ' '.join(soup.stripped_strings)
    return text

def is_company_website(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }

    try:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')

        title = soup.title.string if soup.title else ""
        meta_description_tag = soup.find('meta', attrs={'name': 'description'})
        meta_description = meta_description_tag['content'] if meta_description_tag else ""
        page_text = ' '.join(soup.stripped_strings)

    except requests.exceptions.RequestException:
        return False

    company_indicators = ['inc', 'llc', 'corp', 'ltd', 'company', 'group', 'holdings', 'corporate', 'services', 'solutions', 'partners', 'clients']
    
    if any(indicator in title.lower() + meta_description.lower() for indicator in company_indicators):
        return True
    
    business_terms_count = sum(page_text.lower().count(term) for term in company_indicators)
    
    if business_terms_count > 5:  # Threshold can be adjusted based on testing
        return True
    
    non_business_domains = ['.edu', '.org', '.gov', '.blog', '.net']
    parsed_url = urlparse(url)
    if any(parsed_url.netloc.endswith(domain) for domain in non_business_domains):
        return False

    known_non_business_sites = [
        'geeksforgeeks.org', 'wikipedia.org', 'stackoverflow.com', 'github.com', 
        'medium.com', 'reddit.com', 'nytimes.com', 'bbc.co.uk', 'cnn.com', 'theguardian.com',
        'archive.org', 'coursera.org', 'edx.org', 'khanacademy.org', 'quora.com', 'udemy.com',
        'nytimes.com', 'bloomberg.com', 'dev.to', 'mozilla.org', 'developer.android.com', 
        'docs.python.org', 'mdn.mozilla.org'
    ]
    if any(site in url for site in known_non_business_sites):
        return False
    
    return True

def perform_topic_clustering(texts, num_topics=5):
    # Vectorize the text using TF-IDF
    vectorizer = TfidfVectorizer(max_df=0.95, min_df=2, stop_words='english')
    tfidf_matrix = vectorizer.fit_transform(texts)
    
    # Apply LDA for topic modeling
    lda = LDA(n_components=num_topics, random_state=0)
    lda.fit(tfidf_matrix)
    
    feature_names = vectorizer.get_feature_names_out()
    topics = {}
    
    for idx, topic in enumerate(lda.components_):
        topics[idx] = [feature_names[i] for i in topic.argsort()[:-11:-1]]
    
    return topics

def analyze_competitors_for_search_term(search_term):
    urls = scrape_duckduckgo(search_term)
    
    if not urls:
        print("No search results found.")
        return
    
    all_texts = []  # To store the text of all competitor sites
    
    for url in urls:
        if is_company_website(url):
            print(f"\nAnalyzing {url}")
            text = extract_text_from_url(url)
            if text:
                all_texts.append(text)
            else:
                print("Failed to retrieve content.")
        else:
            print(f"\nSkipping non-company website: {url}")
    
    if all_texts:
        topics = perform_topic_clustering(all_texts)
        print("\nIdentified Topics Across Competitors:")
        for idx, words in topics.items():
            print(f"Topic {idx + 1}: {', '.join(words)}")
    else:
        print("No text data to analyze.")

# Example usage
if __name__ == "__main__":
    search_term = "automated testing tool"
    analyze_competitors_for_search_term(search_term)
