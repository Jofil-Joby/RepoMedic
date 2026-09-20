import os
import sys
import json

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tools.repository_scanner import scan_repository
from tools.error_checker import check_error_logs


def check_package_file(path, files):
    has_package = any(
        os.path.basename(file) == "package.json"
        for file in files
    )

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


def run_diagnostics(path):
    result = scan_repository(path)
    findings = []

    checks = [
        check_package_file,
        check_start_script,
        check_error_logs
    ]

    for check in checks:
        finding = check(path, result["files"])

        if finding:
            findings.append(finding)

    return findings


if __name__ == "__main__":
    findings = run_diagnostics(".")

    if findings:
        print("Problems detected:")

        for number, finding in enumerate(findings, start=1):
            print(f"\nProblem {number}:")
            print(f"  Problem: {finding['problem']}")
            print(f"  Cause: {finding['cause']}")
            print(f"  Evidence: {finding['evidence']}")
            print(f"  Suggested Fix: {finding['suggested_fix']}")
            print(f"  Confidence: {finding['confidence']}")
    else:
        print("No problems detected.")
