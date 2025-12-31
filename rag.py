import json
import numpy as np
from sentence_transformers import SentenceTransformer
from numpy.linalg import norm



embedder = SentenceTransformer("all-MiniLM-L6-v2")

with open("Q_and_A.json", "r", encoding="utf-8") as f:
    RAW_DATA = json.load(f)

QNA_DATA = []

# Case 1: Dictionary {question: answer}
if isinstance(RAW_DATA, dict):
    for q, a in RAW_DATA.items():
        QNA_DATA.append({
            "question": q,
            "answer": a
        })

# Case 2: List of objects [{"question": "...", "answer": "..."}]
elif isinstance(RAW_DATA, list):
    for item in RAW_DATA:
        if isinstance(item, dict) and "question" in item and "answer" in item:
            QNA_DATA.append(item)

# Safety check
if not QNA_DATA:
    raise ValueError("qnada.json format not supported")

QUESTIONS = [item["question"] for item in QNA_DATA]
QUESTION_EMBEDDINGS = embedder.encode(QUESTIONS)


def cosine_similarity(a, b):
    return np.dot(a, b) / (norm(a) * norm(b))


def retrieve_context(user_query, top_k=2):
    query_embedding = embedder.encode([user_query])[0]

    scores = []
    for idx, q_emb in enumerate(QUESTION_EMBEDDINGS):
        score = cosine_similarity(query_embedding, q_emb)
        scores.append((score, idx))

    scores.sort(reverse=True)
    top_matches = scores[:top_k]

    contexts = []
    for _, idx in top_matches:
        q = QNA_DATA[idx]["question"]
        a = QNA_DATA[idx]["answer"]
        contexts.append(f"Q: {q}\nA: {a}")

    return "\n\n".join(contexts)
