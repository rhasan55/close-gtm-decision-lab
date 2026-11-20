with ambiguous as (
    select anon_id from {{ ref('raw_identity') }} group by anon_id having count(distinct org_id) > 1
), ranked as (
    select v.*, row_number() over (partition by v.anon_id order by v.event_date, v.event_id) as visit_rank
    from {{ ref('stg_visits') }} v
    left join ambiguous a on v.anon_id = a.anon_id
    where a.anon_id is null
)
select r.anon_id, r.event_date, r.period, r.channel,
    case when t.org_id is not null then 1 else 0 end as trial_started
from ranked r
left join {{ ref('stg_identity') }} i on r.anon_id = i.anon_id
left join {{ ref('raw_trials') }} t on i.org_id = t.org_id
    and cast(t.trial_date as date) between r.event_date and r.event_date + interval '14 days'
where visit_rank = 1

