with ranked as (
    select *, row_number() over (partition by event_id order by event_date, anon_id) as retry_rank
    from {{ ref('raw_visits') }}
)
select event_id, anon_id, cast(event_date as date) as event_date, period,
    case when utm_source <> 'unknown' then utm_source
         when click_channel <> 'none' then click_channel
         when referrer <> 'none' then referrer else 'unknown' end as channel,
    case when utm_source = 'unknown' and click_channel <> 'none' then 1 else 0 end as recovered_utm
from ranked
where retry_rank = 1 and is_bot = 0

