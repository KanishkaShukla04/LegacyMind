from ai.rag_pipeline import LegacyMindRAG

repository_path = "../sample_data/legacy_student_system"

rag = LegacyMindRAG()

rag.index_repository(repository_path)

question = "How can I find a student using their identification number?"

answer = rag.ask_gemini(question)

print("\n========== AI ANSWER ==========")
print(answer)

print("\n========== PERFORMANCE REPORT ==========")

for metric, value in rag.performance.items():
    print(metric, ":", value)