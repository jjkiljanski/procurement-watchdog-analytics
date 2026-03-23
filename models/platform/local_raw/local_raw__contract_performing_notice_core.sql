{{ config(alias='contract_performing_notice_core') }}

select *
from read_parquet(
    '{{ var("local_silver_root") }}/notice_type_tables/noticeType=ContractPerformingNotice/data_model=core/**/*.parquet',
    hive_partitioning = true,
    union_by_name = true
)
