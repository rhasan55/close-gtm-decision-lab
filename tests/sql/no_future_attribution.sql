select org_id from {{ ref('fct_trials') }} where trial_date > date '2026-11-20'

