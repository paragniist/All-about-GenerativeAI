# semantic_expansion_demo.py
# This script demonstrates synonym and semantic expansion using Word2Vec and BERT

# Import necessary libraries
from gensim.models import Word2Vec
from transformers import AutoTokenizer, AutoModel
import torch

# Sample technology-related terms for training Word2Vec model
sentences = [
    ["AI", "machine", "learning", "deep", "learning", "neural", "networks"],
    ["GPU", "graphics", "processing", "unit", "parallel", "processing"],
    ["LLM", "large", "language", "model", "NLP", "transformer"],
    ["data", "science", "big", "data", "analytics", "AI"],
    ["cloud", "computing", "infrastructure", "GPU", "AI", "ML"]
]

# *****************************************************************************************************************************************
# Step 1: Synonym Expansion with Word2Vec
# *****************************************************************************************************************************************
print("=== Synonym Expansion with Word2Vec ===")

# Train a Word2Vec model on the sample sentences
word2vec_model = Word2Vec(sentences, vector_size=50, min_count=1, workers=1)

# Define a query term and find synonyms
query_term = "AI"
print(f"Expanding synonyms for: {query_term}")
if query_term in word2vec_model.wv:
    synonyms = word2vec_model.wv.most_similar(query_term, topn=5)
    for synonym, score in synonyms:
        print(f"{synonym} (similarity score: {score})")
else:
    print(f"{query_term} not found in vocabulary.")
# *****************************************************************************************************************************************

# *****************************************************************************************************************************************
# Step 2: Semantic Expansion with BERT
# *****************************************************************************************************************************************
print("\n=== Semantic Expansion with BERT ===")

# Load pre-trained BERT model and tokenizer
tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")
model = AutoModel.from_pretrained("bert-base-uncased")

# Define a query sentence for semantic expansion
query_sentence = "Advances in large language models"
inputs = tokenizer(query_sentence, return_tensors="pt")

# Generate embeddings for the query sentence
with torch.no_grad():
    embeddings = model(**inputs).last_hidden_state.mean(dim=1)

# Compare embeddings to identify semantically similar terms (simulated)
# Note: In practice, you would use a database or pre-computed embeddings for this step
# Here we just demonstrate embedding generation
print("Generated embedding for semantic expansion. Use these embeddings to search for related terms.")

# Example output
print(f"Embedding shape: {embeddings.shape}")
# *****************************************************************************************************************************************