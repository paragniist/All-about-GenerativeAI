############################################################################################################
# Step 1 - Import the Required Libraries
############################################################################################################
import json
import torch
from transformers import pipeline
from sentence_transformers import SentenceTransformer, util
############################################################################################################

############################################################################################################
# Step 2 - Load the JSON knowledge base 
############################################################################################################
with open('knowledge_base.json', 'r') as file:
    knowledge_base = json.load(file)
############################################################################################################

############################################################################################################
# Step 3 - Initialize the language-agnostic embeddings model
model = SentenceTransformer('sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2')
############################################################################################################

############################################################################################################
# Step 4 - Prepare the Embeddings for the Knowledge Base
############################################################################################################
questions = [entry['question'] for entry in knowledge_base['questions']]
question_embeddings = model.encode(questions, convert_to_tensor=True)
############################################################################################################

############################################################################################################
# Step 5 - Initialize the Translation Pipeline
############################################################################################################
translator = pipeline('translation_en_to_es', model='Helsinki-NLP/opus-mt-en-es')
############################################################################################################

############################################################################################################
# Step 6 - Define the Function to Find the Best Answer
############################################################################################################
def find_best_answer(user_input):
    # Encode the user input query
    user_input_embedding = model.encode(user_input, convert_to_tensor=True)

    # Compute the cosine similarities
    similarities = util.pytorch_cos_sim(user_input_embedding, question_embeddings)

    # Find the index of the best match
    best_match_index = torch.argmax(similarities).item()

    # Retrieve the best answer
    best_answer = knowledge_base['questions'][best_match_index]['answer']

    return best_answer
############################################################################################################

############################################################################################################
# Step 7 - Define the Function to Translate Text into Spanish
############################################################################################################
def translate_to_spanish(text):
    translation = translator(text, max_length=100)[0]['translation_text']
    return translation
############################################################################################################

############################################################################################################
# Step 8 - Application Loopo for User Interaction
############################################################################################################
while True:
    # Ask for user input
    user_input = input("Please enter your query: ")

    if user_input.lower() == 'exit':
        break

    # Find the best answer
    best_answer = find_best_answer(user_input)

    # Translate the answer to Spanish
    translated_answer = translate_to_spanish(best_answer)

    # Display the answers in English and Spanish
    print(f"Answer in English: {best_answer}")
    print(f"Answer in Spanish: {translated_answer}")
############################################################################################################