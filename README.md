# Close GTM Decision Lab

**A reproducible decision exercise for the Full Stack Data Analyst, GTM role at Close.**

Independent portfolio work by Hasan Raja. All analytical records and results are synthetic. No Close systems, private data, customer records, or credentials are used. Public sources inform the questions, not the simulated answers.

[Open the live walkthrough](https://rhasan55.github.io/close-gtm-decision-lab/) · [Read the decision memo](analysis/decision-memo.md)

## Start with the decision

Would you celebrate a homepage conversion increase from **6.35% to 11.45%**?

In this fixture, conversion fell within every acquisition channel. The apparent improvement came from a shift toward higher-intent traffic. Holding the earlier channel mix fixed produces a **0.81 percentage point decline**, with an approximate 95% interval of **−1.44 to −0.18 points**. That still does **not** identify the redesign's causal effect.

The recommendation: withhold the win, fix measurement gaps, and run a randomized test with a prespecified outcome window.

Open `docs/index.html` directly for the interactive review, or run `make serve` and visit the address printed by Python. No frontend build, paid service, API key, or LLM is required. The page includes a traffic-mix comparison, a geo-experiment example, adjustable acquisition economics, and a measurement repair plan.

## What is built

| Decision | Implemented evidence | Boundary |
| --- | --- | --- |
| Did the homepage improve conversion? | Visitor-grain rates, channel standardization, decomposition, conditional uncertainty | Before/after is descriptive; no randomized redesign assignment |
| Does branded search create customers? | Separate simulated randomized geo pairs; paired difference-in-differences, pair-level interval and sign-flip test | Attribution does not identify lift; no real Close experiment |
| Where should the next dollar go? | Mature trial cohorts, 7-day activation, paid within 30 days, subscription MRR and cost sensitivity | No marginal response curves, churn or identified optimal allocation |
| Can we trust the recommendation? | dbt tests, retry deduplication, identity quarantine, maturity flags, reconciliation, bounded evidence interface | Production bot detection and source ingestion are outside this demo |

The five dbt models execute locally on DuckDB. SQL model definitions, metric contracts, assumptions and limitations are included. A Snowflake migration plan is documented; execution against Snowflake has **not** been verified.

## Reproduce

Tested with Python 3.12. A supported Python version for the pinned dependencies is required.

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
make all
make serve
```

`make all` generates seeded data, runs `dbt build`, computes evidence and runs behavioral tests. The as-of date is frozen at **2026-11-20**. Generated CSV seeds and the local database are ignored by Git. Checked-in JSON and JS outputs allow review without installing Python.

```bash
python src/answer.py homepage
python src/answer.py brand-incrementality
python src/answer.py budget
```

The brand-incrementality request explicitly refuses to infer real campaign lift from attribution. This interface is a small allowlist with structured evidence, not a general-purpose AI analyst or a full MetricFlow deployment.

## Review path

1. [Decision memo](analysis/decision-memo.md): what to do, why, and what would change the decision.
2. [Company and market research](analysis/research.md): primary sources and resulting hypotheses.
3. [Metric contracts](analysis/metrics.md): grain, denominator, maturity and exclusions.
4. [Experiment plan](analysis/experiments.md): assignment, power, endpoints and risks.
5. [Engineering handoff](analysis/production-plan.md): instrumentation, ingestion and Snowflake mapping.
6. [SQL models](models) and [behavioral tests](tests/test_analysis.py): inspect implementation.
7. [Computed results](analysis/results.json): review the exact evidence used by the page.

## Fixture scope

20,825 raw visit rows include 205 retries and 120 flagged bots. Five anonymous IDs map to multiple organizations and are quarantined. The fixture recovers 605 visits using supplied click-channel mappings. There are 1,841 trial organizations; 56 lack a complete 30-day observation window. Ambiguous organizations remain financially reconciled under `unattributed`.

The homepage example and geo experiment use **different synthetic populations**. Never combine their estimates. The visitor fixture deliberately creates Simpson's paradox; it is an explanatory stress case, not an unbiased sample of a real business.

## Publishing

The `docs` directory is a static site. To use GitHub Pages, create a public repository, push this project, and select **Deploy from a branch → main → /docs** in Pages settings. GitHub Actions runs the analytical checks on pushes and pull requests. A portable `docs/close-gtm-decision-lab.zip` can be generated with `python src/package.py`; it excludes hosting identity and private application notes.

## Limitations worth discussing

- Channel standardization controls only observed channel composition. Intent, country, device, seasonality and concurrent launches remain potential confounders.
- The normal approximation interval assumes independent visitors and conditions on baseline weights. A real deployment should cluster repeated visits and check small cells.
- Activation thresholds are proposals. Their association with payment does not establish a causal effect, and optimizing them can invite gaming.
- Subscription MRR is a normalized recurring amount, not invoice cash, recognized revenue, ARR or contribution profit.
- Economics use fictional costs and cohort mix. Usage revenue and costs, refunds beyond the observation window, retention, expansion and acquisition salaries need real inputs.
- The geo example assumes correct randomization, comparable observation windows, no spillover and stable measurement. Twenty pairs do not establish an appropriate sample size for Close.

## Sources and independence

Research was checked November 20, 2026. See [the source register](analysis/research.md). Customer claims remain vendor-published accounts. Company headcount differs across public pages. The project does not estimate Close's revenue, CAC, retention, budget, or channel performance.

MIT license. Close names and marks belong to their respective owners; no endorsement is implied.
