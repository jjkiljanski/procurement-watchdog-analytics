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

## Getting Started

1. Install dbt and the local adapter:

   ```bash
   pip install dbt-core dbt-duckdb
   ```

2. Copy the example profile:

   ```bash
   copy profiles\profiles.yml.example %USERPROFILE%\.dbt\profiles.yml
   ```

3. Adjust the profile if needed. The default local profile points at a DuckDB
   file and uses the local parquet-backed raw access models.

4. Run:

   ```bash
   dbt debug
   dbt parse
   dbt run
   dbt test
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
