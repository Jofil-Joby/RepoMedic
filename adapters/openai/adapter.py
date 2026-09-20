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


class OpenAIAdapter:
    def __init__(self):
        self.agent = RepoMedic()

    def run(self, path):
        result = self.agent.inspect(path)

        if hasattr(result, "to_dict"):
            return result.to_dict()

        return result


if __name__ == "__main__":
    adapter = OpenAIAdapter()

    result = adapter.run("tests/broken_project")

    print("RepoMedic OpenAI Adapter")
    print("========================")
    print(result)
