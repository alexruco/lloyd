# utils.py

import requests
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

ua = UserAgent()

def is_company_website(url):
    headers = {
        'User-Agent': ua.random
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

    combined_text = (title.lower() + meta_description.lower()).strip()

    company_indicators = [
        'inc', 'llc', 'corp', 'ltd', 'company', 'group', 'holdings', 
        'corporate', 'services', 'solutions', 'partners', 'clients'
    ]
    
    if any(indicator in combined_text for indicator in company_indicators):
        return True
    
    business_terms_count = sum(page_text.lower().count(term) for term in company_indicators)
    
    if business_terms_count > 5:
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
