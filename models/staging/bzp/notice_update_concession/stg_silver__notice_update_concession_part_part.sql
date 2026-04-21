select
    objectId as nuc_part_part_notice_id,
    'NoticeUpdateConcession' as nuc_part_part_notice_type,
    cast(publicationDateDay as date) as nuc_part_part_publication_date_day,
    part_ordinal as nuc_part_part_ordinal,
    part_part_ordinal as nuc_part_part_subitem_ordinal,
    section_3_4_1_label as nuc_updated_notice_change_label,
    section_3_4_1_before as nuc_updated_notice_change_before,
    section_3_4_1_after as nuc_updated_notice_change_after
from {{ raw_silver_relation('notice_update_concession_part_part') }}
{{ dev_date_window('publicationDateDay') }}
