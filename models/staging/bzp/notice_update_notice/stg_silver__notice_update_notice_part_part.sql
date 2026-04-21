select
    objectId as nun_part_part_notice_id,
    'NoticeUpdateNotice' as nun_part_part_notice_type,
    cast(publicationDateDay as date) as nun_part_part_publication_date_day,
    part_ordinal as nun_part_part_ordinal,
    part_part_ordinal as nun_part_part_subitem_ordinal,
    section_3_4_1_label as nun_updated_notice_change_label,
    section_3_4_1_before as nun_updated_notice_change_before,
    section_3_4_1_after as nun_updated_notice_change_after
from {{ raw_silver_relation('notice_update_notice_part_part') }}
{{ dev_date_window('publicationDateDay') }}
