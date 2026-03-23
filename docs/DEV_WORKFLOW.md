# Dev Workflow

Copy-paste oriented notes for local development with dbt and DuckDB on
Windows.

## Assumptions

- repo root:
  - `E:\git_projects\procurement-watchdog-analytics`
- local Silver parquet:
  - `E:\git_projects\procurement-watchdog-api-exploration\data\silver`
- dbt profile:
  - `%USERPROFILE%\.dbt\profiles.yml`

## Enter The Repo

```powershell
cd E:\git_projects\procurement-watchdog-analytics
```

## Activate Your Python Environment

If you use conda:

```powershell
conda activate procurement-dbt
```

Check what will be used:

```powershell
Get-Command python
Get-Command dbt
```

## Install / Upgrade dbt

```powershell
python -m pip install --upgrade pip
python -m pip install dbt-core dbt-duckdb
```

## Copy The Example Profile

```powershell
New-Item -ItemType Directory -Force $HOME\.dbt
Copy-Item profiles\profiles.yml.example $HOME\.dbt\profiles.yml
```

## Validate The Setup

```powershell
dbt debug
dbt parse
python scripts/validate_notice_contracts.py
```

## First Narrow Run

Build only the local raw access dependencies plus the current staging contract
for `common_envelope` and `ContractNotice`, restricted to 2025-10-01 through
2025-10-10:

```powershell
dbt run --select +stg_silver__common_envelope +stg_silver__contract_notice_core +stg_silver__contract_notice_client +stg_silver__contract_notice_part +stg_silver__contract_notice_part_criterion --vars "{dev_date_from: '2025-10-01', dev_date_to: '2025-10-10'}"
```

Why the leading `+` matters:

- it includes upstream models from `models/platform/local_raw`

## Rebuild Only One Model

```powershell
dbt run --select +stg_silver__contract_notice_core --vars "{dev_date_from: '2025-10-01', dev_date_to: '2025-10-10'}"
```

## Run Tests For One Model

```powershell
dbt test --select stg_silver__contract_notice_core --vars "{dev_date_from: '2025-10-01', dev_date_to: '2025-10-10'}"
```

## Build Downstream Models Too

```powershell
dbt run --select +stg_silver__contract_notice_core+ --vars "{dev_date_from: '2025-10-01', dev_date_to: '2025-10-10'}"
```

The left `+` includes parents. The right `+` includes children.

## Run All Current Local Models

```powershell
dbt run --vars "{dev_date_from: '2025-10-01', dev_date_to: '2025-10-10'}"
```

## Open DuckDB

The local profile writes into:

- `procurement_watchdog_analytics.duckdb`

Open it:

```powershell
duckdb procurement_watchdog_analytics.duckdb
```

## Inspect What dbt Created

```sql
select table_schema, table_name
from information_schema.tables
where table_schema in ('silver', 'analytics')
order by 1, 2;
```

```sql
select table_schema, table_name
from information_schema.views
where table_schema in ('silver', 'analytics')
order by 1, 2;
```

## Quick Sanity Checks

```sql
select count(*) from analytics.stg_silver__common_envelope;
select count(*) from analytics.stg_silver__contract_notice_core;
select count(*) from analytics.stg_silver__contract_notice_client;
select count(*) from analytics.stg_silver__contract_notice_part;
select count(*) from analytics.stg_silver__contract_notice_part_criterion;
```

```sql
select min(cn_publication_date_day), max(cn_publication_date_day)
from analytics.stg_silver__contract_notice_core;
```

```sql
select cn_notice_subject, count(*)
from analytics.stg_silver__contract_notice_core
group by 1
order by 2 desc;
```

```sql
select *
from analytics.stg_silver__contract_notice_core
limit 20;
```

## Regenerate Notice Docs

```powershell
python scripts/generate_all_notice_profile_markdown.py
```

## Re-run The Static Contract Check

```powershell
python scripts/validate_notice_contracts.py
```

## Useful Cleanup

Remove dbt build artifacts:

```powershell
dbt clean
```

Remove the local DuckDB database file if you want to rebuild from scratch:

```powershell
Remove-Item .\procurement_watchdog_analytics.duckdb
```

## Typical Local Loop

```powershell
python scripts/validate_notice_contracts.py
dbt run --select +stg_silver__contract_notice_core --vars "{dev_date_from: '2025-10-01', dev_date_to: '2025-10-10'}"
dbt test --select stg_silver__contract_notice_core --vars "{dev_date_from: '2025-10-01', dev_date_to: '2025-10-10'}"
duckdb procurement_watchdog_analytics.duckdb
```
