def check_package_file(files):
    has_package = any(file.endswith("package.json") for file in files)

    if not has_package:
        return {
            "problem": "Missing package.json",
            "cause": "A Node.js project may not have its package configuration file.",
            "evidence": "No package.json file was found.",
            "suggested_fix": "Create or restore the package.json file.",
            "confidence": "Medium"
        }

    return None
