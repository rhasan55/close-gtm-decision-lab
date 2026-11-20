# Decision memo

**Status:** fictional exercise, not a recommendation about Close's actual spend. **As of:** November 20, 2026.

The data supports a measurement and experimentation decision before a budget decision.

## Homepage

Observed human-visitor-to-trial conversion rises from 6.35% to 11.45%. At the earlier channel mix, after-period conversion is 5.54%, a decline of 0.81 percentage points. Composition contributes +5.91 points to the +5.10-point headline change; performance at fixed mix contributes −0.81 points. This is a reference-dependent decomposition, not a unique causal allocation.

Do not announce a redesign win or conclude that the redesign caused harm. Run a stable-assignment randomized comparison. Use a 14-day trial endpoint with a prespecified 30-day paid quality check. An illustrative 6.4% baseline and +1-point MDE need approximately 10,083 eligible visitors per arm at 80% power before adjustments for attrition or dependence.

The decision would change with a valid randomized result, balanced exposure, complete outcome windows and no material paid-quality deterioration.

## Branded search

The separate randomized geo fixture estimates 141 incremental paid organizations on $36,000 of incremental spend, with a pair-level 95% interval of approximately 30–252. Incremental cost is approximately $255 per paid organization, with a wide $143–$1,193 transformed interval. The sign-flip randomization test gives a two-sided Monte Carlo p-value near .017.

These numbers illustrate why uncertainty matters. They are not an observed brand campaign result and cannot be compared directly with the channel fixture's attributed cost. Run a bounded holdout using all-channel paid organizations, with a loss limit agreed in advance. If the interval includes zero, a finite upper bound on incremental acquisition cost is unavailable.

The decision would change when real experimental lift and contribution economics support a prespecified investment hurdle.

## Activation and acquisition economics

Partners show the strongest proposed activation rate in the fixture, but may simply deliver more prepared buyers. Use this as an investigation and test priority. Do not move the entire budget based on average attributed acquisition cost.

Compare cohorts only at equal maturity. Keep the 56 recent trial organizations visible as immature rather than treating unobserved payment as failure. Use the sensitivity controls to see whether apparent payback survives lower margins and higher AI/support costs. Do not treat the simple payback calculation as LTV or an incremental return curve.

## Measurement repair

Keep all organizations in financial reconciliation, including five unattributed trials. Exclude ambiguous visitor identities from the homepage denominator, report that exclusion, and repair signup identity with engineering. Require idempotent event ingestion, preserved click metadata, fixed metric definitions and an explicit as-of date.

The practical output is a recommendation with an owner, acceptance checks and a follow-up experiment. No money is spent, no campaign is changed and no production system is connected by this project.
