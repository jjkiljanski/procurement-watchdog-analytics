select
    case
        when section_1_1 = 'A' then 'x'
        else null
    end as cn_procedure_conduct_mode,
    section_1_11_8_code as cn_procedure_operator_nuts3_code,
    section_1_11_8_name as cn_procedure_operator_nuts3_name
from something
