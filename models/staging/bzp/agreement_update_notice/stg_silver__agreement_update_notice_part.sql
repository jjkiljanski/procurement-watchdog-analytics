select
    objectId as aun_part_notice_id,
    'AgreementUpdateNotice' as aun_part_notice_type,
    cast(publicationDateDay as date) as aun_part_publication_date_day,
    part_ordinal as aun_part_ordinal,
    section_3_7 as aun_part_short_description,
    {{ optional_raw_column('section_3_8') }} as aun_part_main_cpv_codes,
    {{ optional_raw_column('section_3_9') }} as aun_part_additional_cpv_codes
from {{ raw_silver_relation('agreement_update_notice_part') }}
{{ dev_date_window('publicationDateDay') }}
