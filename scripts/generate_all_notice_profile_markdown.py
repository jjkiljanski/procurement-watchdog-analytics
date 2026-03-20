from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


DEFAULT_NOTICE_SCHEMAS_DIR = Path(
    r"E:\git_projects\procurement-watchdog-lakehouse\src\procurement\silver\notice_schemas"
)
DEFAULT_OUTPUT_DIR = Path("docs/notice_profiles")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate markdown catalogs for all notice profile JSON files."
    )
    parser.add_argument(
        "--notice-schemas-dir",
        type=Path,
        default=DEFAULT_NOTICE_SCHEMAS_DIR,
        help="Directory containing *_profile*.json files.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=DEFAULT_OUTPUT_DIR,
        help="Directory where markdown files should be written.",
    )
    args = parser.parse_args()

    profile_paths = sorted(args.notice_schemas_dir.glob("*_profile*.json"))
    if not profile_paths:
        raise SystemExit(f"No profile JSON files found in {args.notice_schemas_dir}")

    args.output_dir.mkdir(parents=True, exist_ok=True)

    for profile_path in profile_paths:
        output_path = args.output_dir / f"{profile_path.stem}.md"
        subprocess.run(
            [
                sys.executable,
                "scripts/generate_notice_profile_markdown.py",
                str(profile_path),
                str(output_path),
            ],
            check=True,
        )

    print(f"Generated {len(profile_paths)} markdown files in {args.output_dir}")


if __name__ == "__main__":
    main()
