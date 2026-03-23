# procurement-watchdog-analytics

dbt project for the business-facing Gold layer of Procurement Watchdog.

This repository is intentionally separate from the Spark lakehouse in
`E:\git_projects\procurement-watchdog-lakehouse`.

The current split is:

- `procurement-watchdog-lakehouse`: ingestion and physical medallion pipeline
  (`bronze_raw` -> `bronze` -> `silver`)
- `procurement-watchdog-analytics`: dbt models that define reusable Gold logic
  over a canonical `silver` contract

## Design Goals

- keep Gold business logic in SQL and version it independently
- treat the lakehouse `silver` layer as the main dbt input contract
- support `bzp` first without locking the business layer to parquet paths
- leave room for future sources such as `krs`
- stay small for the first commit

## Expected Upstream Inputs

The current canonical input contract for this repo is:

- `common_envelope`
- `contract_notice_core`
- `contract_notice_client`
- `contract_notice_part`

Locally, DuckDB builds these canonical relations from parquet files under:

- `E:\git_projects\procurement-watchdog-api-exploration\data\silver`

In production, BigQuery is expected to expose the same `silver.*` relations
with the same schema and semantics. The business-layer dbt models are written
to swap between those runtimes without changing downstream SQL.

## Project Layout

```text
models/
  platform/
    local_raw/
  staging/
  intermediate/
    procurement/
  marts/
    core/
    signals/
macros/
seeds/
analyses/
snapshots/
profiles/
```

## Modeling Approach

- `platform/local_raw`: DuckDB-only parquet access models with no business
  renaming
- `staging`: platform-independent Silver contract models that define the
  canonical column names, casts, and the first downstream-facing contract
- `intermediate`: reusable joins and business-ready building blocks
- `marts`: end-user tables for cases, buyers, market views, and signals

The initial scaffold includes only a few starter models. They are placeholders
for the real Gold logic and are meant to be easy to replace as the warehouse
contract stabilizes.

For now, the notice-type side is intentionally limited to `ContractNotice`
tables only. This matches the current workflow: start Gold modeling on one
notice family while keeping the repo structure ready to add more notice types
later.

## Local Setup

The local workflow has been checked on Windows with:

- `dbt-core`
- `dbt-duckdb`
- DuckDB profile at `%USERPROFILE%\.dbt\profiles.yml`
- local Silver parquet under
  `E:\git_projects\procurement-watchdog-api-exploration\data\silver`

Recommended setup:

1. Activate the Python/conda environment that should own `dbt`.

2. Install dbt and the DuckDB adapter:

   ```bash
   python -m pip install dbt-core dbt-duckdb
   ```

3. Copy the example profile:

   ```bash
   copy profiles\profiles.yml.example %USERPROFILE%\.dbt\profiles.yml
   ```

4. Validate the setup:

   ```bash
   dbt debug
   dbt parse
   ```

5. Run the static contract check before builds:

   ```bash
   python scripts/validate_notice_contracts.py
   ```

The local profile creates a DuckDB database file in the repo root:

- `procurement_watchdog_analytics.duckdb`

This file stores dbt-created views and tables. The source parquet files remain
external and are read through DuckDB.

## First Local Run

For a narrow first run, build only the raw-access dependencies plus the
ContractNotice/CommonEnvelope staging contract for the first ten days of
October 2025:

```bash
dbt run --select +stg_silver__common_envelope +stg_silver__contract_notice_core +stg_silver__contract_notice_client +stg_silver__contract_notice_part +stg_silver__contract_notice_part_criterion --vars "{dev_date_from: '2025-10-01', dev_date_to: '2025-10-10'}"
```

Notes:

- The leading `+` is important. It includes upstream raw models from
  `models/platform/local_raw`.
- `dev_date_from` and `dev_date_to` are optional development vars that restrict
  the staging contract to a smaller date window for faster local iteration.
- Recommended local sequence:
  - `python scripts/validate_notice_contracts.py`
  - `dbt run --select ...`

## Inspecting Local Outputs

Open the local DuckDB database:

```bash
duckdb procurement_watchdog_analytics.duckdb
```

Then inspect what dbt created:

```sql
select table_schema, table_name
from information_schema.tables
where table_schema in ('silver', 'analytics')
order by 1, 2;
```

Example checks:

```sql
select count(*) from analytics.stg_silver__common_envelope;
select min(publication_date_day), max(publication_date_day)
from analytics.stg_silver__contract_notice_core;
```

## Relationship To The Lakehouse Repo

The lakehouse repo still owns:

- raw ingestion from APIs
- Bronze and Silver transformation logic
- physical partitioning and backfill mechanics
- Spark operational workflows

This repo should own:

- analytical entity definitions
- business metrics and signals
- source-combining logic across `bzp`, `krs`, and future datasets
- dbt documentation and tests around Gold semantics

## Local vs Production Runtime

The contract is documented in `docs/contracts/silver_contract.md`.

Runtime behavior:

- `duckdb` target:
  - dbt reads local parquet from
    `E:\git_projects\procurement-watchdog-api-exploration\data\silver`
  - raw access happens in `models/platform/local_raw`
- `bigquery` target:
  - dbt reads copied raw Silver tables in BigQuery with original upstream
    column names

The canonical renaming and casting logic lives in `models/staging`, so the
business layer does not change when you switch environments.

## Near-Term Next Steps

- replace starter marts with production business logic
- add source freshness/tests where the adapter supports it
- add `krs` once its upstream contract exists

## Notice Schema Utilities

This repo also includes helper scripts for notice-schema maintenance:

```bash
python scripts/generate_all_notice_profile_markdown.py
python scripts/validate_notice_contracts.py
```

See [scripts/README.md](e:/git_projects/procurement-watchdog-analytics/scripts/README.md)
for details.

## Developer Guide

For copy-paste local development commands with dbt and DuckDB, see
[DEV_WORKFLOW.md](e:/git_projects/procurement-watchdog-analytics/docs/DEV_WORKFLOW.md).
