import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin

def get_page_info(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract the page title
        title = soup.title.string if soup.title else 'No title found'

        # Extract the meta description
        meta_desc_tag = soup.find('meta', attrs={'name': 'description'})
        meta_description = meta_desc_tag['content'] if meta_desc_tag else 'No description found'

        # Extract text content from the homepage
        page_text = ' '.join(soup.stripped_strings)

        return {
            'title': title,
            'meta_description': meta_description,
            'page_text': page_text
        }

    except requests.exceptions.RequestException as e:
        print(f"Error accessing {url}: {e}")
        return None

def is_company_website(url):
    page_info = get_page_info(url)
    if not page_info:
        return False
    
    title = page_info['title']
    meta_description = page_info['meta_description']
    page_text = page_info['page_text']

    # Define stricter indicators of a company website
    company_indicators = ['inc', 'llc', 'corp', 'ltd', 'company', 'group', 'holdings', 'corporate', 'services', 'solutions', 'partners', 'clients']
    
    # Check if these indicators appear in title, meta description, or significant presence in page text
    if any(indicator in title.lower() + meta_description.lower() for indicator in company_indicators):
        return True
    
    # Count occurrences of business-related terms in the page text
    business_terms_count = sum(page_text.lower().count(term) for term in company_indicators)
    
    # Consider it a company if the text has multiple mentions of business-related terms
    if business_terms_count > 5:  # Threshold can be adjusted based on testing
        return True
    
    # Exclude certain domains known not to be company websites
    non_business_domains = ['.edu', '.org', '.gov', '.blog']
    parsed_url = urlparse(url)
    if any(parsed_url.netloc.endswith(domain) for domain in non_business_domains):
        return False

    # Exclude known non-business websites
    known_non_business_sites = [
        'geeksforgeeks.org', 'wikipedia.org', 'stackoverflow.com', 'github.com', 
        'medium.com', 'reddit.com', 'nytimes.com', 'bbc.co.uk', 'cnn.com', 'theguardian.com',
        'archive.org', 'coursera.org', 'edx.org', 'khanacademy.org', 'quora.com', 'udemy.com',
        'nytimes.com', 'bloomberg.com', 'dev.to', 'mozilla.org', 'developer.android.com', 
        'docs.python.org', 'mdn.mozilla.org'
    ]
    if any(site in url for site in known_non_business_sites):
        return False
    
    return False  # Default to non-company if none of the checks pass

# Example usage:
url = "https://testsigma.com/"
if is_company_website(url):
    print(f"{url} is likely a company website.")
else:
    print(f"{url} does not appear to be a company website.")
