
import time

from ai.ingestion import ingest_repository
from ai.chunking import chunk_repository
from ai.embeddings import CodeEmbedder
from ai.vector_store import CodeVectorStore
from ai.context_builder import build_context
from ai.gemini_client import generate_answer


class LegacyMindRAG:

    def __init__(self):
        self.embedder = CodeEmbedder()
        self.vector_store = CodeVectorStore()
        self.performance = {}

    def index_repository(self, repository_path):

        print("\nReading repository...")

        files = ingest_repository(repository_path)

        print("Files found:", len(files))

        print("\nCreating code chunks...")

        chunks = chunk_repository(
            files,
            chunk_size=10,
            overlap=2
        )

        print("Total chunks:", len(chunks))

        code_texts = [
            chunk["content"] for chunk in chunks
        ]

        print("\nGenerating embeddings...")

        start_time = time.perf_counter()

        embeddings = self.embedder.generate_embeddings(
            code_texts
        )

        embedding_time = time.perf_counter() - start_time

        self.performance["embedding_time"] = round(
            embedding_time, 4
        )

        self.vector_store.add_embeddings(
            embeddings,
            chunks
        )

        print("\nRepository indexed successfully!")

    def ask_question(self, question):

        total_start = time.perf_counter()

        query_embedding = (
            self.embedder.generate_query_embedding(question)
        )

        search_start = time.perf_counter()

        results = self.vector_store.search(
            query_embedding,
            top_k=3
        )

        search_time = time.perf_counter() - search_start

        context = build_context(question, results)

        total_time = time.perf_counter() - total_start

        average_similarity = (
            sum(result["similarity_score"] for result in results)
            / len(results)
            if results else 0
        )

        self.performance["search_time"] = round(
            search_time, 6
        )

        self.performance["average_similarity"] = round(
            average_similarity, 4
        )

        self.performance["retrieved_chunks"] = len(results)

        self.performance["context_time"] = round(
            total_time - search_time, 6
        )

        return context

    def ask_gemini(self, question):

        total_start = time.perf_counter()

        context = self.ask_question(question)

        print("\nSending context to Gemini...")

        gemini_start = time.perf_counter()

        answer = generate_answer(context)

        gemini_time = time.perf_counter() - gemini_start

        total_time = time.perf_counter() - total_start

        self.performance["gemini_time"] = round(
            gemini_time, 3
        )

        self.performance["total_question_time"] = round(
            total_time, 3
        )

        return answer
