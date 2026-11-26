
def build_context(question, retrieved_chunks):

    context = ""

    context += "You are LegacyMind, an AI software engineer.\n"

    context += "Answer using the provided source code.\n"

    context += "Do not invent code or file references.\n\n"

    context += f"Developer Question: {question}\n\n"

    context += "RETRIEVED SOURCE CODE:\n"

    for index, chunk in enumerate(retrieved_chunks):

        context += f"\nCode Section {index + 1}\n"

        context += f"File: {chunk['file_name']}\n"

        context += (
            f"Lines: {chunk['start_line']}"
            f"-{chunk['end_line']}\n"
        )

        context += "Code:\n"

        context += chunk["content"]

        context += "\n"

    context += "\nInstructions:\n"

    context += "- Explain the relevant code.\n"
    context += "- Mention the file name.\n"
    context += "- Mention the line numbers.\n"
    context += "- If evidence is insufficient, say so.\n"

    return context
