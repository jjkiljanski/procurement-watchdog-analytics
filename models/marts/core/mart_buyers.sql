select
    buyer_key,
    buyer_id,
    buyer_name,
    case_count,
    first_case_date,
    last_case_date
from {{ ref('int_procurement__buyers') }}
