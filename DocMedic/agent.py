import os

from tools.documentation_scanner import scan_documentation
from tools.documentation_checker import check_documentation
from core.result import DocumentationResult


class DocMedic:

    def inspect(self, path):

        if not os.path.exists(path):
            return {
                "status": "error",
                "message": "The specified project path does not exist."
            }

        documentation = scan_documentation(path)

        diagnosis = check_documentation(
            path,
            documentation
        )

        return DocumentationResult(
            documentation,
            diagnosis
        )


if __name__ == "__main__":

    agent = DocMedic()
    result = agent.inspect("tests/broken_project")

    print("DocMedic Agent")
    print("================")

    print("\nDocumentation Files:")

    for documentation_file in result.documentation["documentation"]:
        print(f"  {documentation_file}")

    print("\nSummary:")
    print(f"  {result.summary()}")

    print("\nDiagnosis:")
    print(f"  Status: {result.diagnosis['status']}")

    if "findings" in result.diagnosis:

        for number, finding in enumerate(
            result.diagnosis["findings"],
            start=1
        ):
            print(f"\n  Problem {number}")
            print(f"  Problem: {finding['problem']}")
            print(f"  Cause: {finding['cause']}")
            print(f"  Evidence: {finding['evidence']}")
            print(f"  Suggested Fix: {finding['suggested_fix']}")
            print(f"  Confidence: {finding['confidence']}")
