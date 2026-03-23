select
    objectId as cpn_part_notice_id,
    noticeType as cpn_part_notice_type,
    cast(publicationDateDay as date) as cpn_part_publication_date_day,
    part_ordinal as cpn_part_ordinal,
    section_3_8 as cpn_part_short_description,
    section_3_9 as cpn_part_main_cpv_codes,
    section_3_10 as cpn_part_additional_cpv_codes
from {{ raw_silver_relation('contract_performing_notice_part') }}
{{ dev_date_window('publicationDateDay') }}
