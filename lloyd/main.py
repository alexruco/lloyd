#main.py

import json
from collections import Counter
from fetch_content import fetch_content_from_url
from datetime import datetime, timezone
from bing_search_scraper import get_search_result_urls
from ai_handler import classify_page_with_ai, extract_keywords_with_ai

def main(target_url, search_term, max_position=10):
    # Step 1: Fetch URLs from the SERP based on the target keyword
    urls = get_search_result_urls(search_term)  #    Get URLs from Bing search results

    competitors = []
    influencers = []
    keyword_frequency = Counter()

    for position, url in enumerate(urls, start=1):
        if position > max_position:
            break
        
        fetched_data = fetch_content_from_url(url)  # Fetch content for each URL
        if fetched_data is None:
            continue  # Skip URLs that failed to fetch

        classification = classify_page_with_ai(url, fetched_data['title'], fetched_data['meta_description'], fetched_data['text_content'])
        
        # Step 2: Classify as either 'PLAYER' or 'INFLUENCER'
        if classification.strip() == "PLAYER":
            keywords = extract_keywords_with_ai(fetched_data['text_content'])
            competitors.append({
                "url": url,
                "title": fetched_data['title'],
                "meta_description": fetched_data['meta_description'],
                "keywords": keywords
            })
            keyword_frequency.update(keywords)  # Update keyword frequency for players
        elif classification.strip() == "INFLUENCER":
            influencers.append({
                "url": url,
                "title": fetched_data['title'],
                "meta_description": fetched_data['meta_description'],
            })

    # Step 3: Extract keywords from the content of the target URL
    target_data = fetch_content_from_url(target_url)
    if target_data is None:
        return json.dumps({"error": "Failed to fetch content from the target URL."}, indent=4)

    target_keywords = extract_keywords_with_ai(target_data['text_content'])

    # Step 4: Calculate the Keyword Gap with Frequencies
    keyword_gap = [
        {"keyword": keyword, "frequency": keyword_frequency[keyword]}
        for keyword in keyword_frequency if keyword not in target_keywords
    ]

    # Step 5: Prepare the final JSON output
    result = {
        "target_url": target_url,
        "search_term": search_term,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "competitors": competitors,
        "influencers": influencers,
        "keyword_gap": keyword_gap
    }

    # Ensure Latin characters are preserved
    return json.dumps(result, indent=4, ensure_ascii=False)

# Example usage
if __name__ == "__main__":
    target_url = "https://mysitefaster.com"
    search_term = "melhorar website"
    result_json = main(target_url, search_term)
    print(result_json)
