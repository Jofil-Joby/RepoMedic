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

from adapters.openai_adapter import OpenAIAdapter
from adapters.crewai_adapter import CrewAIAdapter
from adapters.claude_adapter import ClaudeCodeAdapter
from adapters.lyzr_adapter import LyzrAdapter


path = "tests/broken_project"

adapters = [
    OpenAIAdapter(),
    CrewAIAdapter(),
    ClaudeCodeAdapter(),
    LyzrAdapter()
]

print("DocMedic Adapter Verification")
print("==============================")

all_passed = True

for adapter in adapters:

    result = adapter.verify(path)

    passed = result["verified"]

    if not passed:
        all_passed = False

    print(f"{adapter.framework}: {'PASS' if passed else 'FAIL'}")
    print(f"  Framework: {adapter.framework}")

    if adapter.framework == "openai":
        print(f"  Mode: {result['mode']}")

    print(
        f"  Diagnosis: "
        f"{result['result']['diagnosis']['status']}"
    )

print()

if all_passed:
    print("All adapter verification checks: PASS")
else:
    print("Adapter verification checks: FAIL")
