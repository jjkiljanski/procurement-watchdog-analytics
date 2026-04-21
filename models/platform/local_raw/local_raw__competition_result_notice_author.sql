{{ config(alias='competition_result_notice_author') }}

select *
from read_parquet(
    '{{ var("local_silver_root") }}/notice_type_tables/noticeType=CompetitionResultNotice/data_model=author/**/*.parquet',
    hive_partitioning = true,
    union_by_name = true
)
