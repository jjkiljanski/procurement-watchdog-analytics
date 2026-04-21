{{ config(alias='circumstances_fulfillment_notice_core') }}

select *
from read_parquet(
    '{{ var("local_silver_root") }}/notice_type_tables/noticeType=CircumstancesFulfillmentNotice/data_model=core/**/*.parquet',
    hive_partitioning = true,
    union_by_name = true
)
