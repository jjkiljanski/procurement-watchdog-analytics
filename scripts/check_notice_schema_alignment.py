from __future__ import annotations

import argparse
import ast
import json
import re
import sys
from collections import defaultdict
from pathlib import Path


def snake_to_pascal(name: str) -> str:
    return "".join(part.capitalize() for part in re.split(r"[_\.]+", name) if part)


def expected_fields_by_data_model(profile_path: Path) -> dict[str, set[str]]:
    profile = json.loads(profile_path.read_text(encoding="utf-8"))
    expected: dict[str, set[str]] = defaultdict(set)

    for _, section_data in profile.items():
        data_model = section_data["data_model"]
        col_name = section_data["col_name"]
        expected[data_model].add(col_name)

        derived_cols = section_data.get("derived_cols", {})
        for derived_col_name in derived_cols:
            expected[data_model].add(derived_col_name)

    return dict(expected)


def model_fields_by_class(models_path: Path) -> dict[str, set[str]]:
    module = ast.parse(models_path.read_text(encoding="utf-8"))
    class_fields: dict[str, set[str]] = {}

    for node in module.body:
        if not isinstance(node, ast.ClassDef):
            continue

        fields: set[str] = set()
        for class_node in node.body:
            if isinstance(class_node, ast.AnnAssign) and isinstance(class_node.target, ast.Name):
                fields.add(class_node.target.id)

        class_fields[node.name] = fields

    return class_fields


def expected_class_name(models_path: Path, data_model: str) -> str:
    notice_type_token = models_path.stem.removesuffix("_models")
    return f"{snake_to_pascal(notice_type_token)}{snake_to_pascal(data_model)}Model"


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Check that fields implied by a notice profile JSON align with the "
            "corresponding Pydantic models."
        )
    )
    parser.add_argument("profile_json", type=Path, help="Path to *_profile.json")
    parser.add_argument("models_py", type=Path, help="Path to *_models.py")
    args = parser.parse_args()

    expected = expected_fields_by_data_model(args.profile_json)
    actual = model_fields_by_class(args.models_py)

    failures: list[str] = []

    for data_model, expected_fields in sorted(expected.items()):
        class_name = expected_class_name(args.models_py, data_model)
        actual_fields = actual.get(class_name)

        if actual_fields is None:
            failures.append(
                f"Missing model class for data_model='{data_model}': expected {class_name}"
            )
            continue

        missing = sorted(expected_fields - actual_fields)
        extra = sorted(actual_fields - expected_fields)

        if missing:
            failures.append(
                f"{class_name} is missing fields: {', '.join(missing)}"
            )
        if extra:
            failures.append(
                f"{class_name} has fields not defined in profile JSON: {', '.join(extra)}"
            )

    referenced_classes = {expected_class_name(args.models_py, data_model) for data_model in expected}
    unreferenced_classes = sorted(set(actual) - referenced_classes)
    for class_name in unreferenced_classes:
        failures.append(
            f"{class_name} exists in models file but is not referenced by the profile JSON"
        )

    if failures:
        print("Schema alignment check failed:")
        for failure in failures:
            print(f"- {failure}")
        sys.exit(1)

    print("Schema alignment check passed.")


if __name__ == "__main__":
    main()
