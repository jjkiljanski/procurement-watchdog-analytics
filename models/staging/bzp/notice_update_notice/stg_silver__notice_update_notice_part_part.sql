select
    objectId as nun_part_part_notice_id,
    noticeType as nun_part_part_notice_type,
    cast(publicationDateDay as date) as nun_part_part_publication_date_day,
    part_ordinal as nun_part_part_ordinal,
    part_part_ordinal as nun_part_part_subitem_ordinal,
    section_3_4_1 as nun_updated_notice_change_description
from {{ raw_silver_relation('notice_update_notice_part_part') }}
{{ dev_date_window('publicationDateDay') }}
