# procurement-watchdog-analytics

dbt project for the business-facing Gold layer of Procurement Watchdog.

This repository is intentionally separate from the Spark lakehouse in
`E:\git_projects\procurement-watchdog-lakehouse`.

The current split is:

- `procurement-watchdog-lakehouse`: ingestion and physical medallion pipeline
  (`bronze_raw` -> `bronze` -> `silver`)
- `procurement-watchdog-analytics`: dbt models that define reusable Gold logic
  over warehouse tables/views exposed from the lakehouse outputs

## Design Goals

- keep Gold business logic in SQL and version it independently
- treat the lakehouse `silver` layer as the main dbt input contract
- support `bzp` first without hard-coding the repo around one source forever
- leave room for future sources such as `krs`
- stay small for the first commit

## Expected Upstream Inputs

The lakehouse currently produces these main Silver assets:

- `common_envelope`
- `notice_type_tables`
- `case_derived_facts`

This dbt project assumes those assets are made available in the target
warehouse as tables or views. The exact physical names can differ by adapter
and environment; the source definitions in `models/staging/*/*sources*.yml`
are the place to map them.

## Project Layout

```text
models/
  staging/
    bzp/
    krs/
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

- `staging`: thin source cleanup and naming normalization per upstream system
- `intermediate`: reusable joins and business-ready building blocks
- `marts`: end-user tables for cases, buyers, market views, and signals

The initial scaffold includes only a few starter models. They are placeholders
for the real Gold logic and are meant to be easy to replace as the warehouse
contract stabilizes.

## Getting Started

1. Install dbt and the adapter for your warehouse, for example:

   ```bash
   pip install dbt-core dbt-duckdb
   ```

2. Copy the example profile:

   ```bash
   copy profiles\profiles.yml.example %USERPROFILE%\.dbt\profiles.yml
   ```

3. Adjust the profile and the source table mappings to your environment.

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

## Near-Term Next Steps

- wire the `source()` definitions to real warehouse tables/views
- replace starter marts with production business logic
- add source freshness/tests where the adapter supports it
- add `krs` staging models once the upstream contract exists
