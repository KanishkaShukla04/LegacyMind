
from ai.ingestion import ingest_repository
from ai.chunking import chunk_repository

repository_path = "../sample_data/legacy_student_system"

# Stage 1: Read repository
files = ingest_repository(repository_path)

# Stage 2: Divide source code into chunks
chunks = chunk_repository(
    files,
    chunk_size=10,
    overlap=2
)

print("Total files:", len(files))
print("Total chunks:", len(chunks))

for chunk in chunks:

    print("\n-------------------------")
    print("File:", chunk["file_name"])
    print("Lines:", chunk["start_line"],
          "-", chunk["end_line"])

    print("Code:")
    print(chunk["content"])
