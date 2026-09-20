import os
import sys

ROOT = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

sys.path.insert(0, ROOT)


def check_file(filename):
    path = os.path.join(ROOT, filename)

    if not os.path.isfile(path):
        return False

    return os.path.getsize(path) > 0


def check_agent_yaml():
    path = os.path.join(ROOT, "agent.yaml")

    if not os.path.isfile(path):
        return False

    with open(path, "r", encoding="utf-8") as file:
        content = file.read()

    return (
        'spec_version: "0.1.0"' in content
        and "name: repomedic" in content
    )


def check_explainability():
    path = os.path.join(ROOT, "EXPLAINABILITY.md")

    if not os.path.isfile(path):
        return False

    with open(path, "r", encoding="utf-8") as file:
        content = file.read().lower()

    return (
        "# decision" in content
        and "# inputs" in content
        and "# limits" in content
    )


def main():
    required_files = [
        "agent.yaml",
        "SOUL.md",
        "AGENTS.md",
        "DUTIES.md",
        "EXPLAINABILITY.md"
    ]

    print("RepoMedic Passport Verification")
    print("===============================")

    all_passed = True

    for filename in required_files:
        passed = check_file(filename)
        print(f"{filename}: {'PASS' if passed else 'FAIL'}")

        if not passed:
            all_passed = False

    agent_yaml = check_agent_yaml()
    explainability = check_explainability()

    print(f"agent.yaml rules: {'PASS' if agent_yaml else 'FAIL'}")
    print(f"EXPLAINABILITY rules: {'PASS' if explainability else 'FAIL'}")

    print()

    if all_passed and agent_yaml and explainability:
        print("Passport verification: PASS")
        return 0

    print("Passport verification: FAIL")
    return 1


if __name__ == "__main__":
    sys.exit(main())
