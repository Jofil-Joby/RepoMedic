import os
import sys

sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)

from tools.diagnostics import run_diagnostics


def generate_repair_plan(path):
    findings = run_diagnostics(path)

    if not findings:
        return {
            "status": "healthy",
            "message": "No known problems were detected."
        }

    repair_plan = []

    for finding in findings:
        repair_plan.append({
            "problem": finding["problem"],
            "cause": finding["cause"],
            "evidence": finding["evidence"],
            "suggested_fix": finding["suggested_fix"],
            "confidence": finding["confidence"]
        })

    return {
        "status": "problems_detected",
        "findings": repair_plan
    }


if __name__ == "__main__":
    result = generate_repair_plan("tests/broken_project")

    print("RepoMedic Diagnosis")
    print("===================")

    print(f"\nStatus: {result['status']}")

    if "findings" in result:
        for number, finding in enumerate(result["findings"], start=1):
            print(f"\nProblem {number}")
            print(f"Problem: {finding['problem']}")
            print(f"Cause: {finding['cause']}")
            print(f"Evidence: {finding['evidence']}")
            print(f"Suggested Fix: {finding['suggested_fix']}")
            print(f"Confidence: {finding['confidence']}")
    else:
        print(result["message"])
