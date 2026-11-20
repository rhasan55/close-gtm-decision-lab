import sys
import unittest
from pathlib import Path
import duckdb

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from analyze import standardized,paired_lift,sample_size
from answer import answer

class DecisionTests(unittest.TestCase):
    def test_simpsons_paradox(self):
        rows=[dict(period=p,channel=c,visitors=n,trials=k) for p,c,n,k in [
            ('before','high',100,50),('before','low',900,90),('after','high',900,405),('after','low',100,5)]]
        r=standardized(rows)
        self.assertGreater(r['raw_delta'],0)
        self.assertLess(r['adjusted_delta'],0)
        self.assertAlmostEqual(r['raw_delta'],r['composition_delta']+r['adjusted_delta'])

    def test_nonoverlap_refused(self):
        with self.assertRaises(ValueError):
            standardized([dict(period='before',channel='a',visitors=10,trials=1),dict(period='after',channel='b',visitors=10,trials=1)])

    def test_uncertain_lift_has_no_finite_cost_interval(self):
        r=paired_lift([-20,20,0,-10,10],1000)
        self.assertIsNone(r['cost_ci'])
        self.assertFalse(r['positive_evidence'])

    def test_power_increases_for_smaller_effect(self):
        self.assertGreater(sample_size(.068,.005),sample_size(.068,.01))

    def test_causal_question_refused(self):
        self.assertEqual(answer('brand-incrementality')['status'],'refused')

    def test_unknown_question_refused(self):
        self.assertEqual(answer('DROP TABLE fct_trials')['status'],'refused')

    def test_duplicate_and_ambiguous_identity_quarantined(self):
        con=duckdb.connect()
        con.execute("create table raw_identity as select * from (values ('a','o1'),('a','o1'),('b','o1'),('b','o2')) t(anon_id,org_id)")
        sql=(ROOT/'models/staging/stg_identity.sql').read_text().replace("{{ ref('raw_identity') }}",'raw_identity')
        self.assertEqual(con.execute(sql).fetchall(),[('a','o1')])
        con.close()

    def test_bots_and_event_retries_removed(self):
        con=duckdb.connect()
        con.execute("""create table raw_visits as select * from (values
          ('e1','a','2026-01-01','before','unknown','brand','none',0),
          ('e1','a','2026-01-01','before','unknown','brand','none',0),
          ('e2','b','2026-01-01','before','content','none','none',1)
        ) t(event_id,anon_id,event_date,period,utm_source,click_channel,referrer,is_bot)""")
        sql=(ROOT/'models/staging/stg_visits.sql').read_text().replace("{{ ref('raw_visits') }}",'raw_visits')
        rows=con.execute(sql).fetchall()
        self.assertEqual(len(rows),1); self.assertEqual(rows[0][-2: ],('brand',1))
        con.close()

    def test_maturity_and_revenue_reconciliation(self):
        con=duckdb.connect(str(ROOT/'target/close_gtm.duckdb'),read_only=True)
        self.assertEqual(con.execute('select count(*)-count(distinct org_id) from fct_trials').fetchone()[0],0)
        self.assertGreater(con.execute('select count(*) from fct_trials where mature_30d=0').fetchone()[0],0)
        self.assertEqual(con.execute('select sum(subscription_mrr) from channel_cohorts').fetchone()[0],
            con.execute('select sum(subscription_mrr) from fct_trials where mature_30d=1').fetchone()[0])
        con.close()

    def test_postsignup_touch_refund_and_activity_fanout(self):
        import re
        con=duckdb.connect()
        con.execute("""create table raw_trials as select * from (values
            ('o1','2026-09-01','saas',5,'Growth'),
            ('o2','2026-11-15','saas',3,'Essentials')
        ) t(org_id,trial_date,segment,seats,plan)""")
        con.execute("create table stg_identity as select * from (values ('a1','o1'),('a2','o2')) t(anon_id,org_id)")
        con.execute("""create table stg_visits as select event_id,anon_id,cast(event_date as date) as event_date,channel
          from (values ('e1','a1','2026-08-30','content'),('e2','a1','2026-09-05','brand')) t(event_id,anon_id,event_date,channel)""")
        con.execute("""create table raw_activity as select * from (values
          ('o1','data_imported','2026-09-02'),('o1','data_imported','2026-09-02'),
          ('o1','teammate_invited','2026-09-03'),('o1','conversation_completed','2026-09-04')
          ) t(org_id,event_name,event_date)""")
        con.execute("""create table raw_invoices as select * from (values
          ('o1','2026-09-20',100,0),('o1','2026-09-21',999,1),('o1','2026-10-15',5000,0)
          ) t(org_id,paid_date,subscription_mrr,refunded)""")
        sql=re.sub(r"\{\{ ref\('([^']+)'\) \}\}",r'\1',(ROOT/'models/marts/fct_trials.sql').read_text())
        cur=con.execute(sql); rows=[dict(zip([x[0] for x in cur.description],r)) for r in cur.fetchall()]
        rows={r['org_id']:r for r in rows}
        self.assertEqual(len(rows),2)
        self.assertEqual(rows['o1']['channel'],'content')
        self.assertEqual(rows['o1']['subscription_mrr'],100)
        self.assertEqual(rows['o1']['activated_7d'],1)
        self.assertEqual(rows['o2']['mature_30d'],0)
        con.close()

if __name__=='__main__': unittest.main()
