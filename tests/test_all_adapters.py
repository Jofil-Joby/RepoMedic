import os
import sys

sys.path.insert(
    0,
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)

from adapters.openai.adapter import OpenAIAdapter
from adapters.crewai.adapter import CrewAIAdapter
from adapters.claude.adapter import ClaudeAdapter
from adapters.lyzr.adapter import LyzrAdapter


def test_adapter(adapter_class):
    adapter = adapter_class()

    result = adapter.run("tests/broken_project")

    assert isinstance(result, dict)
    assert "project_types" in result
    assert "diagnosis" in result
    assert "framework" in result
    assert adapter.verify("tests/broken_project") is True

    return result


def main():
    adapters = [
        OpenAIAdapter,
        CrewAIAdapter,
        ClaudeAdapter,
        LyzrAdapter
    ]

    print("RepoMedic Adapter Verification")
    print("==============================")

    for adapter_class in adapters:
        result = test_adapter(adapter_class)

        print(
            f"{adapter_class.framework if hasattr(adapter_class, 'framework') else adapter_class.__name__}: PASS"
        )
        print(f"  Framework: {result['framework']}")
        print(f"  Mode: {result.get('mode', 'unknown')}")
        print(f"  Diagnosis: {result['diagnosis']['status']}")

    print()
    print("All adapter verification checks: PASS")


if __name__ == "__main__":
    main()
