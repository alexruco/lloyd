# topic_modeling.py

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import LatentDirichletAllocation as LDA
from nltk.stem import WordNetLemmatizer
import nltk

nltk.download('wordnet')
nltk.download('omw-1.4')

def lemmatize_text(text):
    lemmatizer = WordNetLemmatizer()
    return ' '.join([lemmatizer.lemmatize(word) for word in text.split()])

def perform_topic_clustering(texts, num_topics=5):
    lemmatized_texts = [lemmatize_text(text) for text in texts]
    
    vectorizer = TfidfVectorizer(min_df=1, stop_words='english', ngram_range=(1, 2))
    tfidf_matrix = vectorizer.fit_transform(lemmatized_texts)
    
    lda = LDA(n_components=num_topics, random_state=0)
    lda.fit(tfidf_matrix)
    
    feature_names = vectorizer.get_feature_names_out()
    topics = {}
    
    for idx, topic in enumerate(lda.components_):
        topics[idx] = [feature_names[i] for i in topic.argsort()[:-11:-1]]
    
    return topics
