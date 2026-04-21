{{ config(alias='agreement_intention_notice_client') }}

select *
from read_parquet(
    '{{ var("local_silver_root") }}/notice_type_tables/noticeType=AgreementIntentionNotice/data_model=client/**/*.parquet',
    hive_partitioning = true,
    union_by_name = true
)
