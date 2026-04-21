# Scripts

Utilities for keeping the analytics repo aligned with the lakehouse notice
schemas.

## Generate Notice Docs

Generate markdown catalogs for all notice profile JSON files:

```bash
python scripts/generate_all_notice_profile_markdown.py
```

This reads all `*_profile*.json` files from the lakehouse notice schema
directory and writes markdown catalogs to:

- `docs/notice_profiles/`

The generated markdown is intentionally derived only from JSON content, plus a
short note that value constraints are documented separately at the column
level.

## Validate Notice Contracts

Check that each notice profile JSON is aligned with its corresponding
`*_models.py` Pydantic file:

```bash
python scripts/validate_notice_contracts.py
```

The check is static and contract-focused:

- it compares profile-defined raw and derived columns with model fields
- it fails on missing fields
- it fails on extra fields
- it fails when the expected Pydantic model class is missing

## Validate Notice Staging

Check that lakehouse notice profiles are fully represented in dbt staging and,
optionally, that the raw input tables are compatible with the staging SQL:

```bash
python scripts/validate_notice_staging.py --input metadata
python scripts/validate_notice_staging.py --input duckdb
python scripts/validate_notice_staging.py --input bigquery --bigquery-project YOUR_PROJECT --bigquery-dataset silver
```

The check is analytics-layer focused:

- it verifies every notice profile/data-model has a matching staging SQL model
- it verifies every profile-defined raw or derived field is explicitly mapped
  to a renamed business column in staging SQL
- it verifies the raw table is registered in `raw_silver` sources
- it verifies the matching `local_raw__*` DuckDB model and YAML entry exist
- with `--input duckdb`, it inspects local parquet schemas
- with `--input bigquery`, it inspects BigQuery table schemas via `bq show`

Recommended usage:

- run before `dbt run` / `dbt build`
- run in CI once the repo gets a CI workflow

## Path Assumption

By default, these scripts read lakehouse notice schemas from:

- `E:\git_projects\procurement-watchdog-lakehouse\src\procurement\silver\notice_schemas`

You can override that with `--notice-schemas-dir` if needed.
