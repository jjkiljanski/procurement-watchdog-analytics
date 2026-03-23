select
    objectId as cn_client_notice_id,
    noticeType as cn_client_notice_type,
    cast(publicationDateDay as date) as cn_client_publication_date_day,
    section_1_2 as cn_client_name,
    section_1_3 as cn_client_department,
    section_1_4 as cn_client_national_id,
    section_1_4_type as cn_client_national_id_type,
    section_1_5_1 as cn_client_street,
    section_1_5_2 as cn_client_city,
    section_1_5_3 as cn_client_postal_code,
    section_1_5_4 as cn_client_province,
    section_1_5_5 as cn_client_country,
    section_1_5_6_code as cn_client_nuts3_code,
    section_1_5_6_name as cn_client_nuts3_name,
    section_1_5_7 as cn_client_phone,
    section_1_5_8 as cn_client_fax,
    section_1_5_9 as cn_client_email,
    section_1_5_10 as cn_client_website
from {{ raw_silver_relation('contract_notice_client') }}
{{ dev_date_window('publicationDateDay') }}
