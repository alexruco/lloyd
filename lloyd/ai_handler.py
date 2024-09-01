# ai_handler.py

from kate import AIInterface, get_response
ai_interface = AIInterface(config_path="/Users/aimaggie.com/projects/aimaggie.com/config.json")

def classify_page_with_ai(url, title, meta_description, text_content):
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

def extract_keywords_with_ai(content, model_name="llama3"):
    prompt = (
        f"Analyze the following content and extract the most relevant keywords. "
        f"Return only the keywords in a comma-separated list, with no introduction or additional text.\n\n"
        f"Content:\n{content}\n\n"
        f"Keywords:"
    )
    keywords = get_response(prompt, model_name)
    return keywords.split(', ')  # Assuming the AI returns a comma-separated list
