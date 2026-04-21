select
    objectId as nuc_part_notice_id,
    'NoticeUpdateConcession' as nuc_part_notice_type,
    cast(publicationDateDay as date) as nuc_part_publication_date_day,
    part_ordinal as nuc_part_ordinal,
    section_4_1 as nuc_updated_notice_section_identifier
from {{ raw_silver_relation('notice_update_concession_part') }}
{{ dev_date_window('publicationDateDay') }}
