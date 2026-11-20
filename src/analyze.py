"""Compute reviewable decision evidence from dbt tables, never from an LLM."""
from pathlib import Path
import json
import math
import duckdb
import numpy as np
from scipy.stats import t, norm

ROOT=Path(__file__).resolve().parents[1]
AS_OF='2026-11-20'


def standardized(rows):
    """Pre-period channel weights; variance conditional on those fixed weights."""
    groups=sorted({r['channel'] for r in rows})
    before={r['channel']:r for r in rows if r['period']=='before'}
    after={r['channel']:r for r in rows if r['period']=='after'}
    if any(c not in before or c not in after for c in groups):
        raise ValueError('No channel overlap; standardization is not identified.')
    n0=sum(r['visitors'] for r in before.values())
    n1=sum(r['visitors'] for r in after.values())
    raw0=sum(r['trials'] for r in before.values())/n0
    raw1=sum(r['trials'] for r in after.values())/n1
    adjusted=0.; variance=0.; within=[]
    for c in groups:
        a,b=before[c],after[c]
        w=a['visitors']/n0
        p0=a['trials']/a['visitors']; p1=b['trials']/b['visitors']
        adjusted+=w*p1
        variance+=w*w*(p0*(1-p0)/a['visitors']+p1*(1-p1)/b['visitors'])
        within.append(dict(channel=c,before=p0,after=p1,before_n=a['visitors'],after_n=b['visitors'],weight=w))
    delta=adjusted-raw0
    return dict(before=raw0,after=raw1,adjusted_after=adjusted,raw_delta=raw1-raw0,
        adjusted_delta=delta,composition_delta=raw1-adjusted,
        ci=[delta-1.96*math.sqrt(variance),delta+1.96*math.sqrt(variance)],segments=within,
        interpretation='Descriptive fixed-mix comparison. No randomized homepage assignment; no causal redesign claim.')


def paired_lift(pairs, spend):
    """Paired before/after difference. CI clusters at randomized pair, not users."""
    d=np.asarray(pairs,dtype=float)
    if len(d)<3: raise ValueError('At least three randomized pairs required.')
    mean=float(d.mean()); se=float(d.std(ddof=1)/np.sqrt(len(d)))
    q=float(t.ppf(.975,len(d)-1))
    ci=[len(d)*(mean-q*se),len(d)*(mean+q*se)]
    rng=np.random.default_rng(42)
    flips=rng.choice([-1,1],size=(100000,len(d)))
    p=float((1+np.sum(np.abs((flips*d).mean(axis=1))>=abs(mean)))/100001)
    total=mean*len(d)
    return dict(pairs=len(d),incremental_paid=total,ci=ci,spend=spend,
        incremental_cost_per_paid=spend/total if total>0 else None,
        cost_ci=[spend/ci[1],spend/ci[0]] if ci[0]>0 else None,
        randomization_p=p,positive_evidence=ci[0]>0,
        scope='Synthetic randomized geo-pair fixture; all-channel paid orgs. Not evidence about Close.')


def sample_size(baseline, absolute_mde):
    """Normal approximation: two-sided alpha .05, power .80, equal allocation."""
    p1=baseline+absolute_mde
    if not 0<baseline<p1<1: raise ValueError('Rates must be strictly inside (0, 1).')
    p=(baseline+p1)/2
    return math.ceil(((norm.ppf(.975)*math.sqrt(2*p*(1-p))+norm.ppf(.8)*math.sqrt(baseline*(1-baseline)+p1*(1-p1)))**2)/(absolute_mde**2))


def build():
    con=duckdb.connect(str(ROOT/'target/close_gtm.duckdb'),read_only=True)
    def records(sql):
        cur=con.execute(sql)
        return [dict(zip([x[0] for x in cur.description],row)) for row in cur.fetchall()]
    home=records("select period,channel,count(*) as visitors,sum(trial_started) as trials from fct_visitors where period in ('before','after') group by period,channel")
    channels=records('select * from channel_cohorts order by channel')
    cost={'brand':18000,'nonbrand':26000,'content':14000,'partner':8000,'unattributed':None}
    for r in channels:
        r['modeled_cost']=cost[r['channel']]
        r['cost_per_paid']=cost[r['channel']]/r['paid_orgs'] if r['paid_orgs'] and cost[r['channel']] is not None else None
        r['trial_to_paid']=r['paid_orgs']/r['mature_trials']
        r['activation_rate']=r['activated']/r['mature_trials']
        r['monthly_subscription_per_paid']=r['subscription_mrr']/r['paid_orgs'] if r['paid_orgs'] else 0
    d=con.execute('''select sum(case when treatment=1 then after_paid-before_paid else -(after_paid-before_paid) end)
        from raw_geo group by pair_id order by pair_id''').fetchnumpy()
    pairs=list(d.values())[0]
    spend=int(con.execute('select sum(incremental_spend) from raw_geo').fetchone()[0])
    scalar=lambda sql: int(con.execute(sql).fetchone()[0])
    quality=dict(raw_rows=scalar('select count(*) from raw_visits'),
        duplicate_events=scalar('select count(*)-count(distinct event_id) from raw_visits'),
        bot_events=scalar('select count(distinct event_id) from raw_visits where is_bot=1'),
        ambiguous_visitors=scalar('select count(*) from (select anon_id from raw_identity group by anon_id having count(distinct org_id)>1)'),
        recovered_utm=scalar('select sum(recovered_utm) from stg_visits'),
        immature_trials=scalar('select count(*) from fct_trials where mature_30d=0'),
        unattributed_trials=scalar("select count(*) from fct_trials where channel='unattributed'"))
    result=dict(synthetic=True,as_of=AS_OF,seed=42,homepage=standardized(home),geo=paired_lift(pairs,spend),
        channels=channels,quality=quality,experiment=dict(baseline=.064,mde=.01,per_arm=sample_size(.064,.01)))
    (ROOT/'docs/results.json').write_text(json.dumps(result,indent=2)+'\n')
    (ROOT/'docs/results.js').write_text('window.LAB_RESULTS = '+json.dumps(result)+';\n')
    (ROOT/'analysis/results.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
    con.close()


if __name__=='__main__': build()

