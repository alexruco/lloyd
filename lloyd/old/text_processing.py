# text_processing.py

import re
import ssl
import nltk
from nltk.corpus import stopwords

# Bypass SSL verification for NLTK downloads
ssl._create_default_https_context = ssl._create_unverified_context

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
