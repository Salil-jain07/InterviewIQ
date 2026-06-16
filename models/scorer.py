from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# Load model once
model = SentenceTransformer("all-MiniLM-L6-v2")


def calculate_similarity(ideal_answer, student_answer):
    # handle empty input
    if not student_answer or not student_answer.strip():
        return 0.0

    if not ideal_answer or not ideal_answer.strip():
        return 0.0

    # embeddings
    ideal_embedding = model.encode([ideal_answer])
    student_embedding = model.encode([student_answer])

    # similarity score (-1 to 1 range theoretically)
    similarity = cosine_similarity(ideal_embedding, student_embedding)[0][0]

    # convert to percentage scale
    score = similarity * 100

    # safety clamp (VERY IMPORTANT)
    score = max(0, min(100, score))

    return round(score, 2)