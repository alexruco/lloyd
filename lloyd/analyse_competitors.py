# main.py

import time
import random
from lloyd.old.scraper import scrape_duckduckgo, extract_text_from_url
from text_processing import filter_search_terms
from lloyd.old.topic_modeling import perform_topic_clustering
from utils import is_company_website
from bertha import crawl_website, indexible_pages


def analyze_single_website_for_topics(base_url, num_topics=3):
    """
    Analyzes a website and returns its topic clusters based on the content of all indexed pages.

    Parameters:
        base_url (str): The base URL of the website to analyze.
        num_topics (int): The number of topics to identify (default is 5).

    Returns:
        dict: A dictionary of topics, where keys are topic indices and values are lists of top words in each topic.
    """
    
    # Fetch all indexable pages for the base URL from the database
    pages = indexible_pages(base_url)  # Make sure the correct database path is provided
    #print(f"pages:{pages}")
    
    # Collect text content from all pages
    all_texts = []
    
    for page in pages:
        print(f"Analyzing page: {page}")
        text = extract_text_from_url(page)
        if text:
            all_texts.append(text)
        else:
            print(f"Failed to retrieve content from {page}")
    
    if all_texts:
        # Combine all the collected text into a single corpus
        combined_text = ' '.join(all_texts)
        
        # Perform topic clustering on the combined text
        topics = perform_topic_clustering([combined_text], num_topics=num_topics)
        print("\nIdentified Topics for the Website:")
        for idx, words in topics.items():
            print(f"Topic {idx + 1}: {', '.join(words)}")
        
        return topics
    else:
        print("No content to analyze.")
        return {}



def analyze_competitors_for_search_term(search_term, num_topics=5):
    """
    Analyzes the websites of competitors found for a given search term and returns topic clusters
    based on the content of all indexed pages from each competitor's site.

    Parameters:
        search_term (str): The search term to find competitors.
        num_topics (int): The number of topics to identify (default is 5).

    Returns:
        dict: A dictionary of topics, where keys are topic indices and values are lists of top words in each topic.
    """
    
    # Step 1: Scrape search results from DuckDuckGo for the given search term
    competitor_urls = scrape_duckduckgo(search_term)
    
    if not competitor_urls:
        print("No competitors found for the search term.")
        return
    
    all_texts = []
    
    # Step 2: Crawl and analyze each competitor's website
    for competitor_url in competitor_urls:
        print(f"\nCrawling and analyzing website: {competitor_url}")
        
        # Step 2a: Use bertha to crawl the website
        crawl_website(competitor_url)  # Assuming bertha has a function `crawl_website`
        
        # Step 2b: Retrieve all indexable pages for the competitor's site
        pages = indexible_pages("db_websites.db", competitor_url)
        print(f"Found {len(pages)} pages for {competitor_url}")
        
        # Step 2c: Collect text content from all pages
        for page in pages:
            print(f"Analyzing page: {page}")
            text = extract_text_from_url(page)
            if text:
                all_texts.append(text)
            else:
                print(f"Failed to retrieve content from {page}")
    
    if all_texts:
        # Step 3: Combine all the collected text into a single corpus
        combined_text = ' '.join(all_texts)
        
        # Step 4: Perform topic clustering on the combined text
        topics = perform_topic_clustering([combined_text], num_topics=num_topics)
        print("\nIdentified Topics Across Competitors:")
        for idx, words in topics.items():
            print(f"Topic {idx + 1}: {', '.join(words)}")
        
        return topics
    else:
        print("No content to analyze across competitors.")
        return {}

# Example usage
if __name__ == "__main__":
    # Analyze the competitors for a given search term
    search_term = "automated testing tool"
    analyze_competitors_for_search_term(search_term, num_topics=5)
