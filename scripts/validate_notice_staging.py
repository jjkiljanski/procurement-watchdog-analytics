from __future__ import annotations

import argparse
import glob
import json
import re
import shutil
import subprocess
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any


DEFAULT_NOTICE_SCHEMAS_DIR = Path(
    r"E:\git_projects\procurement-watchdog-lakehouse\src\procurement\silver\notice_schemas"
)
DEFAULT_STAGING_DIR = Path("models/staging/bzp")
DEFAULT_LOCAL_RAW_DIR = Path("models/platform/local_raw")
DEFAULT_SOURCES_YML = Path("models/sources/_raw_silver__sources.yml")
DEFAULT_LOCAL_RAW_YML = Path("models/platform/local_raw/_local_raw__models.yml")
DEFAULT_LOCAL_SILVER_ROOT = Path(
    r"E:\git_projects\procurement-watchdog-api-exploration\data\silver"
)

RAW_COLUMN_PATTERN = re.compile(
    r"\b(?:objectId|publicationDateDay|noticeType|element|[a-z]+(?:_[a-z]+)*_ordinal|section_\d[\w_]*)\b"
)
RAW_ALIAS_PREFIXES = ("section_",)


def notice_token_from_profile(profile_path: Path) -> str:
    name = profile_path.name
    if name.endswith("_profile_automatic.json"):
        return name.removesuffix("_profile_automatic.json")
    if name.endswith("_profile.json"):
        return name.removesuffix("_profile.json")
    raise ValueError(f"Unexpected profile file name: {profile_path.name}")


def data_model_to_relation_suffix(data_model: str) -> str:
    if data_model.endswith(".core"):
        data_model = data_model.removesuffix(".core")
    return data_model.replace(".", "_")


def load_profile(profile_path: Path) -> dict[str, Any]:
    return json.loads(profile_path.read_text(encoding="utf-8"))


def expected_columns_by_relation(profile: dict[str, Any]) -> dict[str, list[set[str]]]:
    expected: dict[str, list[set[str]]] = defaultdict(list)

    for section_data in profile.values():
        if not isinstance(section_data, dict):
            continue

        relation = data_model_to_relation_suffix(section_data["data_model"])
        derived_cols = set(section_data.get("derived_cols", {}))
        if derived_cols:
            expected[relation].append(derived_cols)
        else:
            expected[relation].append({section_data["col_name"]})

    return dict(expected)


def source_table_names(sources_yml: Path) -> set[str]:
    names = set(re.findall(r"(?m)^\s{6}- name:\s*([A-Za-z0-9_]+)\s*$", sources_yml.read_text(encoding="utf-8")))
    names.discard("raw_silver")
    return names


def local_raw_model_names(local_raw_yml: Path) -> set[str]:
    return set(re.findall(r"(?m)^\s{2}- name:\s*([A-Za-z0-9_]+)\s*$", local_raw_yml.read_text(encoding="utf-8")))


def split_select_items(select_body: str) -> list[str]:
    items: list[str] = []
    current: list[str] = []
    paren_depth = 0
    in_single_quote = False
    in_double_quote = False
    previous_char = ""

    for char in select_body:
        if char == "'" and not in_double_quote and previous_char != "\\":
            in_single_quote = not in_single_quote
        elif char == '"' and not in_single_quote and previous_char != "\\":
            in_double_quote = not in_double_quote
        elif not in_single_quote and not in_double_quote and char == "(":
            paren_depth += 1
        elif not in_single_quote and not in_double_quote and char == ")":
            paren_depth = max(paren_depth - 1, 0)
        elif not in_single_quote and not in_double_quote and char == "," and paren_depth == 0:
            item = "".join(current).strip()
            if item:
                items.append(item)
            current = []
            previous_char = char
            continue
        current.append(char)
        previous_char = char

    item = "".join(current).strip()
    if item:
        items.append(item)

    return items


def select_body(sql_text: str) -> str:
    match = re.search(r"(?is)\bselect\b(?P<body>.*?)\bfrom\b", sql_text)
    if not match:
        raise ValueError("Could not find SELECT ... FROM block")
    return match.group("body")


