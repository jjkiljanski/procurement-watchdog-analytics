with cases as (
    select * from {{ ref('int_procurement__cases') }}
)

select
    {{ generate_case_key(["buyer_id", "buyer_name"]) }} as buyer_key,
    buyer_id,
    buyer_name,
    count(*) as case_count,
    min(first_publication_date) as first_case_date,
    max(last_publication_date) as last_case_date
from cases
where buyer_id is not null or buyer_name is not null
group by 1, 2, 3
