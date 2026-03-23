{{ config(alias='contract_notice_part_criterion') }}

select *
from read_parquet(
    '{{ var("local_silver_root") }}/notice_type_tables/noticeType=ContractNotice/data_model=part_criterion/**/*.parquet',
    hive_partitioning = true,
    union_by_name = true
)
