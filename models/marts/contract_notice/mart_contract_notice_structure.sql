with envelope as (
    select * from {{ ref('stg_silver__common_envelope') }}
),
core as (
    select * from {{ ref('stg_silver__contract_notice_core') }}
),
client as (
    select * from {{ ref('stg_silver__contract_notice_client') }}
),
parts as (
    select * from {{ ref('stg_silver__contract_notice_part') }}
),
criteria as (
    select * from {{ ref('stg_silver__contract_notice_part_criterion') }}
),
part_criteria_counts as (
    select * from {{ ref('int_procurement__contract_notice_part_criteria_counts') }}
),
buyer_location as (
    select
        cn_client_notice_id as notice_id,
        min(cn_client_nuts3_code) as buyer_nuts3_code,
        min(cn_client_nuts3_name) as buyer_nuts3_name
    from client
    group by 1
),
part_flags as (
    select
        cn_part_notice_id as notice_id,
        max(case when cn_part_has_options then 1 else 0 end) = 1 as cn_part_has_options,
        max(case when cn_part_has_renewals then 1 else 0 end) = 1 as cn_part_has_renewals,
        min(cn_part_duration_days) as cn_part_duration_days_min,
        max(cn_part_duration_days) as cn_part_duration_days_max
    from parts
    group by 1
),
price_criterion_by_part as (
    select
        cn_part_criterion_notice_id as notice_id,
        cn_part_criterion_part_ordinal as part_ordinal,
        max(
            case
                when lower(trim(cn_part_criterion_name)) = 'cena'
                    then cn_part_criterion_weight
            end
        ) as price_criterion_weight
    from criteria
    group by 1, 2
),
price_criterion_stats as (
    select
        notice_id,
        min(price_criterion_weight) as cn_part_price_criterion_weight_min,
        max(price_criterion_weight) as cn_part_price_criterion_weight_max
    from price_criterion_by_part
    group by 1
),
criteria_count_stats as (
    select
        cn_part_notice_id as notice_id,
        min(part_criterion_count) as cn_part_criteria_count_min,
        max(part_criterion_count) as cn_part_criteria_count_max
    from part_criteria_counts
    group by 1
)

select
    envelope.notice_id,
    envelope.tender_id,
    envelope.buyer_name,
    envelope.province_name as buyer_province_name,
    buyer_location.buyer_nuts3_code,
    buyer_location.buyer_nuts3_name,
    envelope.publication_date,
    core.cn_allows_partial_offers,
    core.cn_number_of_lots,
    core.cn_limits_lots_per_bidder,
    part_flags.cn_part_has_options,
    part_flags.cn_part_has_renewals,
    part_flags.cn_part_duration_days_min,
    part_flags.cn_part_duration_days_max,
    core.cn_has_optional_exclusion_grounds,
    core.cn_optional_exclusion_grounds,
    core.cn_participation_conditions_description,
    core.cn_submission_languages,
    core.cn_request_to_participate_deadline,
    core.cn_allows_variant_offers,
    core.cn_has_restricted_procurement_documents,
    core.cn_may_cancel_if_funding_missing,
    core.cn_allows_contract_changes,
    core.cn_contract_change_terms,
    core.cn_has_advance_payments,
    core.cn_has_electronic_auction,
    price_criterion_stats.cn_part_price_criterion_weight_min,
    price_criterion_stats.cn_part_price_criterion_weight_max,
    criteria_count_stats.cn_part_criteria_count_min,
    criteria_count_stats.cn_part_criteria_count_max,
    core.cn_has_social_environmental_label_requirements,
    core.cn_social_environmental_label_requirements_description
from envelope
inner join core
    on envelope.notice_id = core.cn_core_notice_id
left join buyer_location
    on envelope.notice_id = buyer_location.notice_id
left join part_flags
    on envelope.notice_id = part_flags.notice_id
left join price_criterion_stats
    on envelope.notice_id = price_criterion_stats.notice_id
left join criteria_count_stats
    on envelope.notice_id = criteria_count_stats.notice_id
where envelope.notice_type = 'ContractNotice'
