from retriever import Retriever
from transformers import pipeline

class Verifier:
    def __init__(self, data_path):
        self.retriever = Retriever(data_path)
        self.entailment_model = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

    def verify(self, claim):
        evidence = self.retriever.retrieve(claim)
        entailment_scores = []

        for _, row in evidence.iterrows():
            result = self.entailment_model(row['evidence'], candidate_labels=["entailment", "contradiction", "neutral"], hypothesis=claim)
            entailment_scores.append(result['scores'][result['labels'].index("entailment")])
            avg_entailment_score = sum(entailment_scores) / len(entailment_scores)

        print(avg_entailment_score)
        if avg_entailment_score >= 0.4:
            return "TRUE", evidence
        elif avg_entailment_score < 0.4 and avg_entailment_score > 0.1:
            return "FALSE", evidence
        else:
            return "INCONCLUSIVE", evidence

if __name__ == "__main__":
    verifier = Verifier('./sample_evidence.csv')
    claim = "The earth is flat!"
    result, evidence = verifier.verify(claim)
    print(f"Claim: '{claim}'")
    print(f"Verification result: {result}")
    print("Supporting evidence:")
    print(evidence[['evidence', 'label']])