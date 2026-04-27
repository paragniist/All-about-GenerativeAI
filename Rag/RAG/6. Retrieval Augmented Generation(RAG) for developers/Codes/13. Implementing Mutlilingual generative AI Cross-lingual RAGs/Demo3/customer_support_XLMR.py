######################################################################################################################################
# Step 1 - Importing Necessary Libraries
######################################################################################################################################
import json
from transformers import AutoTokenizer, AutoModel, pipeline, T5ForConditionalGeneration, T5Tokenizer
from googlesearch import search
import torch
import requests
from bs4 import BeautifulSoup
from sklearn.metrics.pairwise import cosine_similarity
import wikipediaapi
import warnings
import logging
from transformers import logging as transformers_logging
######################################################################################################################################

######################################################################################################################################
# Step 2 - Suppressing Warnings and set up logging
######################################################################################################################################
# Suppress warnings related to special tokens
warnings.filterwarnings("ignore", message="Special tokens have been added in the vocabulary, make sure the associated word embeddings are fine-tuned or trained.")

# Set Hugging Face Transformers logging to error level to suppress this specific warning
transformers_logging.set_verbosity_error()
######################################################################################################################################

######################################################################################################################################
# Step 3 - Loading the Knowledge Base
######################################################################################################################################
# Load the knowledge base
with open('knowledge_base.json', 'r') as file:
    knowledge_base = json.load(file)
######################################################################################################################################

######################################################################################################################################
# Step 4 - Initialize Models and APIs
######################################################################################################################################
# Initialize the Wikipedia API
wiki = wikipediaapi.Wikipedia(language='en', user_agent="CustomerSupportRAG/1.0 (example@example.com)")

# Initialize the XLM-R model and tokenizer for language-agnostic embeddings
xlmr_tokenizer = AutoTokenizer.from_pretrained("xlm-roberta-base")
xlmr_model = AutoModel.from_pretrained("xlm-roberta-base")

# Initialize the T5 model and tokenizer for response generation
special_tokens = ['<s>', '</s>', '<pad>']
t5_tokenizer = T5Tokenizer.from_pretrained("t5-small", legacy=True)
t5_tokenizer.add_special_tokens({'additional_special_tokens': special_tokens})
t5_model = T5ForConditionalGeneration.from_pretrained("t5-small")
t5_model.resize_token_embeddings(len(t5_tokenizer))
######################################################################################################################################

######################################################################################################################################
# Step 5 - Create teh Translation Pipeline
######################################################################################################################################
# Create translation pipelines
translator_to_english = pipeline("translation", model="Helsinki-NLP/opus-mt-mul-en")
translator_from_english = {
    "es": pipeline("translation", model="Helsinki-NLP/opus-mt-en-es"),
    "fr": pipeline("translation", model="Helsinki-NLP/opus-mt-en-fr"),
    "zh": pipeline("translation", model="Helsinki-NLP/opus-mt-en-zh"),
}
######################################################################################################################################

######################################################################################################################################
# Step 6 - Helper Function for embedding and context retrieval
######################################################################################################################################
# Helper function to generate embeddings using XLM-R
def generate_embeddings(text):
    inputs = xlmr_tokenizer(text, return_tensors="pt", padding=True, truncation=True)
    with torch.no_grad():
        outputs = xlmr_model(**inputs)
    return outputs.last_hidden_state.mean(dim=1)  # Mean pooling for a fixed-size vector

# Function to retrieve the most relevant context using cosine similarity
def retrieve_most_relevant_context(question, contexts):
    question_embedding = generate_embeddings(question)
    context_embeddings = [generate_embeddings(context) for context in contexts]
    
    # Calculate cosine similarity between the question and each context
    similarities = [cosine_similarity(question_embedding, context_embedding)[0][0] for context_embedding in context_embeddings]
    
    # Find the context with the highest similarity
    most_relevant_index = similarities.index(max(similarities))
    return contexts[most_relevant_index]
######################################################################################################################################

