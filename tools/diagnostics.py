import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tools.repository_scanner import scan_repository


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


def diagnose(path):
    result = scan_repository(path)
    diagnosis = check_package_file(result["files"])

    return diagnosis


if __name__ == "__main__":
    diagnosis = diagnose(".")

    if diagnosis:
        print("Problem:")
        print(f"  {diagnosis['problem']}")

        print("\nCause:")
        print(f"  {diagnosis['cause']}")

        print("\nEvidence:")
        print(f"  {diagnosis['evidence']}")

        print("\nSuggested Fix:")
        print(f"  {diagnosis['suggested_fix']}")

        print("\nConfidence:")
        print(f"  {diagnosis['confidence']}")
    else:
        print("No problems detected.")
