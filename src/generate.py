"""Seeded fictional data. No Close customer data, IDs, or private APIs are used."""
from pathlib import Path
from datetime import date, timedelta
import csv
import random

ROOT = Path(__file__).resolve().parents[1]
AS_OF = date(2026, 11, 20)
SEED = 42


def write(name, rows):
    path = ROOT / 'seeds' / (name + '.csv')
    path.parent.mkdir(exist_ok=True)
    with path.open('w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def generate():
    rng = random.Random(SEED)
    visits, identities, trials, activity, invoices = [], [], [], [], []
    specs = {
        'before': [('brand',1500,.20), ('nonbrand',2000,.08), ('content',6000,.02), ('partner',500,.12)],
        'after': [('brand',4500,.18), ('nonbrand',2000,.07), ('content',2000,.015), ('partner',1500,.11)],
        'recent': [('brand',200,.18), ('nonbrand',100,.07), ('content',100,.02), ('partner',100,.11)]
    }
    num = 0
    for period, groups in specs.items():
        for channel, size, rate in groups:
            converted = set(rng.sample(range(size), round(size*rate)))
            for j in range(size):
                num += 1
                anon = f'anon_{num:06}'
                base = {'before':date(2026,7,1),'after':date(2026,9,1),'recent':date(2026,11,10)}[period]
                day = base + timedelta(days=rng.randrange(40 if period != 'recent' else 5))
                missing = channel in ('brand','nonbrand') and num % 17 == 0
                visits.append(dict(event_id=f'visit_{num}',anon_id=anon,event_date=day,period=period,
                    utm_source='unknown' if missing else channel,click_channel=channel if missing else 'none',
                    referrer='none' if missing else channel,is_bot=0))
                if j in converted:
                    org = f'org_{num:06}'
                    started = day + timedelta(days=1)
                    identities.append(dict(anon_id=anon,org_id=org,identified_date=started))
                    trials.append(dict(org_id=org,trial_date=started,segment=rng.choice(['agency','education','saas','services']),
                        seats=rng.choice([3,5,10]),plan=rng.choice(['Essentials','Growth','Scale'])))
                    activated = rng.random() < {'brand':.57,'nonbrand':.64,'content':.39,'partner':.78}[channel]
                    if activated:
                        for event in ['data_imported','teammate_invited','conversation_completed']:
                            activity.append(dict(event_id=f'{org}_{event}',org_id=org,event_name=event,event_date=started+timedelta(days=rng.randrange(1,7))))
                    if rng.random() < (.42 if activated else .07):
                        paid_date = started+timedelta(days=rng.randrange(15,29))
                        if paid_date <= AS_OF:
                            t=trials[-1]
                            mrr=t['seats']*{'Essentials':35,'Growth':99,'Scale':139}[t['plan']]
                            # Normalized monthly subscription MRR, excludes usage and tax.
                            invoices.append(dict(invoice_id=f'inv_{org}',org_id=org,paid_date=paid_date,
                                subscription_mrr=mrr,refunded=int(rng.random()<.035)))
                if num % 100 == 0:
                    visits.append(dict(visits[-1]))  # retry duplicates
    for i in range(120):
        visits.append(dict(event_id=f'bot_{i}',anon_id=f'bot_anon_{i}',event_date='2026-09-15',period='after',
            utm_source='content',click_channel='none',referrer='content',is_bot=1))
    # Deliberately ambiguous shared-browser identity: quarantine, never arbitrarily pick one org.
    for row in identities[:5]:
        identities.append(dict(row,org_id=identities[20]['org_id']))
    write('raw_visits',visits)
    write('raw_identity',identities)
    write('raw_trials',trials)
    write('raw_activity',activity)
    write('raw_invoices',invoices)
    geo=[]
    # Pair-level randomized simulation; all-channel new paid organizations are outcomes.
    for pair in range(20):
        baseline=rng.randrange(100,180)
        trends=rng.randrange(-8,12)
        assignment=rng.randrange(2)
        for member in range(2):
            treatment=int(member==assignment)
            before=baseline+rng.randrange(-8,9)
            after=before+trends+(7 if treatment else 0)+rng.randrange(-12,13)
            geo.append(dict(pair_id=pair,geo_id=f'geo_{pair}_{member}',treatment=treatment,
                before_paid=before,after_paid=after,incremental_spend=1800 if treatment else 0))
    write('raw_geo',geo)
    print(f'Generated synthetic fixture: {len(visits):,} raw visit rows; {len(trials):,} trial organizations.')


if __name__=='__main__':
    generate()
