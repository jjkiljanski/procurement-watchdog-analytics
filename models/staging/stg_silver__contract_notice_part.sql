select
    objectId as notice_id,
    noticeType as notice_type,
    cast(publicationDateDay as date) as publication_date_day,
    * exclude (objectId, noticeType, publicationDateDay, data_model)
from {{ raw_silver_relation('contract_notice_part') }}
{{ dev_date_window('publicationDateDay') }}
