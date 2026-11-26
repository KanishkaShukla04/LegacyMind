
print("STEP 1: Starting retrieval test")

from ai.ingestion import ingest_repository
print("STEP 2: Ingestion imported")

from ai.chunking import chunk_repository
print("STEP 3: Chunking imported")

from ai.retrieval import CodeRetriever
print("STEP 4: Retrieval imported")


repository_path = "../sample_data/legacy_student_system"

files = ingest_repository(repository_path)
print("STEP 5: Files found:", len(files))


chunks = chunk_repository(files, chunk_size=10, overlap=2)
print("STEP 6: Chunks created:", len(chunks))


retriever = CodeRetriever()
print("STEP 7: Retriever created")


retriever.index_chunks(chunks)
print("STEP 8: Chunks indexed")


question = "Find the method that searches for a student using ID?" \
""

print("STEP 9: Searching:", question)

results = retriever.search(question, top_k=3)

print("STEP 10: Results found:", len(results))


for result in results:

    print("\n----------------------")
    print("File:", result["file_name"])
    print("Lines:", result["start_line"], "-", result["end_line"])
    print("Score:", result["similarity_score"])
    print("Code:", result["content"])


print("\nRETRIEVAL TEST FINISHED")