######################################################################################################################################
# Step 7 - Knowledge Base, Wikipedia, and Web Search Functions
######################################################################################################################################
# Helper function to find an answer in the knowledge base
def find_answer_in_knowledge_base(question):
    for faq in knowledge_base["FAQs"]:
        if faq["question"].lower() in question.lower():
            return faq["answer"]
    return None

# Wikipedia retrieval function
def get_wikipedia_content(query):
    page = wiki.page(query)
    if page.exists():
        return page.summary
    return None

# Search engine retrieval function
def get_search_results(query):
    search_results = []
    for url in search(query, num_results=3):
        search_results.append(get_page_content(url))
    return ' '.join(search_results)

# Function to get content from a URL
def get_page_content(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        return ' '.join([p.text for p in soup.find_all('p')])
    except:
        return ''
######################################################################################################################################

######################################################################################################################################
# Step 8 - Retrieve Contextual Information
######################################################################################################################################
# Retrieve contextual information from Wikipedia first, then web search
def retrieve_information(query):
    # First attempt to retrieve content from Wikipedia
    wikipedia_content = get_wikipedia_content(query)
    if wikipedia_content:
        return wikipedia_content
    
    # If no Wikipedia content is found, search the web
    search_content = get_search_results(query)
    return search_content if search_content else "No relevant information found."
######################################################################################################################################

######################################################################################################################################
# Step 9 - Generate Responses
######################################################################################################################################
# Generate a response using the T5 model
def generate_response(question, context):
    input_text = f"question: {question} context: {context}"
    inputs = t5_tokenizer.encode(input_text, return_tensors="pt", max_length=512, truncation=True)
    
    outputs = t5_model.generate(
        inputs, 
        max_length=512, 
        num_beams=5, 
        early_stopping=True
    )
    return t5_tokenizer.decode(outputs[0], skip_special_tokens=True)
######################################################################################################################################

######################################################################################################################################
# Step 10 - Main Customer Support Response Handling
######################################################################################################################################
# Main function to handle customer support responses
def get_customer_support_response(question, input_language, output_language):
    # Translate the question to English if necessary
    if input_language != "en":
        translated_question = translator_to_english(question)[0]['translation_text']
    else:
        translated_question = question
    
    # Search the knowledge base first
    knowledge_base_answer = find_answer_in_knowledge_base(translated_question)
    
    if knowledge_base_answer:
        context_aware_response = knowledge_base_answer
    else:
        # Retrieve context from Wikipedia or the web if no knowledge base answer is found
        retrieved_context = retrieve_information(translated_question)
        
        # Generate a response using T5 with the retrieved context
        context_aware_response = generate_response(translated_question, retrieved_context)
    
    # If the output language is not English, translate the response back
    if output_language != "en":
        final_response = translator_from_english[output_language](context_aware_response)[0]['translation_text']
    else:
        final_response = context_aware_response
    
    return final_response
######################################################################################################################################

######################################################################################################################################
# Step 11 - Main Loop for continuous user interaction
######################################################################################################################################
if __name__ == "__main__":
    while True:
        # Prompt for the user's question
        print("Please enter your question (type 'exit' to quit). You can ask in English, Spanish, Chinese, or French:")
        question = input("> ").strip()
        
        if question.lower() == "exit":
            print("Exiting the program.")
            break

        # Prompt for the language of the response
        print("In which language would you like the response? Enter 'en' for English, 'es' for Spanish, 'zh' for Chinese, or 'fr' for French:")
        output_language = input("> ").strip()

        # Determine the input language based on the first prompt
        if any(char in question for char in "áéíóúñ"):
            input_language = "es"
        elif any(char in question for char in "你好"):
            input_language = "zh"
        elif any(char in question for char in "éèàç"):
            input_language = "fr"
        else:
            input_language = "en"
        
        # Get the response
        response = get_customer_support_response(question, input_language, output_language)
        
        # Print the response
        print("Response:", response)
######################################################################################################################################
