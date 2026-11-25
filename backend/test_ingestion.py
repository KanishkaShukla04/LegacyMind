
from ai.ingestion import ingest_repository

repository_path = "../sample_data/legacy_student_system"

files = ingest_repository(repository_path)

print("Total files:", len(files))

for file in files:
    print("\nFilename:", file["file_name"])
    print("Language:", file["language"])
    print("Characters:", len(file["content"]))
