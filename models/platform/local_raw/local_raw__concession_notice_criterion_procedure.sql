{{ config(alias='concession_notice_criterion_procedure') }}

select *
from read_parquet(
    '{{ var("local_silver_root") }}/notice_type_tables/noticeType=ConcessionNotice/data_model=criterion_procedure/**/*.parquet',
    hive_partitioning = true,
    union_by_name = true
)
