
import numpy as np


class CodeVectorStore:

    def __init__(self):

        self.embeddings = None
        self.chunks = []

    def add_embeddings(self, embeddings, chunks):

        self.embeddings = np.asarray(
            embeddings,
            dtype="float32"
        )

        self.chunks = chunks

        print("Vectors stored successfully!")

    def search(self, query_embedding, top_k=3):

        if self.embeddings is None:
            raise ValueError("Vector index is empty")

        query_embedding = np.asarray(
            query_embedding,
            dtype="float32"
        )

        # Calculate cosine similarity
        scores = np.dot(
            self.embeddings,
            query_embedding.T
        ).flatten()

        # Sort results from highest similarity
        ranked_indices = np.argsort(scores)[::-1]

        results = []

        for index in ranked_indices[:top_k]:

            result = self.chunks[index].copy()

            result["similarity_score"] = float(
                scores[index]
            )

            results.append(result)

        return results
