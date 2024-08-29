import requests
from bs4 import BeautifulSoup
import re
import time

def get_search_results_count(query):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    # Format the query to replace spaces with '+'
    formatted_query = query.replace(' ', '+')
    
    # Google search URL
    url = f'https://www.google.com/search?q={formatted_query}'
    
    # Send GET request to Google
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find the element that contains the result stats
        result_stats = soup.find('div', id='result-stats')
        
        if result_stats:
            # Extract the text and parse the number of results
            results_text = result_stats.get_text()
            print(f"Raw result stats text: {results_text}")  # Debugging line
            
            # Use a regular expression to extract numbers (remove any non-numeric characters)
            results_number = re.findall(r'\d+', results_text.replace(',', ''))
            
            if results_number:
                return int(''.join(results_number))
            else:
                print("Could not parse the number of results from the text.")
                return None
        else:
            print("Could not find result stats on the page.")
            return None
    else:
        print(f"Request failed with status code {response.status_code}.")
        return None

# Example usage
if __name__ == "__main__":
    query = "Python programming"
    results_count = get_search_results_count(query)
    
    if results_count:
        print(f"Estimated number of results for '{query}': {results_count}")
    else:
        print("Could not estimate the number of results.")
    
    # Be polite and delay before making another request
    time.sleep(2)
