select 'channel totals mismatch' as failure
where (select sum(paid_orgs) from {{ ref('channel_cohorts') }} ) <>
      (select sum(paid_30d) from {{ ref('fct_trials') }} where mature_30d = 1)

