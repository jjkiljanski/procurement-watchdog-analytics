select
    objectId as ain_part_notice_id,
    'AgreementIntentionNotice' as ain_part_notice_type,
    cast(publicationDateDay as date) as ain_part_publication_date_day,
    part_ordinal as ain_part_ordinal,
    section_3_8 as ain_part_short_description,
    section_3_9 as ain_part_value_amount,
    section_3_10 as ain_part_main_cpv_codes,
    section_3_11 as ain_part_additional_cpv_codes,
    section_5_1_1 as ain_part_intended_supplier_name,
    section_5_1_2 as ain_part_intended_supplier_street,
    section_5_1_3 as ain_part_intended_supplier_city,
    section_5_1_4 as ain_part_intended_supplier_postal_code,
    section_5_1_5 as ain_part_intended_supplier_province,
    section_5_1_6 as ain_part_intended_supplier_country
from {{ raw_silver_relation('agreement_intention_notice_part') }}
{{ dev_date_window('publicationDateDay') }}
