{{ config(alias='notice_update_concession_core') }}

select *
from read_parquet(
    '{{ var("local_silver_root") }}/notice_type_tables/noticeType=NoticeUpdateConcession/data_model=core/**/*.parquet',
    hive_partitioning = true,
    union_by_name = true
)
