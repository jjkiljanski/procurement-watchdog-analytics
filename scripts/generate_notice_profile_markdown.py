from __future__ import annotations

import argparse
import json
import re
from collections.abc import Iterable
from pathlib import Path


SECTION_COLUMN_PATTERN = re.compile(r"\bsection_\d+(?:_\d+)*(?:_[A-Za-z0-9]+)?\b")
ALIAS_PATTERN = re.compile(r"\bas\s+([A-Za-z_][A-Za-z0-9_]*)\s*$", re.IGNORECASE | re.DOTALL)


def _format_scalar(value: object) -> str:
    if isinstance(value, str):
        return f"`{value}`"
    if isinstance(value, bool):
        return "`true`" if value else "`false`"
    if value is None:
        return "`null`"
    return f"`{value}`"


def _render_mapping_lines(mapping: dict[str, object], indent: str = "") -> list[str]:
    lines: list[str] = []
    for key, value in mapping.items():
        if isinstance(value, dict):
            lines.append(f"{indent}- `{key}`:")
            lines.extend(_render_mapping_lines(value, indent=indent + "  "))
        elif isinstance(value, list):
            lines.append(f"{indent}- `{key}`:")
            lines.extend(_render_list_lines(value, indent=indent + "  "))
        else:
            lines.append(f"{indent}- `{key}`: {_format_scalar(value)}")
    return lines


def _render_list_lines(values: Iterable[object], indent: str = "") -> list[str]:
    lines: list[str] = []
    for value in values:
        if isinstance(value, dict):
            lines.append(f"{indent}-")
            lines.extend(_render_mapping_lines(value, indent=indent + "  "))
        elif isinstance(value, list):
            lines.append(f"{indent}-")
            lines.extend(_render_list_lines(value, indent=indent + "  "))
        else:
            lines.append(f"{indent}- {_format_scalar(value)}")
    return lines


def _render_value_lines(value: object, indent: str = "") -> list[str]:
    if isinstance(value, dict):
        return _render_mapping_lines(value, indent=indent)
    if isinstance(value, list):
        return _render_list_lines(value, indent=indent)
    return [f"{indent}- {_format_scalar(value)}"]


def notice_token_from_profile_path(profile_path: Path) -> str:
    return (
        profile_path.name.replace("_profile_automatic.json", "").replace("_profile.json", "")
    )


def profile_column_to_section_map(profile: dict[str, object]) -> dict[str, str]:
    column_map: dict[str, str] = {}
    for section_id, section_data in profile.items():
        if isinstance(section_data, dict):
            col_name = section_data.get("col_name")
            if isinstance(col_name, str):
                column_map[col_name] = section_id
            derived_cols = section_data.get("derived_cols", {})
            if isinstance(derived_cols, dict):
                for derived_col_name in derived_cols:
                    column_map[derived_col_name] = section_id
    return column_map


def split_select_items(sql_text: str) -> list[str]:
    match = re.search(r"\bselect\b(.*?)\bfrom\b", sql_text, re.IGNORECASE | re.DOTALL)
    if not match:
        return []

    body = match.group(1)
    items: list[str] = []
    current: list[str] = []
    depth = 0
    in_single_quote = False

    for char in body:
        if char == "'" and (not current or current[-1] != "\\"):
            in_single_quote = not in_single_quote
        elif not in_single_quote:
            if char == "(":
                depth += 1
            elif char == ")":
                depth = max(0, depth - 1)
            elif char == "," and depth == 0:
                item = "".join(current).strip()
                if item:
                    items.append(item)
                current = []
                continue
        current.append(char)

    tail = "".join(current).strip()
    if tail:
        items.append(tail)

    return items


def extract_staging_mappings(sql_text: str) -> dict[str, list[str]]:
    mappings: dict[str, list[str]] = {}
    for item in split_select_items(sql_text):
        alias_match = ALIAS_PATTERN.search(item)
        if not alias_match:
            continue

        alias = alias_match.group(1)
        referenced_columns = SECTION_COLUMN_PATTERN.findall(item)
        for column_name in referenced_columns:
            mappings.setdefault(column_name, [])
            if alias not in mappings[column_name]:
                mappings[column_name].append(alias)

    return mappings


def enrich_profile_with_staging_mappings(
    profile: dict[str, object],
    profile_path: Path,
    staging_dir: Path,
) -> dict[str, object]:
    enriched = json.loads(json.dumps(profile))
    notice_token = notice_token_from_profile_path(profile_path)
    column_to_section = profile_column_to_section_map(enriched)

    for staging_path in sorted(staging_dir.rglob(f"stg_silver__{notice_token}_*.sql")):
        mappings = extract_staging_mappings(staging_path.read_text(encoding="utf-8"))
        for raw_column, aliases in mappings.items():
            section_id = column_to_section.get(raw_column)
            if section_id is None:
                continue
            section_data = enriched.get(section_id)
            if not isinstance(section_data, dict):
                continue
            section_data.setdefault("staging_columns", [])
            for alias in aliases:
                if alias not in section_data["staging_columns"]:
                    section_data["staging_columns"].append(alias)

    for section_data in enriched.values():
        if isinstance(section_data, dict) and "staging_columns" in section_data:
            section_data["staging_columns"] = sorted(section_data["staging_columns"])

    return enriched


def render_markdown(profile: dict[str, dict[str, object]]) -> str:
    lines: list[str] = [
        "Specific column-level value constraints are defined separately at the",
        "column level and described in the column-level documentation.",
        "",
    ]
    for section_id, section_data in profile.items():
        lines.append(f"## {section_id}")
        lines.extend(_render_value_lines(section_data))
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Render a markdown catalog directly from a notice profile JSON."
    )
    parser.add_argument("profile_json", type=Path, help="Path to *_profile.json")
    parser.add_argument("output_md", type=Path, help="Output markdown path")
    parser.add_argument(
        "--staging-dir",
        type=Path,
        default=Path("models/staging"),
        help="Directory containing dbt staging SQL models.",
    )
    args = parser.parse_args()

    profile = json.loads(args.profile_json.read_text(encoding="utf-8"))
    profile = enrich_profile_with_staging_mappings(profile, args.profile_json, args.staging_dir)
    markdown = render_markdown(profile)

    args.output_md.parent.mkdir(parents=True, exist_ok=True)
    args.output_md.write_text(markdown, encoding="utf-8")


if __name__ == "__main__":
    main()
