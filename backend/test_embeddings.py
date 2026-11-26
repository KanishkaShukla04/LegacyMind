
from ai.ingestion import ingest_repository
from ai.chunking import chunk_repository
from ai.embeddings import CodeEmbedder
from ai.vector_store import CodeVectorStore


# Step 1: Read the repository
repository_path = "../sample_data/legacy_student_system"

files = ingest_repository(repository_path)


# Step 2: Create code chunks
chunks = chunk_repository(
    files,
    chunk_size=10,
    overlap=2
)

print("Total chunks:", len(chunks))


# Step 3: Load embedding model
embedder = CodeEmbedder()


# Step 4: Generate embeddings for code
documents = [
    chunk["content"]
    for chunk in chunks
]

embeddings = embedder.generate_embeddings(documents)

print("Embedding shape:", embeddings.shape)


# Step 5: Create vector store
vector_store = CodeVectorStore()

vector_store.add_embeddings(
    embeddings,
    chunks
)


# Step 6: Ask a natural-language question
question = "How can I find a student using their identification number?"


# Step 7: Convert question into an embedding
query_embedding = embedder.generate_query_embedding(
    question
)


# Step 8: Retrieve matching code
results = vector_store.search(
    query_embedding,
    top_k=3
)


# Step 9: Display results
print("\nSEMANTIC SEARCH RESULTS")

for result in results:

    print("\n----------------------")

    print("File:", result["file_name"])

    print(
        "Lines:",
        result["start_line"],
        "-",
        result["end_line"]
    )

    print(
        "Similarity:",
        round(result["similarity_score"], 3)
    )

    print("Code:")
    print(result["content"])
