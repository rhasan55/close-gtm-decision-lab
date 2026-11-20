select org_id from {{ ref('fct_trials') }} where paid_30d = 1 and subscription_mrr <= 0
