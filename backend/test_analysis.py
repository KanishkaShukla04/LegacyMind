
from ai.ingestion import ingest_repository
from ai.chunking import chunk_repository
from ai.analysis import analyze_repository

repository_path = "../sample_data/legacy_student_system"

files = ingest_repository(repository_path)

chunks = chunk_repository(
    files,
    chunk_size=10,
    overlap=2
)

report = analyze_repository(files, chunks)

print("\n========== LEGACYMIND ANALYSIS REPORT ==========")

for metric, value in report.items():

    print(metric, ":", value)
