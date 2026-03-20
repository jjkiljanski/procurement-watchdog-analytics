from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


DEFAULT_NOTICE_SCHEMAS_DIR = Path(
    r"E:\git_projects\procurement-watchdog-lakehouse\src\procurement\silver\notice_schemas"
)


def models_path_for_profile(profile_path: Path) -> Path:
    profile_name = profile_path.name
    if "_profile" not in profile_name:
        raise ValueError(f"Unexpected profile file name: {profile_name}")
    model_name = profile_name.replace("_profile_automatic.json", "_models.py").replace(
        "_profile.json", "_models.py"
    )
    return profile_path.with_name(model_name)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Validate all notice profile JSON files against their Pydantic model files."
    )
    parser.add_argument(
        "--notice-schemas-dir",
        type=Path,
        default=DEFAULT_NOTICE_SCHEMAS_DIR,
        help="Directory containing *_profile*.json and *_models.py files.",
    )
    args = parser.parse_args()

    profile_paths = sorted(args.notice_schemas_dir.glob("*_profile*.json"))
    if not profile_paths:
        raise SystemExit(f"No profile JSON files found in {args.notice_schemas_dir}")

    failures = 0
    for profile_path in profile_paths:
        models_path = models_path_for_profile(profile_path)
        if not models_path.exists():
            print(f"Missing models file for {profile_path.name}: expected {models_path.name}")
            failures += 1
            continue

        result = subprocess.run(
            [
                sys.executable,
                "scripts/check_notice_schema_alignment.py",
                str(profile_path),
                str(models_path),
            ],
            text=True,
        )
        if result.returncode != 0:
            failures += 1

    if failures:
        raise SystemExit(f"Notice contract validation failed for {failures} file(s).")

    print(f"Notice contract validation passed for {len(profile_paths)} profile/model pair(s).")


if __name__ == "__main__":
    main()
