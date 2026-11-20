# Metric contracts

These definitions are implemented in dbt SQL or the Python evidence calculation. This is a lightweight contract layer, not a deployed dbt Semantic Layer service.

| Metric | Grain and denominator | Window and exclusions | Source |
| --- | --- | --- | --- |
| Visitor → trial | First human anonymous visitor; eligible visitors in each period | Trial starts 0–14 days after first visit; exclude bots, event retries and multi-org anonymous identities | `fct_visitors` |
| Fixed-mix conversion | Channel rates weighted by before-period eligible visitor shares | Common channel support required; weights are fixed for conditional uncertainty | `src/analyze.py:standardized` |
| Trial organization | One `org_id` | One fictional first trial per org; no retrials modeled | `fct_trials` |
| Activation | Trial org completes all three distinct milestones | 0–7 days inclusive: import, invite, completed conversation; as-of cutoff applies; require full 7-day maturity for comparisons | `fct_trials` |
| Paid within 30 days | Trial org has positive net subscription MRR from qualifying nonrefunded invoices | Trial date through day 30 inclusive and no later than as-of; compare only mature orgs | `fct_trials`, `channel_cohorts` |
| Subscription MRR | Sum of normalized recurring monthly subscription values from qualifying nonrefunded invoices | Fictional fixture has one initial subscription invoice per paid org; excludes usage, tax and refunded invoices | `fct_trials` |
| Channel assignment | Latest eligible pretrial touch in a 30-day window | Deterministic unambiguous org bridge; source → trusted click mapping → referrer → unknown; no post-signup touches | `fct_trials` |
| Modeled acquisition cost / paid | Fictional fully assigned channel expense ÷ mature paid org count | Cost period matches the combined mature fixture; excludes unknown allocation and unmodeled acquisition salaries | Python cost assumptions |
| Simple modeled payback | Cost / paid ÷ monthly contribution proxy | MRR × assumed margin minus additional monthly cost; no churn/expansion; null if cost unknown or contribution nonpositive | `docs/app.js` |
| Geo incremental paid | Sum over treated geos of paired before/after differences relative to control | Randomization unit is geo within matched pair; independent fixture; outcomes count all-channel new paid orgs | `src/analyze.py:paired_lift` |

## Identity and source contracts

- Synthetic IDs are meaningless identifiers. No names, emails or real organizations are included.
- One anonymous ID resolving to multiple organizations is quarantined, not arbitrarily assigned. Multiple anonymous IDs resolving to one organization require an organization-level touch choice, not a fanout join.
- Event IDs identify delivery retries, not business entities. Production ingestion needs event timestamps, received timestamps and version ordering; conflicting duplicate payloads should be investigated.
- Fixtures supply trusted `click_channel` and `is_bot` signals. This is not a production implementation of click-ID resolution or bot detection.
- Direct, consent-denied and untracked traffic should remain explicit in a real channel model. No probabilistic cross-device identity or causal multi-touch credit is inferred here.

## Reconciliation and maturity

The visitor mart can exclude ambiguous identities; the trial mart retains all trials, with unattributed channel where needed. Finance totals reconcile to the full mature trial population. The 7-day and 30-day flags are separate. Paid within 30 days is **not** retained on day 30, and no survival or retention analysis is claimed.

The simple subscription calculation is valid only for the fixture's one initial invoice per org. Production needs subscription-state history, credit notes, seat changes, cancellations, annual normalization and an authoritative billing ledger before computing MRR.
