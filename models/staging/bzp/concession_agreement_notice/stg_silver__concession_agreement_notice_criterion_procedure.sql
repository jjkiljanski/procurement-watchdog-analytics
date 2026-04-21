select
    objectId as can_criterion_notice_id,
    'ConcessionAgreementNotice' as can_criterion_notice_type,
    cast(publicationDateDay as date) as can_criterion_publication_date_day,
    criterion_procedure_ordinal as can_criterion_ordinal,
    section_4_3_2 as can_criterion_type,
    section_4_3_3 as can_criterion_name,
    section_4_3_4 as can_criterion_weight,
    section_4_3_7 as can_criterion_description
from {{ raw_silver_relation('concession_agreement_notice_criterion_procedure') }}
{{ dev_date_window('publicationDateDay') }}
