
def chunk_file(file_data, chunk_size=30, overlap=5):

    content = file_data["content"]
    lines = content.splitlines()

    chunks = []

    start = 0

    while start < len(lines):

        end = min(start + chunk_size, len(lines))

        # Prefer ending a chunk at a blank line
        if end < len(lines):
            for position in range(end - 1, start, -1):
                if lines[position].strip() == "":
                    end = position + 1
                    break

        chunk_content = "\n".join(lines[start:end])

        chunk = {
            "file_name": file_data["file_name"],
            "file_path": file_data["file_path"],
            "language": file_data["language"],
            "start_line": start + 1,
            "end_line": end,
            "content": chunk_content
        }

        chunks.append(chunk)

        if end == len(lines):
            break

        next_start = end - overlap

        # Avoid getting stuck if overlap is too large
        start = max(next_start, start + 1)

    return chunks


def chunk_repository(files, chunk_size=30, overlap=5):

    all_chunks = []

    for file_data in files:

        file_chunks = chunk_file(
            file_data,
            chunk_size,
            overlap
        )

        all_chunks.extend(file_chunks)

    return all_chunks
