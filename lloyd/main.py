# main.py

from kate import AIInterface, get_response
from bing_organic_results_selenium import search_and_fetch_content
from datetime import datetime, timezone  # Import timezone for timezone-aware datetime objects

ai_interface = AIInterface(config_path="/Users/aimaggie.com/projects/aimaggie.com/config.json")

def enhance_page_content(url, title, meta_description):
    # Example of additional processing: creating a summary
    
    prompt = f"Please return COMPETITOR if the following website is a company page, and INFORMATION if it is a blog, or information portal or other:  {url}\nTitle: {title}\nDescription: {meta_description}"
    
    enhanced_content = get_response(prompt, "llama3")
    
    return enhanced_content

search_term = "automated testing tools"
max_position = 10
fetched_results = search_and_fetch_content(search_term, max_position)    
print(f"Fetched Results: {fetched_results}")  # Debug print

# Output the result
results = {}
for url, data in fetched_results.items():
    print(f"Processing URL: {url}")  # Debug print
    enhanced_summary = enhance_page_content(url, data['title'], data['meta_description'])
    print(f"Enhanced Summary: {enhanced_summary}")  # Debug print

    results[url] = {
        "search_term": search_term,
        "position": data["position"],
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "title": data["title"],
        "meta_description": data["meta_description"],
        "summary": enhanced_summary  # Store the enhanced summary
    }
    
if results:  # Ensure results is not empty
    for url, data in results.items():
        print(f"URL: {url}")
        print(f"Position: {data['position']}")
        print(f"Title: {data['title']}")
        print(f"Meta Description: {data['meta_description']}")
        print(f"Summary: {data['summary']}")
        print("-" * 40)
else:
    print("No results to display.")
