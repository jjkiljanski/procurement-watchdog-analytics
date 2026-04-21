from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from scripts.generate_notice_profile_markdown import (
    enrich_profile_with_staging_mappings,
    extract_staging_mappings,
    render_markdown,
)
from scripts.validate_notice_staging import (
    data_model_to_relation_suffix,
    extract_staging_select,
    expected_columns_by_relation,
)
from scripts.validate_notice_contracts import models_path_for_profile


def test_render_markdown_for_mapping_sections() -> None:
    profile = {
        "1.1": {
            "col_name": "section_1_1",
            "section_header": "Rola zamawiajacego",
            "data_model": "core",
            "example_values": ["A", "B"],
            "staging_columns": ["cn_procedure_conduct_mode"],
        }
    }

    markdown = render_markdown(profile)

    assert "## 1.1" in markdown
    assert "- `col_name`: `section_1_1`" in markdown
    assert "- `example_values`:" in markdown
    assert "- `staging_columns`:" in markdown
    assert "- `cn_procedure_conduct_mode`" in markdown
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


def test_notice_staging_relation_suffix_handles_nested_models() -> None:
    assert data_model_to_relation_suffix("core") == "core"
    assert data_model_to_relation_suffix("part.core") == "part"
    assert data_model_to_relation_suffix("part.part") == "part_part"


def test_expected_columns_by_relation_uses_derived_cols_as_coverage_group() -> None:
    profile = {
        "1.1": {
            "col_name": "section_1_1",
            "data_model": "core",
        },
        "1.2": {
            "col_name": "section_1_2",
            "data_model": "part.part",
            "derived_cols": {
                "section_1_2_before": {"fn": "parse_before"},
                "section_1_2_after": {"fn": "parse_after"},
            },
        },
    }

    expected = expected_columns_by_relation(profile)

    assert expected["core"] == [{"section_1_1"}]
    assert expected["part_part"] == [{"section_1_2_before", "section_1_2_after"}]


def test_extract_staging_select_handles_case_commas_and_optional_columns() -> None:
    sql = """
select
    case
        when section_1_1 = 'A, B' then 'x'
        else null
    end as cn_mode,
    {{ optional_raw_column('section_9_9') }} as cn_optional_value
from {{ raw_silver_relation('contract_notice_core') }}
"""

    mappings, selected_source_columns, aliases = extract_staging_select(sql)

    assert mappings["section_1_1"] == ["cn_mode"]
    assert mappings["section_9_9"] == ["cn_optional_value"]
    assert "section_9_9" not in selected_source_columns
    assert aliases == {"cn_mode", "cn_optional_value"}


def test_extract_staging_mappings_captures_direct_and_case_mappings() -> None:
    sql = """
select
    case
        when section_1_1 = 'A' then 'x'
        else null
    end as cn_procedure_conduct_mode,
    section_1_11_8_code as cn_procedure_operator_nuts3_code,
    section_1_11_8_name as cn_procedure_operator_nuts3_name
from something
"""

    mappings = extract_staging_mappings(sql)

    assert mappings["section_1_1"] == ["cn_procedure_conduct_mode"]
    assert mappings["section_1_11_8_code"] == ["cn_procedure_operator_nuts3_code"]
    assert mappings["section_1_11_8_name"] == ["cn_procedure_operator_nuts3_name"]


def test_enrich_profile_with_staging_mappings_adds_staging_columns() -> None:
    profile = {
        "1.1": {
            "col_name": "section_1_1",
            "data_model": "core",
        },
        "1.11.8": {
            "col_name": "section_1_11_8",
            "data_model": "core",
            "derived_cols": {
                "section_1_11_8_code": {"fn": "x"},
                "section_1_11_8_name": {"fn": "y"},
            },
        },
    }

    repo_root = Path(__file__).resolve().parents[1]
    staging_dir = repo_root / "tests" / "fixtures" / "staging_mappings"
    profile_path = Path("contract_notice_profile.json")

    enriched = enrich_profile_with_staging_mappings(profile, profile_path, staging_dir)

    assert enriched["1.1"]["staging_columns"] == ["cn_procedure_conduct_mode"]
    assert enriched["1.11.8"]["staging_columns"] == [
        "cn_procedure_operator_nuts3_code",
        "cn_procedure_operator_nuts3_name",
    ]


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
