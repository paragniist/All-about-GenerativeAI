# Clip 1
import nltk
import torch

# Clip 1
import numpy as np
from colorama import Fore, init
from transformers import BertTokenizer, BertModel
from prettytable import PrettyTable
from sklearn.metrics.pairwise import cosine_similarity

# Clip 2
from sentence_transformers import SentenceTransformer

# Clip 3
from nltk.tokenize import word_tokenize
from rank_bm25 import BM25Okapi
from sentence_transformers import SentenceTransformer
from sklearn.metrics import precision_score, recall_score, ndcg_score

# Initialize colorama for colored output in the terminal
init(autoreset=True)
nltk.download('punkt')

# Define reusable functions
def get_bert_emb(text, tok, mdl):  # Clip 1
    """Retrieve BERT embeddings for a given text."""
    inp = tok(text, return_tensors='pt', truncation=True, padding=True, max_length=128)
    with torch.no_grad():
        return mdl(**inp).last_hidden_state.mean(dim=1).squeeze().cpu().numpy()

def calc_cos_sim(query_emb, corpus_embs):  # Clip 1 and 2
    """Compute cosine similarity between query and corpus embeddings."""
    return cosine_similarity(query_emb, corpus_embs).flatten()

def tokenize_corp(corp):  # Clip 3
    """Tokenize the corpus for BM25."""
    return [word_tokenize(doc.lower()) for doc in corp]

def calc_bm25_scores(corp, qry):  # Clip 3
    """Compute BM25 scores for the given query against the corpus."""
    bm25 = BM25Okapi(tokenize_corp(corp))
    tok_qry = word_tokenize(qry.lower())
    return np.array(bm25.get_scores(tok_qry)) / bm25.get_scores(tok_qry).max()

def eval_rank(y_true, y_scores):  # Clip 3
    """Evaluate ranking using precision, recall, and NDCG metrics."""
    y_pred_bin = (y_scores >= 0.5).astype(int)
    return precision_score(y_true, y_pred_bin), recall_score(y_true, y_pred_bin), ndcg_score([y_true], [y_scores])

# Clip 1: Introduction to Ranking Algorithms
def clip_1_basic_ranking(corp, qry):
    """Clip 1: Basic Ranking with BERT and cosine similarity."""
    print(Fore.YELLOW + "\n--- Clip 1: Basic Ranking with BERT ---\n")
    
    tok = BertTokenizer.from_pretrained('bert-base-uncased')
    mdl = BertModel.from_pretrained('bert-base-uncased')

    corp_embs = np.array([get_bert_emb(doc, tok, mdl) for doc in corp])
    qry_emb = get_bert_emb(qry, tok, mdl).reshape(1, -1)
    
    cos_sim = calc_cos_sim(qry_emb, corp_embs)
    
    tbl = PrettyTable(["Rank", "Document"])
    for rank, doc in enumerate([corp[i] for i in cos_sim.argsort()[::-1]], start=1):
        tbl.add_row([rank, doc])
    print(tbl)
    input("\nPress Enter to continue to Clip 2...")

# Clip 2: Advanced Scoring Mechanisms
def clip_2_advanced_scoring(corp, qry):
    """Clip 2: Explore advanced scoring mechanisms using Sentence Transformers."""
    print(Fore.YELLOW + "\n--- Clip 2: Advanced Scoring Mechanisms ---\n")
    
    mdl_st = SentenceTransformer('paraphrase-MiniLM-L6-v2')
    corp_embs_st = mdl_st.encode(corp, convert_to_tensor=True).cpu().numpy()
    qry_emb_st = mdl_st.encode([qry], convert_to_tensor=True).cpu().numpy()
    
    cos_sim_st = calc_cos_sim(qry_emb_st, corp_embs_st)
    
    tbl = PrettyTable(["Rank", "Document"])
    for rank, doc in enumerate([corp[i] for i in cos_sim_st.argsort()[::-1]], start=1):
        tbl.add_row([rank, doc])
    print(tbl)
    input("\nPress Enter to continue to Clip 3...")

# Clip 3: Implementation and Evaluation of Ranking Techniques
def clip_3_impl_eval(corp, qry):
    """Clip 3: Implement and evaluate ranking techniques using BM25 and BERT."""
    print(Fore.YELLOW + "\n--- Clip 3: Implementation and Evaluation of Ranking Techniques ---\n")
    
    bm25_scores = calc_bm25_scores(corp, qry)
    tok = BertTokenizer.from_pretrained('bert-base-uncased')
    mdl = BertModel.from_pretrained('bert-base-uncased')

    corp_embs = np.array([get_bert_emb(doc, tok, mdl) for doc in corp])
    qry_emb = get_bert_emb(qry, tok, mdl).reshape(1, -1)
    cos_sim = calc_cos_sim(qry_emb, corp_embs)

    ensemble_scores = (bm25_scores + cos_sim) / 2
    
    tbl = PrettyTable(["Rank", "Document"])
    for rank, doc in enumerate([corp[i] for i in ensemble_scores.argsort()[::-1]], start=1):
        tbl.add_row([rank, doc])
    print(tbl)
    
    precision, recall, ndcg = eval_rank(np.array([1, 0, 1, 1, 0, 0, 1, 1, 0]), ensemble_scores)
    print(f"Precision: {precision:.2f}\nRecall: {recall:.2f}\nNDCG: {ndcg:.2f}")
    input("\nPress Enter to continue to Clip 4...")

if __name__ == "__main__":
    corp = [
        "Shipment ID 1234 is scheduled for delivery on August 20th.",
        "Inventory update: Warehouse A has received 100 units of item X.",
        "Customer order 5678 includes items Y and Z, expected delivery on August 22nd.",
        "The new shipment from supplier B is expected to arrive on August 25th.",
        "Warehouse B has dispatched 50 units of item Y to customer C.",
        "Update: Shipment ID 7890 is delayed due to weather conditions.",
        "Inventory count for item Z in Warehouse A is at a critical low.",
        "Order 6789 includes items X and Z, scheduled for delivery on August 30th.",
        "Supplier A has confirmed the shipment of 200 units of item X."
    ]
    qry = "shipment delivery status"

    clip_1_basic_ranking(corp, qry)
    print("\n")
    clip_2_advanced_scoring(corp, qry)
    print("\n")
    clip_3_impl_eval(corp, qry)
    print("\n")