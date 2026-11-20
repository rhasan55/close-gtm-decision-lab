select channel, count(*) as mature_trials, sum(activated_7d) as activated,
    sum(paid_30d) as paid_orgs, sum(subscription_mrr) as subscription_mrr
from {{ ref('fct_trials') }}
where mature_30d = 1
group by channel

