# Experiment plans

These are proposed designs. No experiments have been run on Close.

## Homepage: remove the before/after ambiguity

**Decision:** ship a new homepage when randomized evidence improves acquisition without a material downstream quality loss.

**Assignment:** eligible first-time human visitor, deterministic and stable through signup, with assignment linked to the eventual organization. Do not randomize page loads independently. Analyze intent-to-treat; log exposure separately for diagnostics. Specify handling of returning visitors, multiple devices, shared company domains, staff and bots before launch.

**Primary endpoint:** trial organization created within 14 days of first eligible exposure. Use one qualifying acquisition per visitor and reconcile organization duplication. The prototype's visitor-grain rate is an illustration; the experiment needs a locked visitor-to-org policy.

**Secondary quality endpoints:** paid within 30 days, activation, normalized subscription contribution. These do not share the primary endpoint's maturity window. Do not quietly change the winner metric after seeing results. Guardrails: page performance, signup errors and support burden.

**Power:** with a hypothetical 6.4% baseline and +1 percentage point absolute MDE, an equal-allocation two-sided normal approximation at alpha .05 and 80% power requires about 10,083 eligible visitors per arm. Derive the actual baseline, unit correlation, eligible daily traffic and acceptable effect before launch. Total calendar time is enrollment duration plus endpoint maturation, with full-week coverage; no invented two-week promise.

**Analysis:** prespecified fixed-horizon difference in proportions with an uncertainty interval; check sample-ratio mismatch, assignment persistence, measurement outages, novelty and channel/device balance. Repeated-visitor dependence and organization spillovers may require clustering or a different randomization unit. No repeated significance peeking; use a prespecified sequential method only if continuous decisions are required.

## Branded search: measure substitution

**Decision:** retain, scale or reduce brand spend based on incremental contribution, with an agreed maximum loss during learning.

**Design:** choose geographies with enough volume, stable targeting and observable all-channel acquisition. Match on prespecified pre-period outcomes, randomize within pairs, suppress brand ads only in assigned off geos, hold other acquisition changes steady, and document assignment before launch. Inspect pre-period trends and run power simulations with historical geo-level variation. If geo separation is too weak or volume insufficient, do not force this design.

**Outcome:** all-channel new paid organizations assigned consistently by organization geography, not only ad-platform attributed conversions. Include organic and direct substitution. Prespecify signup-to-paid maturation and use the same treatment enrollment window on both sides. Track competitor bidding, brand defense effects, cross-geo travel and campaign leakage.

**Estimator in this repo:** treated minus control change within each pair, summed over treated geos. Pair-level t interval for uncertainty; two-sided sign-flip Monte Carlo test of a sharp zero-effect null. The randomization test uses 100,000 seeded flips with the plus-one correction. The fixture assumes randomized pairs and no interference. It is not a production power analysis.

**Decision rule:** compare a defensible range of incremental contribution against spend and the prespecified hurdle. A positive point estimate with an economically weak lower bound should not automatically trigger scaling. If the lift interval spans zero, do not report a finite upper acquisition-cost bound. A materially negative result supports reduction only after confirming measurement and treatment delivery.

## AI-focused acquisition: the distinctive follow-on

Compare an AI-oriented landing-page message with a communication-and-follow-up message under randomized assignment. Keep audience and purchase path consistent. Measure trial conversion first, then seven-day activation and 30-day paid conversion at equal maturity. Segment by pre-exposure business size or use case only when measured consistently and supported by sample size.

Treat AI activation as a mediator, not a pre-treatment control. Comparing voluntary AI adopters against nonadopters is not a causal test of AI value. A randomized onboarding encouragement could be a later experiment, with intent-to-treat analysis and explicit limitations.

Google's [Conversion Lift explanation](https://support.google.com/google-ads/answer/12003020?hl=en) supports the distinction between attributed and incremental conversions. Availability of a platform lift product is not assumed.
