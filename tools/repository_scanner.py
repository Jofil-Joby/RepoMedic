import os
import json


def scan_repository(path):
    files = []
    directories = []

    for root, dirs, filenames in os.walk(path):
        dirs[:] = [d for d in dirs if d not in {".git", ".venv", "__pycache__"}]

        for directory in dirs:
            directories.append(os.path.relpath(os.path.join(root, directory), path))

        for filename in filenames:
            files.append(os.path.relpath(os.path.join(root, filename), path))

    return {
        "directories": sorted(directories),
        "files": sorted(files)
    }


def detect_project_type(files):
    project_types = []

    filenames = set(os.path.basename(file) for file in files)

    if "package.json" in filenames:
        project_types.append("Node.js")

    if "requirements.txt" in filenames or "pyproject.toml" in filenames:
        project_types.append("Python")

    if "pom.xml" in filenames:
        project_types.append("Java Maven")

    if "build.gradle" in filenames or "build.gradle.kts" in filenames:
        project_types.append("Java Gradle")

    if "Cargo.toml" in filenames:
        project_types.append("Rust")

    if "go.mod" in filenames:
        project_types.append("Go")

    if not project_types:
        project_types.append("Unknown")

    return project_types


def scan_dependencies(path, files):
    dependencies = []

    for file in files:
        if os.path.basename(file) == "package.json":
            package_path = os.path.join(path, file)

            try:
                with open(package_path, "r", encoding="utf-8") as package_file:
                    package_data = json.load(package_file)

                dependencies.extend(
                    package_data.get("dependencies", {}).keys()
                )

                dependencies.extend(
                    package_data.get("devDependencies", {}).keys()
                )

            except (json.JSONDecodeError, OSError):
                pass

    return sorted(set(dependencies))


if __name__ == "__main__":
    result = scan_repository(".")

    print("Project Type:")
    for project_type in detect_project_type(result["files"]):
        print(f"  {project_type}")

    print("\nDependencies:")
    dependencies = scan_dependencies(".", result["files"])

    if dependencies:
        for dependency in dependencies:
            print(f"  {dependency}")
    else:
        print("  None detected")

    print("\nDirectories:")
    for directory in result["directories"]:
        print(f"  {directory}")

    print("\nFiles:")
    for file in result["files"]:
        print(f"  {file}")
