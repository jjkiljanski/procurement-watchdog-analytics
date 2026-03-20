{{ config(alias='common_envelope') }}

select *
from read_parquet(
    '{{ var("local_silver_root") }}/common_envelope/**/*.parquet',
    hive_partitioning = true,
    union_by_name = true
)
