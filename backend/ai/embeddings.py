
from sentence_transformers import SentenceTransformer


class CodeEmbedder:

    def __init__(self):

        print("Loading embedding model...")

        self.model = SentenceTransformer(
            "all-MiniLM-L6-v2"
        )

        print("Embedding model loaded successfully!")

    def generate_embeddings(self, texts):

        embeddings = self.model.encode(
            texts,
            convert_to_numpy=True,
            normalize_embeddings=True
        )

        return embeddings

    def generate_query_embedding(self, question):

        embedding = self.model.encode(
            [question],
            convert_to_numpy=True,
            normalize_embeddings=True
        )

        return embedding
