from pathlib import Path
SUPPORTED_EXTENSIONS={
    ".java",
    ".py",
    ".cpp",
    ".c",
    ".h",
    ".js",
    ".ts"
}

IGNORED_FOLDERS={
    ".git",
    "venv",
    ".venv",
    "node_modules",
    "__pycache__"
}

def ingest_repository(repository_path):
    repository_path = Path(repository_path)

    if not repository_path.exists():
        raise FileNotFoundError("Repository not found")

    collected_files = []

    for file_path in repository_path.rglob("*"):

        if not file_path.is_file():
            continue

        if any(folder in IGNORED_FOLDERS
               for folder in file_path.parts):
            continue

        if file_path.suffix.lower() not in SUPPORTED_EXTENSIONS:
            continue

        try:
            content = file_path.read_text(
                encoding="utf-8",
                errors="ignore"
            )

            collected_files.append({
                "file_name": file_path.name,
                "file_path": str(file_path),
                "content": content,
                "language": file_path.suffix.lower()
            })

        except OSError:
            print("Unable to read:", file_path)

    return collected_files
