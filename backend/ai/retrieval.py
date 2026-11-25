
import re

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def normalize_code_text(text):

    # Split camelCase identifiers
    text = re.sub(r"([a-z0-9])([A-Z])", r"\1 \2", text)

    # Convert everything to lowercase
    return text.lower()


class CodeRetriever:

    def __init__(self):

        self.vectorizer = TfidfVectorizer(
            stop_words="english",
            preprocessor=normalize_code_text
        )

        self.chunks = []
        self.chunk_vectors = None

    def index_chunks(self, chunks):

        self.chunks = chunks

        documents = [
            chunk["content"]
            for chunk in chunks
        ]

        self.chunk_vectors = self.vectorizer.fit_transform(
            documents
        )

        print("Code chunks indexed successfully!")

    def search(self, question, top_k=3):

        if self.chunk_vectors is None:
            raise ValueError("No code has been indexed")

        question_vector = self.vectorizer.transform(
            [question]
        )

        scores = cosine_similarity(
            question_vector,
            self.chunk_vectors
        ).flatten()

        ranked_indices = scores.argsort()[::-1]

        results = []

        for index in ranked_indices:

            if scores[index] <= 0:
                continue

            result = self.chunks[index].copy()

            result["similarity_score"] = float(
                scores[index]
            )

            results.append(result)

            if len(results) == top_k:
                break

        return results
