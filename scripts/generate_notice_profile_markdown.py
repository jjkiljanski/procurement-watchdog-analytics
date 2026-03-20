from __future__ import annotations

import argparse
import json
from collections.abc import Iterable
from pathlib import Path


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
    args = parser.parse_args()

    profile = json.loads(args.profile_json.read_text(encoding="utf-8"))
    markdown = render_markdown(profile)

    args.output_md.parent.mkdir(parents=True, exist_ok=True)
    args.output_md.write_text(markdown, encoding="utf-8")


if __name__ == "__main__":
    main()
