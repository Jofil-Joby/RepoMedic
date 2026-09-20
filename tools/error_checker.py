import os


def check_error_logs(path, files):
    error_files = []

    for file in files:
        filename = os.path.basename(file).lower()

        if filename in {"error.log", "errors.log", "npm-debug.log"}:
            error_files.append(file)

    if not error_files:
        return None

    return {
        "problem": "Error log detected",
        "cause": "The project contains an error log that may contain information about a runtime or build problem.",
        "evidence": "Error log found: " + ", ".join(error_files),
        "suggested_fix": "Inspect the error log and use the reported error to identify the underlying problem.",
        "confidence": "Medium"
    }
