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


def test_openai_adapter():
    adapter = OpenAIAdapter()

    result = adapter.run("tests/broken_project")

    assert isinstance(result, dict)
    assert "project_types" in result
    assert "diagnosis" in result
    assert result["framework"] == "openai"


if __name__ == "__main__":
    test_openai_adapter()
    print("OpenAI adapter verification: PASS")
