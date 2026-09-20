import os
import sys
import json

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


def check_start_script(path, files):
    package_files = [
        file for file in files
        if os.path.basename(file) == "package.json"
    ]

    for file in package_files:
        package_path = os.path.join(path, file)

        try:
            with open(package_path, "r", encoding="utf-8") as package_file:
                package_data = json.load(package_file)

            scripts = package_data.get("scripts", {})

            if "start" not in scripts:
                return {
                    "problem": "Missing start script",
                    "cause": "The Node.js project does not define a start script in package.json.",
                    "evidence": "The scripts section does not contain a start command.",
                    "suggested_fix": "Add a start script to package.json.",
                    "confidence": "High"
                }

        except (json.JSONDecodeError, OSError):
            pass

    return None


def diagnose(path):
    result = scan_repository(path)

    diagnosis = check_package_file(result["files"])

    if diagnosis:
        return diagnosis

    diagnosis = check_start_script(path, result["files"])

    if diagnosis:
        return diagnosis

    return None


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
