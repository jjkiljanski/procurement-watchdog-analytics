with envelope as (
    select * from {{ ref('stg_silver__common_envelope') }}
),
contract_notice_core as (
    select * from {{ ref('stg_silver__contract_notice_core') }}
)

select
    {{ generate_case_key(["envelope.case_id", "envelope.buyer_id"]) }} as case_key,
    envelope.case_id,
    envelope.buyer_id,
    max(envelope.buyer_name) as buyer_name,
    min(envelope.publication_date) as first_publication_date,
    max(envelope.publication_date) as last_publication_date,
    count(distinct envelope.notice_id) as notice_count,
    count(distinct contract_notice_core.notice_id) as contract_notice_core_count,
    count(distinct envelope.notice_type) as notice_type_count
from envelope
left join contract_notice_core
    on envelope.notice_id = contract_notice_core.notice_id
where envelope.case_id is not null
group by 1, 2, 3
