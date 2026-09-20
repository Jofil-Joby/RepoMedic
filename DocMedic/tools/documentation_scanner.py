import os

def scan_documentation(path):
    files = []

    for root, directories, filenames in os.walk(path):
        directories[:] = [
            d for d in directories
            if d not in {".git", ".venv", "__pycache__", "node_modules"}
        ]

        for filename in filenames:
            full_path = os.path.join(root, filename)
            relative_path = os.path.relpath(full_path, path)
            files.append(relative_path)

    documentation = []

    for filename in files:
        normalized = filename.replace("\\", "/").lower()

        if (
            os.path.basename(filename).lower().startswith("readme")
            or os.path.basename(filename).lower() in {
                "contributing.md",
                "changelog.md",
                "license",
            }
            or "/docs/" in normalized
        ):
            documentation.append(filename)

    return {
        "files": files,
        "documentation": documentation
    }
