import pandas as pd
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

class Retriever:
    def __init__(self, data_path):
        self.data = pd.read_csv(data_path)
        self.model = SentenceTransformer('paraphrase-MiniLM-L6-v2')
        self.evidence_embeddings = self.model.encode(self.data['evidence'].tolist())

    def retrieve(self, claim, top_k=3):
        claim_embedding = self.model.encode([claim])
        similarities = cosine_similarity(claim_embedding, self.evidence_embeddings)[0]
        top_indices = similarities.argsort()[-top_k:][::-1]
        return self.data.iloc[top_indices]
    
if __name__ == "__main__":
    retriever = Retriever('./sample_evidence.csv')
    claim = "The earth is flat!"
    results = retriever.retrieve(claim)
    print(f"Top 3 pieces of evidence for the claim '{claim}'")
    print(results[['evidence', 'label']])