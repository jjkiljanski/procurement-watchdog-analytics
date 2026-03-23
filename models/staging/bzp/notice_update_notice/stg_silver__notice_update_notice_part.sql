select
    objectId as nun_part_notice_id,
    noticeType as nun_part_notice_type,
    cast(publicationDateDay as date) as nun_part_publication_date_day,
    part_ordinal as nun_part_ordinal,
    section_3_4 as nun_updated_notice_section_identifier
from {{ raw_silver_relation('notice_update_notice_part') }}
{{ dev_date_window('publicationDateDay') }}
