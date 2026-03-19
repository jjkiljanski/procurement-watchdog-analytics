select
    case_key,
    case_id,
    buyer_id,
    buyer_name,
    first_publication_date,
    last_publication_date,
    notice_count,
    winning_supplier_name,
    winning_price_amount,
    winning_price_currency
from {{ ref('int_procurement__cases') }}
