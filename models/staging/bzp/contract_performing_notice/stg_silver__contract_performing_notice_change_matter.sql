select
    objectId as cpn_change_notice_id,
    noticeType as cpn_change_notice_type,
    cast(publicationDateDay as date) as cpn_change_publication_date_day,
    change_matter_ordinal as cpn_change_ordinal,
    section_5_4_2 as cpn_change_number,
    section_5_4_3 as cpn_change_legal_basis,
    section_5_4_4 as cpn_change_reason,
    section_5_4_5 as cpn_change_contract_description_after_change,
    section_5_4_6 as cpn_change_value_amount,
    section_5_4_7 as cpn_change_value_currency,
    section_5_4_8 as cpn_change_increased_contract_price
from {{ raw_silver_relation('contract_performing_notice_change_matter') }}
{{ dev_date_window('publicationDateDay') }}
