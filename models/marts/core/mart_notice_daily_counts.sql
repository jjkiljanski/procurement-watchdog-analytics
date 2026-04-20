with notices as (
    select * from {{ ref('stg_silver__common_envelope') }}
)

select
    publication_date_day,
    count(*) as total_notice_count
from notices
group by 1