def extract_staging_select(sql_text: str) -> tuple[dict[str, list[str]], set[str], set[str]]:
    source_to_aliases: dict[str, list[str]] = defaultdict(list)
    source_columns: set[str] = set()
    aliases: set[str] = set()

    for item in split_select_items(select_body(sql_text)):
        alias_match = re.search(r"(?is)\s+as\s+([A-Za-z_][A-Za-z0-9_]*)\s*$", item)
        if not alias_match:
            continue

        alias = alias_match.group(1)
        expression = item[: alias_match.start()].strip()
        aliases.add(alias)

        optional_cols = re.findall(r"optional_raw_column\(['\"]([A-Za-z0-9_]+)['\"]\)", expression)
        for source_col in optional_cols:
            source_to_aliases[source_col].append(alias)

        expression_for_scan = re.sub(
            r"optional_raw_column\(['\"][A-Za-z0-9_]+['\"]\)",
            "",
            expression,
        )
        for source_col in RAW_COLUMN_PATTERN.findall(expression_for_scan):
            source_columns.add(source_col)
            source_to_aliases[source_col].append(alias)

    return dict(source_to_aliases), source_columns, aliases


def extract_raw_relation_name(sql_text: str) -> str | None:
    match = re.search(r"raw_silver_relation\(['\"]([A-Za-z0-9_]+)['\"]\)", sql_text)
    if match:
        return match.group(1)
    return None


def parquet_columns_from_local_raw(
    local_raw_sql: Path,
    local_silver_root: Path,
    required_columns: set[str],
) -> set[str]:
    sql_text = local_raw_sql.read_text(encoding="utf-8")
    match = re.search(r"\{\{\s*var\(['\"]local_silver_root['\"]\)\s*\}\}([^'\"]+)", sql_text)
    if not match:
        raise ValueError(f"Could not extract local_silver_root parquet pattern from {local_raw_sql}")

    pattern = str(local_silver_root) + match.group(1)
    import pyarrow.parquet as pq

    columns: set[str] = set()
    matched_any = False
    for parquet_path in glob.iglob(pattern, recursive=True):
        matched_any = True
        columns.update(pq.ParquetFile(parquet_path).schema.names)
        if required_columns.issubset(columns):
            break
    if not matched_any:
        raise FileNotFoundError(f"No parquet files matched {pattern}")
    return columns


def bigquery_columns(table_name: str, project: str, dataset: str) -> set[str]:
    bq_executable = shutil.which("bq") or shutil.which("bq.cmd") or shutil.which("bq.exe")
    if bq_executable is None:
        raise FileNotFoundError("Could not find bq, bq.cmd, or bq.exe on PATH")

    result = subprocess.run(
        [bq_executable, "show", "--format=json", f"{project}:{dataset}.{table_name}"],
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or result.stdout.strip())

    table = json.loads(result.stdout)
    return {field["name"] for field in table.get("schema", {}).get("fields", [])}


