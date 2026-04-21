{{ config(alias='concession_agreement_notice_criterion_procedure') }}

select *
from read_parquet(
    '{{ var("local_silver_root") }}/notice_type_tables/noticeType=ConcessionAgreementNotice/data_model=criterion_procedure/**/*.parquet',
    hive_partitioning = true,
    union_by_name = true
)
