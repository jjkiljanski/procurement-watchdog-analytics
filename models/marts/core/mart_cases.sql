select
    case_key,
    case_id,
    buyer_id,
    buyer_name,
    first_publication_date,
    last_publication_date,
    notice_count,
    contract_notice_core_count,
    notice_type_count
from {{ ref('int_procurement__cases') }}
