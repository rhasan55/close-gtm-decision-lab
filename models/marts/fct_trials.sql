-- Grain: one trial organization. Aggregate each one-to-many source before joining.
with touches as (
    select i.org_id, v.channel,
        row_number() over (partition by i.org_id order by v.event_date desc, v.event_id) as touch_rank
    from {{ ref('stg_visits') }} v
    join {{ ref('stg_identity') }} i on v.anon_id = i.anon_id
    join {{ ref('raw_trials') }} t on i.org_id = t.org_id
    where v.event_date <= cast(t.trial_date as date)
      and v.event_date >= cast(t.trial_date as date) - interval '30 days'
), activation as (
    select a.org_id, count(distinct a.event_name) as milestones
    from {{ ref('raw_activity') }} a
    join {{ ref('raw_trials') }} t on a.org_id = t.org_id
    where cast(a.event_date as date) between cast(t.trial_date as date) and cast(t.trial_date as date) + interval '7 days'
      and cast(a.event_date as date) <= date '2026-11-20'
      and a.event_name in ('data_imported','teammate_invited','conversation_completed')
    group by a.org_id
), paid as (
    select p.org_id, sum(case when p.refunded = 0 then p.subscription_mrr else 0 end) as net_mrr
    from {{ ref('raw_invoices') }} p
    join {{ ref('raw_trials') }} t on p.org_id = t.org_id
    where cast(p.paid_date as date) between cast(t.trial_date as date) and cast(t.trial_date as date) + interval '30 days'
      and cast(p.paid_date as date) <= date '2026-11-20'
    group by p.org_id
)
select t.org_id, cast(t.trial_date as date) as trial_date, t.segment, t.seats, t.plan,
    coalesce(touch.channel, 'unattributed') as channel,
    case when cast(t.trial_date as date) <= date '2026-11-20' - interval '7 days' then 1 else 0 end as mature_7d,
    case when cast(t.trial_date as date) <= date '2026-11-20' - interval '30 days' then 1 else 0 end as mature_30d,
    case when coalesce(a.milestones,0) = 3 then 1 else 0 end as activated_7d,
    case when coalesce(p.net_mrr,0) > 0 then 1 else 0 end as paid_30d,
    coalesce(p.net_mrr,0) as subscription_mrr
from {{ ref('raw_trials') }} t
left join touches touch on t.org_id = touch.org_id and touch.touch_rank = 1
left join activation a on t.org_id = a.org_id
left join paid p on t.org_id = p.org_id

