from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from scripts.generate_notice_profile_markdown import render_markdown
from scripts.validate_notice_contracts import models_path_for_profile


def test_render_markdown_for_mapping_sections() -> None:
    profile = {
        "1.1": {
            "col_name": "section_1_1",
            "section_header": "Rola zamawiajacego",
            "data_model": "core",
            "example_values": ["A", "B"],
        }
    }

    markdown = render_markdown(profile)

    assert "## 1.1" in markdown
    assert "- `col_name`: `section_1_1`" in markdown
    assert "- `example_values`:" in markdown
    assert "Specific column-level value constraints are defined separately" in markdown


def test_render_markdown_for_list_sections() -> None:
    profile = {
        "2.1": [
            {
                "col_name": "section_2_1",
                "section_header": "Example",
                "data_model": "core",
            }
        ]
    }

    markdown = render_markdown(profile)

    assert "## 2.1" in markdown
    assert "- `col_name`: `section_2_1`" in markdown


def test_models_path_for_profile_handles_automatic_suffix() -> None:
    profile_path = Path("competition_result_notice_profile_automatic.json")
    assert models_path_for_profile(profile_path).name == "competition_result_notice_models.py"


def test_validate_notice_contracts_passes_for_aligned_pair() -> None:
    repo_root = Path(__file__).resolve().parents[1]
    schemas_dir = repo_root / "tests" / "fixtures" / "notice_contracts" / "pass"

    result = subprocess.run(
        [
            sys.executable,
            "scripts/validate_notice_contracts.py",
            "--notice-schemas-dir",
            str(schemas_dir),
        ],
        cwd=repo_root,
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0
    assert "Notice contract validation passed" in result.stdout


def test_validate_notice_contracts_fails_for_missing_field() -> None:
    repo_root = Path(__file__).resolve().parents[1]
    schemas_dir = repo_root / "tests" / "fixtures" / "notice_contracts" / "fail_missing_field"

    result = subprocess.run(
        [
            sys.executable,
            "scripts/validate_notice_contracts.py",
            "--notice-schemas-dir",
            str(schemas_dir),
        ],
        cwd=repo_root,
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode != 0
    assert "missing fields" in result.stdout
