
from ai.ingestion import ingest_repository
from ai.chunking import chunk_repository
from ai.retrieval import CodeRetriever
from ai.context_builder import build_context


# Step 1: Read repository
repository_path = "../sample_data/legacy_student_system"

files = ingest_repository(repository_path)


# Step 2: Create code chunks
chunks = chunk_repository(
    files,
    chunk_size=10,
    overlap=2
)


# Step 3: Index chunks
retriever = CodeRetriever()
retriever.index_chunks(chunks)


# Step 4: Developer question
question = "Where is student search functionality implemented?"


# Step 5: Retrieve relevant code
results = retriever.search(
    question,
    top_k=3
)


# Step 6: Build context
context = build_context(
    question,
    results
)


# Step 7: Display context
print("\nLEGACYMIND RAG CONTEXT")
print("======================\n")

print(context)
