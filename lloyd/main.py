# main.py

from kate import AIInterface, get_response
from fetch_content import fetch_content_from_url
from datetime import datetime, timezone
from bing_organic_results_selenium import get_search_result_urls

ai_interface = AIInterface(config_path="/Users/aimaggie.com/projects/aimaggie.com/config.json")

def enhance_page_content(url, title, meta_description, text_content):
    # Example of additional processing: creating a summary
    
    prompt = (
        f"Classify the website described below as either 'PLAYER' or 'INFLUENCER' based on the following criteria:\n\n"
        f"Respond with 'PLAYER' if the website is an organization that primarily offers products or services directly to customers. "
        f"This includes businesses, companies, or any commercial entities whose main purpose is selling, promoting, or providing their own products or services, "
        f"even if they provide some informational content.\n\n"
        f"Respond with 'INFLUENCER' if the website primarily provides independent information, comparisons, reviews, or guidance about products or services available on the market, "
        f"without directly selling or offering their own products or services. This includes blogs, review sites, or educational resources that aim to inform or influence purchasing decisions.\n\n"
        f"Ignore any incomplete or irrelevant content such as security checks, errors, or unrelated advertisements when making your classification.\n\n"
        f"Consider the following details:\n"
        f"URL: {url}\n"
        f"Title: {title}\n"
        f"Meta Description: {meta_description}\n"
        f"Page Content Summary: {text_content}\n\n"
        f"Please respond with either 'PLAYER' or 'INFLUENCER' and nothing else."
    )


    
    enhanced_content = get_response(prompt, "llama3")
    
    return enhanced_content

search_term = "automated testing tools"
max_position = 10
urls = get_search_result_urls(search_term)  # Get URLs from Bing search results

results = {}
for position, url in enumerate(urls, start=1):
    if position > max_position:
        break
    
    fetched_data = fetch_content_from_url(url)  # Fetch content for each URL
    enhanced_summary = enhance_page_content(url, fetched_data['title'], fetched_data['meta_description'], fetched_data['text_content'])
    
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
    print("-" * 40)
