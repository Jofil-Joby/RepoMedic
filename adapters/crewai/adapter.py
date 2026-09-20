import os
import sys

sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.dirname(
                os.path.abspath(__file__)
            )
        )
    )
)

from agent import RepoMedic
from adapters.base import AdapterContract


class CrewAIAdapter(AdapterContract):
    framework = "crewai"

    def __init__(self):
        self.agent = RepoMedic()

    def run(self, path):
        result = self.agent.inspect(path)

        if not hasattr(result, "to_dict"):
            return result

        result_data = result.to_dict()
        result_data["framework"] = self.framework
        result_data["mode"] = "portable"

        return result_data


if __name__ == "__main__":
    adapter = CrewAIAdapter()

    result = adapter.run("tests/broken_project")

    print("RepoMedic CrewAI Adapter")
    print("========================")
    print(result)

    print("\nPassport Verification:")
    print(adapter.verify("tests/broken_project"))
