import os

from tools.repository_scanner import scan_repository, detect_project_type
from tools.diagnosis_engine import generate_repair_plan


class RepoMedic:
    def inspect(self, path):
        if not os.path.exists(path):
            return {
                "status": "error",
                "message": "The specified project path does not exist."
            }

        repository = scan_repository(path)

        project_types = detect_project_type(repository["files"])
        diagnosis = generate_repair_plan(path)

        return {
            "project_types": project_types,
            "files": repository["files"],
            "directories": repository["directories"],
            "diagnosis": diagnosis
        }


if __name__ == "__main__":
    agent = RepoMedic()

    result = agent.inspect("tests/broken_project")

    print("RepoMedic Agent")
    print("================")

    print("\nProject Type:")
    for project_type in result["project_types"]:
        print(f"  {project_type}")

    print("\nDiagnosis:")
    print(f"  Status: {result['diagnosis']['status']}")

    if "findings" in result["diagnosis"]:
        for number, finding in enumerate(
            result["diagnosis"]["findings"],
            start=1
        ):
            print(f"\n  Problem {number}")
            print(f"  Problem: {finding['problem']}")
            print(f"  Cause: {finding['cause']}")
            print(f"  Evidence: {finding['evidence']}")
            print(f"  Suggested Fix: {finding['suggested_fix']}")
            print(f"  Confidence: {finding['confidence']}")
