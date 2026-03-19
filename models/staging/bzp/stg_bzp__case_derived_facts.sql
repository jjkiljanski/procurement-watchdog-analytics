select
    case_id,
    buyer_id,
    buyer_name,
    first_notice_date,
    last_notice_date,
    notice_count,
    winning_supplier_name,
    winning_price_amount,
    winning_price_currency
from {{ source('warehouse_bzp', 'silver_case_derived_facts') }}
