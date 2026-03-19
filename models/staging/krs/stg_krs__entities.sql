select
    entity_id,
    entity_name,
    tax_id,
    national_court_register_number
from {{ source('warehouse_krs', 'silver_entities') }}
