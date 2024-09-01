# main.py

from fetch_content import fetch_content_from_url
from datetime import datetime, timezone
from bing_organic_results_selenium import get_search_result_urls
from ai_handler import classify_page_with_ai, extract_keywords_with_ai


search_term = "automated testing tools"
max_position = 10
urls = get_search_result_urls(search_term)  # Get URLs from Bing search results

results = {}
for position, url in enumerate(urls, start=1):
    if position > max_position:
        break
    
    fetched_data = fetch_content_from_url(url)  # Fetch content for each URL
    enhanced_summary = classify_page_with_ai(url, fetched_data['title'], fetched_data['meta_description'], fetched_data['text_content'])
    
    results[url] = {
        "search_term": search_term,
        "position": position,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "title": fetched_data['title'],
        "meta_description": fetched_data['meta_description'],
        "text_content": fetched_data['text_content'],  # Store the fetched text content
        "summary": enhanced_summary  # Store the enhanced summary
    }

# Output the result
for url, data in results.items():
    print(f"URL: {url}")
    print(f"Position: {data['position']}")
    print(f"Title: {data['title']}")
    print(f"Meta Description: {data['meta_description']}")
    print(f"Text Content: {data['text_content']}")
    print(f"Summary: {data['summary']}")
    keywords = extract_keywords_with_ai(data['text_content'])
    print(f"Keywords: {', '.join(keywords)}")
    print("-" * 40)
