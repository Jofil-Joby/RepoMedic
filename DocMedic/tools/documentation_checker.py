import os

def check_documentation(path, scan_result):
    findings = []

    documentation_files = scan_result["documentation"]
    project_files = scan_result["files"]

    readme_exists = any(
        os.path.basename(f).lower().startswith("readme")
        for f in documentation_files
    )

    if not readme_exists:
        findings.append({
            "problem": "README documentation is missing.",
            "cause": "No README file was detected.",
            "evidence": "No README file was found in the project.",
            "suggested_fix": "Add a README containing project purpose, setup, usage, and development information.",
            "confidence": "high"
        })

    if not project_files:
        findings.append({
            "problem": "Project contains no detectable files.",
            "cause": "The inspected directory appears to be empty.",
            "evidence": "The scanner detected no project files.",
            "suggested_fix": "Provide a project directory containing source code and documentation.",
            "confidence": "high"
        })

    has_docs_directory = any(
        "/docs/" in f.replace("\\", "/").lower()
        for f in documentation_files
    )

    if not has_docs_directory and len(project_files) > 10:
        findings.append({
            "problem": "Dedicated documentation directory was not detected.",
            "cause": "The project contains multiple files but no docs directory.",
            "evidence": "No documentation path containing docs/ was detected.",
            "suggested_fix": "Consider adding a docs directory for detailed technical documentation.",
            "confidence": "medium"
        })

    if not findings:
        return {
            "status": "healthy",
            "message": "No known documentation problems were detected."
        }

    return {
        "status": "problems_detected",
        "findings": findings
    }