def validate(args: argparse.Namespace) -> list[str]:
    failures: list[str] = []
    profile_paths = sorted(args.notice_schemas_dir.glob("*_profile*.json"))
    if not profile_paths:
        return [f"No profile JSON files found in {args.notice_schemas_dir}"]

    raw_source_tables = source_table_names(args.sources_yml)
    local_models = local_raw_model_names(args.local_raw_yml)

    for profile_path in profile_paths:
        notice_token = notice_token_from_profile(profile_path)
        profile = load_profile(profile_path)
        expected_by_relation = expected_columns_by_relation(profile)

        for relation_suffix, expected_columns in sorted(expected_by_relation.items()):
            raw_table = f"{notice_token}_{relation_suffix}"
            staging_model = f"stg_silver__{raw_table}"
            staging_sql = args.staging_dir / notice_token / f"{staging_model}.sql"
            local_raw_sql = args.local_raw_dir / f"local_raw__{raw_table}.sql"

            context = f"{profile_path.name} / {relation_suffix}"

            if not staging_sql.exists():
                failures.append(f"{context}: missing staging SQL {staging_sql}")
                continue

            sql_text = staging_sql.read_text(encoding="utf-8")
            try:
                mappings, selected_source_columns, aliases = extract_staging_select(sql_text)
            except ValueError as exc:
                failures.append(f"{context}: {exc}")
                continue

            missing_mappings = sorted(
                ", ".join(sorted(column_group))
                for column_group in expected_columns
                if not column_group.intersection(mappings)
            )
            if missing_mappings:
                failures.append(
                    f"{context}: profile columns not selected/renamed in staging SQL: "
                    + ", ".join(missing_mappings)
                )

            raw_aliases = sorted(
                alias
                for alias in aliases
                if alias in selected_source_columns or alias.startswith(RAW_ALIAS_PREFIXES)
            )
            if raw_aliases:
                failures.append(
                    f"{context}: staging aliases still look like raw column names: "
                    + ", ".join(raw_aliases)
                )

            referenced_raw_table = extract_raw_relation_name(sql_text)
            if referenced_raw_table != raw_table:
                failures.append(
                    f"{context}: staging model references raw table "
                    f"{referenced_raw_table!r}, expected {raw_table!r}"
                )

            if raw_table not in raw_source_tables:
                failures.append(f"{context}: missing raw_silver source entry for {raw_table}")

            local_model_name = f"local_raw__{raw_table}"
            if local_model_name not in local_models:
                failures.append(f"{context}: missing local raw model YAML entry for {local_model_name}")
            if not local_raw_sql.exists():
                failures.append(f"{context}: missing local raw SQL {local_raw_sql}")

            if args.input == "metadata":
                continue

            try:
                if args.input == "duckdb":
                    if not local_raw_sql.exists():
                        continue
                    physical_columns = parquet_columns_from_local_raw(
                        local_raw_sql,
                        args.local_silver_root,
                        selected_source_columns,
                    )
                else:
                    physical_columns = bigquery_columns(raw_table, args.bigquery_project, args.bigquery_dataset)
            except Exception as exc:  # noqa: BLE001 - report all table/schema access failures
                failures.append(f"{context}: could not inspect {args.input} input table {raw_table}: {exc}")
                continue

            missing_physical_columns = sorted(selected_source_columns - physical_columns)
            if missing_physical_columns:
                failures.append(
                    f"{context}: staging SQL references columns missing from {args.input} input "
                    f"{raw_table}: {', '.join(missing_physical_columns)}"
                )

    return failures


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Validate that lakehouse notice profiles are covered by dbt staging models "
            "and, optionally, by compatible DuckDB/parquet or BigQuery raw inputs."
        )
    )
    parser.add_argument(
        "--input",
        choices=["metadata", "duckdb", "bigquery"],
        default="metadata",
        help=(
            "metadata checks dbt declarations only; duckdb also inspects local parquet; "
            "bigquery also inspects BigQuery raw tables via bq show."
        ),
    )
    parser.add_argument("--notice-schemas-dir", type=Path, default=DEFAULT_NOTICE_SCHEMAS_DIR)
    parser.add_argument("--staging-dir", type=Path, default=DEFAULT_STAGING_DIR)
    parser.add_argument("--local-raw-dir", type=Path, default=DEFAULT_LOCAL_RAW_DIR)
    parser.add_argument("--sources-yml", type=Path, default=DEFAULT_SOURCES_YML)
    parser.add_argument("--local-raw-yml", type=Path, default=DEFAULT_LOCAL_RAW_YML)
    parser.add_argument("--local-silver-root", type=Path, default=DEFAULT_LOCAL_SILVER_ROOT)
    parser.add_argument("--bigquery-project", help="GCP project for --input bigquery.")
    parser.add_argument("--bigquery-dataset", default="silver", help="BigQuery raw Silver dataset.")
    args = parser.parse_args()

    if args.input == "bigquery" and not args.bigquery_project:
        parser.error("--bigquery-project is required when --input bigquery")

    failures = validate(args)
    if failures:
        print("Notice staging validation failed:")
        for failure in failures:
            print(f"- {failure}")
        raise SystemExit(1)

    print(f"Notice staging validation passed for input={args.input}.")


if __name__ == "__main__":
    main()
