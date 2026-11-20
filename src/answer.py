"""A deliberately bounded evidence interface. No arbitrary SQL or generated claims."""
import argparse
import json
from pathlib import Path

def answer(question):
    data=json.loads((Path(__file__).resolve().parents[1]/'analysis/results.json').read_text())
    common=dict(synthetic=True,as_of=data['as_of'],source='analysis/results.json')
    if question=='homepage':
        return dict(**common,status='descriptive_only',evidence=data['homepage'],action='Run an organization-stable randomized homepage test; do not claim causal lift.')
    if question=='brand-incrementality':
        return dict(**common,status='refused',reason='Attribution cannot identify incrementality. The geo fixture illustrates an estimator, not Close campaign results.')
    if question=='budget':
        return dict(**common,status='scenario_only',evidence=data['channels'],action='Use the modeled costs for sensitivity; obtain marginal response or experimental lift before reallocating budget.')
    return dict(**common,status='refused',reason='Unsupported question. Allowed: homepage, brand-incrementality, budget.')

if __name__=='__main__':
    p=argparse.ArgumentParser(); p.add_argument('question'); args=p.parse_args()
    print(json.dumps(answer(args.question),indent=2))

