
from ai.rag_pipeline import LegacyMindRAG

repository_path = "../sample_data/legacy_student_system"

rag = LegacyMindRAG()

rag.index_repository(repository_path)

question = "How can I find a student using their identification number?"

context = rag.ask_question(question)

print("\n========== GENERATED RAG CONTEXT ==========")
print(context)
