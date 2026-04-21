select
    objectId as cno_procedure_criterion_notice_id,
    'ConcessionNotice' as cno_procedure_criterion_notice_type,
    cast(publicationDateDay as date) as cno_procedure_criterion_publication_date_day,
    criterion_procedure_ordinal as cno_procedure_criterion_ordinal,
    section_5_13_2 as cno_procedure_criterion_type,
    section_5_13_3 as cno_procedure_criterion_name,
    section_5_13_4 as cno_procedure_criterion_weight,
    section_5_13_6 as cno_procedure_criterion_order,
    section_5_13_7 as cno_procedure_criterion_description
from {{ raw_silver_relation('concession_notice_criterion_procedure') }}
{{ dev_date_window('publicationDateDay') }}
