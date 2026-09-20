import os

from adapters.base import AdapterContract
from agent import DocMedic


class OpenAIAdapter(AdapterContract):

    framework = "openai"

    def run(self, path):

        agent = DocMedic()
        result = agent.inspect(path)

        return result.to_dict()

    def verify(self, path):

        result = self.run(path)

        if os.getenv("OPENAI_API_KEY"):
            mode = "sdk"
        else:
            mode = "local"

        return {
            "framework": self.framework,
            "mode": mode,
            "verified": super().verify(path),
            "result": result
        }


if __name__ == "__main__":

    adapter = OpenAIAdapter()

    result = adapter.verify("tests/broken_project")

    print("OpenAI Adapter")
    print("================")
    print(f"Framework: {result['framework']}")
    print(f"Mode: {result['mode']}")
    print(f"Verified: {result['verified']}")
