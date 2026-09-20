import os
import sys

from openai import OpenAI

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
        self.client = None

        if os.getenv("OPENAI_API_KEY"):
            self.client = OpenAI(
                api_key=os.getenv("OPENAI_API_KEY")
            )

    def run(self, path):
        result = self.agent.inspect(path)

        if not hasattr(result, "to_dict"):
            return result

        result_data = result.to_dict()

        if self.client is None:
            result_data["framework"] = "openai"
            result_data["mode"] = "local"
            return result_data

        return self.enhance_with_openai(result_data)

    def enhance_with_openai(self, result):
        prompt = f"""
You are RepoMedic, a software project diagnosis agent.

Analyze the following deterministic repository diagnosis.

Diagnosis:
{result}

Return a concise explanation containing:
1. Problem
2. Cause
3. Evidence
4. Suggested Fix
5. Confidence

Do not invent evidence that is not present in the diagnosis.
"""

        response = self.client.responses.create(
            model="gpt-5-mini",
            input=prompt
        )

        result["framework"] = "openai"
        result["mode"] = "openai"
        result["explanation"] = response.output_text

        return result


if __name__ == "__main__":
    adapter = OpenAIAdapter()

    result = adapter.run("tests/broken_project")

    print("RepoMedic OpenAI Adapter")
    print("========================")
    print(result)
