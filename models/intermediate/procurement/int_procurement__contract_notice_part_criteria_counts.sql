with parts as (
    select * from {{ ref('stg_silver__contract_notice_part') }}
),
criteria as (
    select * from {{ ref('stg_silver__contract_notice_part_criterion') }}
),
part_counts as (
    select
        parts.cn_part_notice_id,
        parts.cn_part_notice_type,
        parts.cn_part_publication_date_day,
        parts.cn_part_ordinal,
        parts.cn_part_short_description,
        count(distinct criteria.cn_part_criterion_ordinal) as part_criterion_count
    from parts
    left join criteria
        on parts.cn_part_notice_id = criteria.cn_part_criterion_notice_id
       and parts.cn_part_ordinal = criteria.cn_part_criterion_part_ordinal
    group by 1, 2, 3, 4, 5
)

select
    cn_part_notice_id,
    cn_part_notice_type,
    cn_part_publication_date_day,
    cn_part_ordinal,
    cn_part_short_description,
    part_criterion_count,
    sum(part_criterion_count) over (
        partition by cn_part_notice_id
    ) as notice_criterion_count
from part_counts
