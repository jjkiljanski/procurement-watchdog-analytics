# Silver Input Contract

The dbt business layer reads from a canonical Silver contract regardless of
runtime adapter.

## Layering

- platform layer:
  - DuckDB reads parquet
  - BigQuery reads copied raw tables
  - no canonical renames live here
- staging layer:
  - defines canonical column names and portable casts
  - this is the single source of truth for semantic column mapping
  - is also the first downstream-facing Silver contract
- business layer:
  - intermediate, marts

## Canonical Relations

### `silver.common_envelope`

One row per notice envelope copied from the upstream Silver layer.

Required columns for the current scaffold:

- `notice_id`
- `case_id`
- `notice_type`
- `publication_date`
- `publication_date_day`
- `tender_id`
- `object_id`
- `buyer_id`
- `buyer_name`
- `client_type_name`
- `province_name`
- `notice_stage`

### `silver.contract_notice_core`

One row per notice from:

- `notice_type_tables/noticeType=ContractNotice/data_model=core`

Required normalized columns:

- `notice_id`
- `notice_type`
- `publication_date_day`

All original `section_*` columns should also be preserved.

### `silver.contract_notice_client`

One row per client row from:

- `notice_type_tables/noticeType=ContractNotice/data_model=client`

Required normalized columns:

- `notice_id`
- `notice_type`
- `publication_date_day`

All original `section_*` columns should also be preserved.

### `silver.contract_notice_part`

One row per part row from:

- `notice_type_tables/noticeType=ContractNotice/data_model=part`

Required normalized columns:

- `notice_id`
- `notice_type`
- `publication_date_day`

All original `section_*` columns should also be preserved.

## Runtime Rule

- Local DuckDB: dbt reads raw parquet through platform models.
- Production BigQuery: dbt reads copied raw Silver tables with the original
  upstream column names.
- In both runtimes, the canonical Silver contract is defined by shared staging
  models, not by the platform access layer.

Downstream business models must not reference parquet paths or warehouse-native
table names directly.
