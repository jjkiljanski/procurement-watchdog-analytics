{{ config(alias='concession_update_agreement_notice_core') }}

select *
from read_parquet(
    '{{ var("local_silver_root") }}/notice_type_tables/noticeType=ConcessionUpdateAgreementNotice/data_model=core/**/*.parquet',
    hive_partitioning = true,
    union_by_name = true
)
