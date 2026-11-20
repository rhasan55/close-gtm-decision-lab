select anon_id, min(org_id) as org_id
from {{ ref('raw_identity') }}
group by anon_id
having count(distinct org_id) = 1

