import os
import json


def check_dependencies(path, files):
    package_files = [
        file for file in files
        if os.path.basename(file) == "package.json"
    ]

    if not package_files:
        return None

    package_path = os.path.join(path, package_files[0])

    try:
        with open(package_path, "r", encoding="utf-8") as package_file:
            package_data = json.load(package_file)

        dependencies = {}

        dependencies.update(package_data.get("dependencies", {}))
        dependencies.update(package_data.get("devDependencies", {}))

        if not dependencies:
            return None

        node_modules_exists = any(
            os.path.basename(file) == "node_modules"
            for file in files
        )

        if not node_modules_exists:
            return {
                "problem": "Dependencies may not be installed",
                "cause": "The project declares npm dependencies but no node_modules directory was detected.",
                "evidence": f"{len(dependencies)} dependency packages are declared in package.json.",
                "suggested_fix": "Run npm install in the project directory.",
                "confidence": "Medium"
            }

    except (json.JSONDecodeError, OSError):
        pass

    return None
