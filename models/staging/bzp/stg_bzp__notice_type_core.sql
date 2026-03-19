select
    notice_id,
    case_id,
    notice_type,
    publication_date,
    contracting_mode,
    cpv_main_code,
    estimated_value_amount
from {{ source('warehouse_bzp', 'silver_notice_type_core') }}
