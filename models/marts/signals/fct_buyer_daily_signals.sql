with envelope as (
    select * from {{ ref('stg_bzp__common_envelope') }}
),
buyers as (
    select * from {{ ref('mart_buyers') }}
)

select
    buyers.buyer_key,
    envelope.publication_date as signal_date,
    count(distinct envelope.notice_id) as notices_published,
    count(distinct envelope.case_id) as active_cases
from envelope
inner join buyers
    on envelope.buyer_id = buyers.buyer_id
group by 1, 2
