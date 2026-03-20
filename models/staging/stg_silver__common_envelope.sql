select
    objectId as notice_id,
    caseId as case_id,
    noticeType as notice_type,
    cast(publicationDate as date) as publication_date,
    cast(publicationDateDay as date) as publication_date_day,
    tenderId as tender_id,
    objectId as object_id,
    organizationId as buyer_id,
    organizationName as buyer_name,
    clientTypeName as client_type_name,
    provinceName as province_name,
    noticeStage as notice_stage,
    * exclude (
        objectId,
        caseId,
        noticeType,
        publicationDate,
        publicationDateDay,
        tenderId,
        organizationId,
        organizationName,
        clientTypeName,
        provinceName,
        noticeStage
    )
from {{ raw_silver_relation('common_envelope') }}
{{ dev_date_window('publicationDateDay') }}
