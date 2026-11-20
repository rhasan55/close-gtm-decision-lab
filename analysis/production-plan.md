# Engineering and production handoff

This is a design for adaptation, not a claim that integrations or Snowflake execution have been completed.

## First discovery session

Confirm actual authoritative sources, warehouse schema, billing system, product event taxonomy, consent model, experiment platform and existing dbt conventions with GTM, finance and engineering. No internal table or service names are assumed.

| Needed input | Fixture equivalent | Production acceptance condition |
| --- | --- | --- |
| Web events and exposure assignment | `raw_visits` | Stable event IDs, UTC event/received timestamps, traffic and consent classification, assignment persistence |
| Authenticated signup bridge | `raw_identity` | Deterministic org identity; time-bounded mappings; conflict quarantine and merge handling |
| Trial lifecycle | `raw_trials` | Immutable first-trial time, retrial policy, test accounts, exclusions agreed with GTM |
| Product milestones | `raw_activity` | Server-side org events for import, invite and completed conversation; bot/test activity separated |
| Subscription ledger | `raw_invoices` | Normalize annual billing and state changes; refunds, credits, failed payments, seat changes reconciled to finance |
| Channel expenses | Python assumptions | Same cohort window; paid media, partner fees and allocated costs clearly distinguished |
| Experiment geography | `raw_geo` | Locked geo assignment and eligible population, matched pre-period outcomes, leakage monitoring |

## Concrete repair tickets

1. **Signup identity, product engineering.** Emit stable `organization_id`, `anonymous_id`, experiment assignment and event ID when signup succeeds. Send no raw email into analytics identifiers. Capture deterministic merge/split events. Acceptance: fixture-style ambiguous links quarantined; production match coverage and conflict rate measured against a known signup sample.
2. **Acquisition metadata, growth engineering.** Preserve approved source parameters and click mapping across redirects and the signup domain, respecting consent. Do not overwrite first acquisition with later app navigation. Acceptance: tagged end-to-end journeys from each paid source, organic, partner and unknown reconcile with signup logs.
3. **Idempotent ingestion, data engineering.** Persist immutable raw payload versions with received timestamp. Upsert current representation by event ID and version; preserve audit history. Acceptance: duplicate deliveries do not change metrics, late data restates the correct cohort and conflicting duplicate payloads are observable.
4. **Subscription state, finance + analytics engineering.** Replace the fixture's single invoice model with effective-dated subscription facts and credits. Acceptance: recurring revenue bridges reconcile to the authoritative ledger and refunds do not count as paid wins.
5. **Metric publication, analyst.** Ship explicit definitions, owners, as-of dates, freshness indicators and causal scope. Acceptance: dashboard, memo and bounded answers produce the same mature denominators and totals.

## Snowflake adaptation

Keep the staging → identity → organization-grain fact → channel cohort structure. Replace local CSV seeds with source declarations and source-specific staging. Add an environment-backed Snowflake profile, service-role permissions and warehouse controls using Close's existing conventions. Do not commit credentials or invent database names.

Review date arithmetic, boolean casting, JSON parsing and source timestamp types under the actual Snowflake adapter. Use `DATEADD` and UTC normalization where needed; rerun adversarial fixtures and source reconciliation before deployment. DuckDB execution does not establish Snowflake compatibility.

Start with full-refresh on this small fixture. Only introduce incremental processing after defining late-arrival lookback, update ordering, organization merges, deletions and financial restatements. Partitioned storage and warehouse cost controls depend on measured production volume, not this demo's row count.

## CRM API boundary

If separately building a customer-side Close integration, the [Event Log](https://developer.close.com/api/resources/events) exposes changes for 30 days and can consolidate updates to existing events. Poll with overlap, persist versioned history, handle deletes, checkpoint only after durable writes and respect rate limits. A one-time export cannot reconstruct arbitrarily old changes.

That API is not the proposed source for Close's own marketing acquisition. Internal signup, product and billing data must come from the actual internal sources confirmed in discovery.

## Operational ownership

Weekly: reconcile signup and finance counts, review identity conflicts, assess freshness and ingestion lag, and review changes to channel definitions. Incident: suspend affected recommendations when upstream tests fail, retain the last known snapshot with a stale label, and assign a named owner. Experiments require explicit launch/stop decisions; this repo never changes spend automatically.
