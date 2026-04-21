{{ config(alias='notice_update_concession_part') }}

select *
from read_parquet(
    '{{ var("local_silver_root") }}/notice_type_tables/noticeType=NoticeUpdateConcession/data_model=part/**/*.parquet',
    hive_partitioning = true,
    union_by_name = true
)
