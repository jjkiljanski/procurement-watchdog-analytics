select
    objectId as trn_core_notice_id,
    noticeType as trn_core_notice_type,
    cast(publicationDateDay as date) as trn_core_publication_date_day,
    case
        when section_1_1 = 'Postępowanie prowadzone jest samodzielnie przez zamawiającego' then 'samodzielnie'
        when section_1_1 = 'Postępowanie prowadzi zamawiający centralny' then 'centralny'
        when section_1_1 = 'Postępowanie prowadzi podmiot, któremu powierzono przeprowadzenie postępowania' then 'powierzono'
        else null
    end as trn_procedure_conduct_mode,
    section_1_6 as trn_procedure_website_url,
    section_1_7 as trn_buyer_type,
    section_1_8 as trn_buyer_main_activity,
    section_2_1 as trn_notice_subject,
    section_2_2 as trn_is_social_service_notice,
    section_2_3 as trn_contract_title,
    section_2_4 as trn_procedure_ocid,
    section_2_5 as trn_notice_number,
    section_2_6 as trn_notice_version,
    section_2_7 as trn_notice_date,
    section_2_8 as trn_is_in_procurement_plan,
    section_2_9 as trn_procurement_plan_number,
    section_2_10 as trn_procurement_plan_item_identifier,
    section_2_11 as trn_is_eu_funded,
    section_2_12 as trn_eu_funding_program_name,
    section_2_13 as trn_was_preceded_by_prior_notice,
    section_2_14 as trn_prior_notice_number,
    section_3_1 as trn_award_procedure_legal_basis,
    section_3_1_1 as trn_non_competitive_procedure_justification,
    section_3_1_2 as trn_prior_procedure_ocid,
    section_4_1 as trn_reference_number,
    section_4_2 as trn_is_split_into_separate_lots,
    section_4_3 as trn_total_contract_value_amount,
    section_4_3_currency as trn_total_contract_value_currency,
    section_4_3_1 as trn_current_procedure_value_amount,
    section_4_3_1_currency as trn_current_procedure_value_currency,
    section_4_3_2 as trn_framework_agreement_max_value_amount,
    section_4_4 as trn_contract_type
from {{ raw_silver_relation('tender_result_notice_core') }}
{{ dev_date_window('publicationDateDay') }}
