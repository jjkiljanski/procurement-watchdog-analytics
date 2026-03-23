select
    objectId as cn_part_criterion_notice_id,
    noticeType as cn_part_criterion_notice_type,
    cast(publicationDateDay as date) as cn_part_criterion_publication_date_day,
    part_ordinal as cn_part_criterion_part_ordinal,
    part_criterion_ordinal as cn_part_criterion_ordinal,
    section_4_3_4 as cn_part_criterion_type,
    section_4_3_5 as cn_part_criterion_name,
    section_4_3_6 as cn_part_criterion_weight,
    section_4_3_7 as cn_part_criterion_order
from {{ raw_silver_relation('contract_notice_part_criterion') }}
{{ dev_date_window('publicationDateDay') }}
