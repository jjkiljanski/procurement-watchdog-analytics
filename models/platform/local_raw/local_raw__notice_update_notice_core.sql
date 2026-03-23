{{ config(alias='notice_update_notice_core') }}

select *
from read_parquet(
    '{{ var("local_silver_root") }}/notice_type_tables/noticeType=NoticeUpdateNotice/data_model=core/**/*.parquet',
    hive_partitioning = true,
    union_by_name = true
)
