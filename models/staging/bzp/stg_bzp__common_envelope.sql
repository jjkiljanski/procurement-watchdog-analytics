select
    notice_id,
    caseId as case_id,
    noticeType as notice_type,
    cast(publicationDate as date) as publication_date,
    cast(publicationDateDay as date) as publication_date_day,
    tenderId as tender_id,
    objectId as object_id,
    buyerName as buyer_name,
    buyerId as buyer_id,
    clientTypeName as client_type_name,
    provinceName as province_name,
    noticeStage as notice_stage
from {{ source('warehouse_bzp', 'silver_common_envelope') }}
