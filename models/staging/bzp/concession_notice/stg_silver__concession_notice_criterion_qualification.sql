select
    objectId as cno_qualification_criterion_notice_id,
    'ConcessionNotice' as cno_qualification_criterion_notice_type,
    cast(publicationDateDay as date) as cno_qualification_criterion_publication_date_day,
    criterion_qualification_ordinal as cno_qualification_criterion_ordinal,
    section_6_1_1 as cno_qualification_criterion_type,
    section_6_1_2 as cno_qualification_criterion_name,
    section_6_1_3 as cno_qualification_criterion_minimum_level,
    section_6_1_4 as cno_qualification_criterion_description,
    section_6_1_5 as cno_qualification_criterion_allows_self_declaration,
    section_6_1_6 as cno_qualification_criterion_evidence_requirements
from {{ raw_silver_relation('concession_notice_criterion_qualification') }}
{{ dev_date_window('publicationDateDay') }}
