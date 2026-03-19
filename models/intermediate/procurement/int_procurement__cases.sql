with envelope as (
    select * from {{ ref('stg_bzp__common_envelope') }}
),
case_facts as (
    select * from {{ ref('stg_bzp__case_derived_facts') }}
)

select
    {{ generate_case_key(["coalesce(case_facts.case_id, envelope.case_id)", "coalesce(case_facts.buyer_id, envelope.buyer_id)"]) }} as case_key,
    coalesce(case_facts.case_id, envelope.case_id) as case_id,
    coalesce(case_facts.buyer_id, envelope.buyer_id) as buyer_id,
    coalesce(case_facts.buyer_name, envelope.buyer_name) as buyer_name,
    min(envelope.publication_date) as first_publication_date,
    max(envelope.publication_date) as last_publication_date,
    count(distinct envelope.notice_id) as notice_count,
    max(case_facts.winning_supplier_name) as winning_supplier_name,
    max(case_facts.winning_price_amount) as winning_price_amount,
    max(case_facts.winning_price_currency) as winning_price_currency
from envelope
left join case_facts
    on envelope.case_id = case_facts.case_id
group by 1, 2, 3, 4
