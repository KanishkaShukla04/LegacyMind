
def analyze_repository(files, chunks):

    total_files = len(files)

    total_lines = 0
    total_characters = 0

    language_count = {}

    for file in files:

        content = file["content"]

        total_lines += len(content.splitlines())
        total_characters += len(content)

        language = file["language"]

        if language not in language_count:
            language_count[language] = 0

        language_count[language] += 1

    total_chunks = len(chunks)

    chunk_line_counts = []

    for chunk in chunks:
        number_of_lines = (
            chunk["end_line"] - chunk["start_line"] + 1
        )

        chunk_line_counts.append(number_of_lines)

    average_chunk_size = (
        sum(chunk_line_counts) / total_chunks
        if total_chunks > 0 else 0
    )

    report = {
        "total_files": total_files,
        "total_lines": total_lines,
        "total_characters": total_characters,
        "total_chunks": total_chunks,
        "average_chunk_size": round(average_chunk_size, 2),
        "language_count": language_count
    }

    return report
