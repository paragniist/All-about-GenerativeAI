# demo3_pseudo_relevance_feedback_demo.py
# This script demonstrates pseudo-relevance feedback with query re-weighting and evaluation

# Import necessary libraries
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Sample data for demonstration: documents related to AI and ML technologies
documents = [
    "AI and machine learning are transforming industries",
    "The impact of deep learning on neural networks",
    "Large language models such as GPT and BERT",
    "GPU acceleration enhances deep learning performance",
    "Machine learning applications in healthcare and finance"
]
# *****************************************************************************************************************************************
# Step 1: Define the Initial Query
# *****************************************************************************************************************************************
query = "advancements in AI and machine learning"
# *****************************************************************************************************************************************

# *****************************************************************************************************************************************
# Step 2: Vectorize Query and Documents Using TF-IDF
# Use 'english' stop words directly in TfidfVectorizer
# *****************************************************************************************************************************************
vectorizer = TfidfVectorizer(stop_words='english')
all_texts = [query] + documents  # Include query for initial similarity check
tfidf_matrix = vectorizer.fit_transform(all_texts)

# *****************************************************************************************************************************************
# Step 3: Compute Initial Cosine Similarity
# *****************************************************************************************************************************************
query_vector = tfidf_matrix[0]  # Vectorized query
doc_vectors = tfidf_matrix[1:]   # Vectorized documents
initial_similarities = cosine_similarity(query_vector, doc_vectors).flatten()

# Display initial retrieval results
print("=== Initial Retrieval Results ===")
top_indices = initial_similarities.argsort()[::-1][:3]
top_docs = [documents[i] for i in top_indices]
for i, doc in enumerate(top_docs):
    print(f"Rank {i+1}: {doc} (Score: {initial_similarities[top_indices[i]]})")
# *****************************************************************************************************************************************

# *****************************************************************************************************************************************
# Step 4: Implement Pseudo-Relevance Feedback
# Select top documents as relevant and extract significant terms
# *****************************************************************************************************************************************
feedback_terms = []
for doc in top_docs:
    tokens = doc.lower().split()  # Simple tokenization using split()
    filtered_tokens = [word for word in tokens if word not in vectorizer.get_stop_words()]
    feedback_terms.extend(filtered_tokens)

# Reweight query with feedback terms by updating the query text
expanded_query = query + " " + " ".join(feedback_terms)
print("\nExpanded Query:", expanded_query)
# *****************************************************************************************************************************************

# *****************************************************************************************************************************************
# Step 5: Re-vectorize with Expanded Query and Re-evaluate
# Re-calculate similarities with expanded query
# *****************************************************************************************************************************************
all_texts_updated = [expanded_query] + documents
tfidf_matrix_updated = vectorizer.fit_transform(all_texts_updated)
query_vector_updated = tfidf_matrix_updated[0]
doc_vectors_updated = tfidf_matrix_updated[1:]
updated_similarities = cosine_similarity(query_vector_updated, doc_vectors_updated).flatten()

# Display re-evaluated retrieval results
print("\n=== Re-evaluated Retrieval Results ===")
top_indices_updated = updated_similarities.argsort()[::-1][:3]
top_docs_updated = [documents[i] for i in top_indices_updated]
for i, doc in enumerate(top_docs_updated):
    print(f"Rank {i+1}: {doc} (Score: {updated_similarities[top_indices_updated[i]]})")

# *****************************************************************************************************************************************
# Step 6: Evaluation - Compare Initial and Updated Retrieval
# *****************************************************************************************************************************************
initial_top_docs = set(top_docs)
updated_top_docs = set(top_docs_updated)
print("\n=== Evaluation Results ===")
print("Relevant documents found initially:", initial_top_docs)
print("Relevant documents found after feedback:", updated_top_docs)
print("Improved relevance and alignment with user intent through feedback.")
# *****************************************************************************************************************************************
