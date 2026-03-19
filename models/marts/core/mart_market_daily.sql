select
    publication_date,
    count(distinct notice_id) as notice_count,
    count(distinct case_id) as case_count,
    count(distinct buyer_id) as buyer_count
from {{ ref('stg_bzp__common_envelope') }}
group by 1
