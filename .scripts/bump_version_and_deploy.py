import json
import subprocess
from pathlib import Path

MANIFEST_PATH = Path(__file__).parent.parent / "custom_components" / "mysutro" / "manifest.json"


def bump_version(version: str) -> str:
    major, minor, patch = map(int, version.split("."))
    patch += 1
    return f"{major}.{minor}.{patch}"


def update_manifest_version():
    with open(MANIFEST_PATH, "r+", encoding="utf-8") as f:
        data = json.load(f)
        old_version = data["version"]
        new_version = bump_version(old_version)
        data["version"] = new_version
        f.seek(0)
        json.dump(data, f, indent=4)
        f.truncate()
    return old_version, new_version


def git_commit_and_push(new_version: str):
    subprocess.run(["git", "add", str(MANIFEST_PATH)], check=True)
    subprocess.run(["git", "commit", "-m", f"Bump version to {new_version}"], check=True)
    subprocess.run(["git", "push"], check=True)


def main():
    old_version, new_version = update_manifest_version()
    print(f"Version updated: {old_version} -> {new_version}")
    git_commit_and_push(new_version)
    print("Committed and pushed to repository.")

if __name__ == "__main__":
    main()
