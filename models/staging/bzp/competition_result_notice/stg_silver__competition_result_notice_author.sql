select
    objectId as crn_author_notice_id,
    'CompetitionResultNotice' as crn_author_notice_type,
    cast(publicationDateDay as date) as crn_author_publication_date_day,
    author_ordinal as crn_author_ordinal,
    section_5_7_1 as crn_author_name,
    section_5_7_2 as crn_author_street,
    section_5_7_3 as crn_author_city,
    section_5_7_4 as crn_author_postal_code,
    section_5_7_5 as crn_author_province,
    section_5_7_6 as crn_author_country,
    section_5_7_7_value as crn_author_national_id,
    section_5_7_7_type as crn_author_national_id_type,
    section_5_8 as crn_author_award_place,
    section_5_9 as crn_author_prize_type,
    section_5_10_value as crn_author_prize_value_amount,
    section_5_10_currency as crn_author_prize_value_currency
from {{ raw_silver_relation('competition_result_notice_author') }}
{{ dev_date_window('publicationDateDay') }}
