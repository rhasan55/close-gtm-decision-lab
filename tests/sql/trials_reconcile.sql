select 'trial grain mismatch' as failure
where (select count(*) from {{ ref('fct_trials') }}) <> (select count(*) from {{ ref('raw_trials') }})

