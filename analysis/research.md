# Close: company, customer and market research

Checked November 20, 2026. Links below are public primary sources. This is an independent assessment, not access to Close's strategy or internal performance.

## The business and why the question matters

[Close's About page](https://close.com/about) describes a self-funded, profitable CRM built around sales conversations, founded in 2013, serving 11,500+ businesses. Its customers are small businesses and sales teams whose work depends on calls, email, SMS, meetings and consistent follow-up. That positions acquisition quality and time to useful product adoption as plausible priorities. This is an inference from positioning, not a confirmed internal priority.

The site says 120+ employees; the [GTM role](https://jobs.ashbyhq.com/close/26b8da1b-702b-4e8e-a485-7b1ba79203fd/) and supplied hiring screenshot say approximately 130. Treat those as differing public snapshots, not evidence of contraction. The role is US remote and seeks its first GTM-dedicated full-stack analyst. Its examples explicitly concern branded-search incrementality, homepage traffic mix and investment decisions. It also emphasizes trustworthy self-service and owning the outcome beyond analysis.

The project therefore concentrates on those decisions. A polished reporting surface alone would demonstrate only part of the role. Tested transformations, defensible uncertainty and an engineering repair plan demonstrate more of the requested ownership.

## Current product and revenue structure

[Pricing snapshot](https://close.com/pricing), USD per user per month unless noted:

| Plan | Annual-billing equivalent | Monthly billing |
| --- | --- | --- |
| Solo, one user only | $9 | $19 |
| Essentials | $35 | $49 |
| Growth | $99 | $109 |
| Scale | $139 | $149 |

The page offers a 14-day no-credit-card trial. Calling and SMS usage are additional; AI credit allowances differ by plan. The fixture uses only normalized team-plan subscription prices, with invented seats and plan mix. It does not model Close's realized pricing, discounts, usage margins or economics.

The current [AI product page](https://close.com/ai) separates Chloe, an assistant that helps users act on CRM context, from autonomous AI Agents, currently described as beta. Older launch messaging described Chloe as an inbound voice teammate. Use the current terminology in a real conversation rather than assuming that older posts describe today's packaging exactly.

The useful analytical hypothesis is whether AI-led acquisition produces activated, paying accounts at attractive contribution economics. More AI interest may change trial composition, product costs and onboarding needs. None of those effects is established by public data.

## Vera's relevant public signals

The supplied screenshot is the strongest direct signal: Vera asks for someone who pulls data together, works with engineering on gaps and arrives with a recommendation. Her [joining announcement](https://www.linkedin.com/posts/veraalb_excited-to-share-that-ive-joinedclose-as-activity-7449598718519197696-0qiH) identifies her as Close's first technical recruiter and emphasizes trust, candor and intentional execution. Her [Chloe launch post](https://www.linkedin.com/posts/veraalb_at-close-we-just-unveiled-chloe-a-new-activity-7453458653296132096-xJJS) emphasizes speed to lead and customer outcomes.

These public professional posts support a concise, specific approach: show the working evidence, explain the decision it enables and acknowledge what cannot be known. They do not justify inferring private preferences. LinkedIn's public indexing is incomplete and relative dates are inconsistent; this is not a claim to have reviewed every post.

## Customer evidence translated into measurement hypotheses

| Customer | What Close publishes | Why it informs this project | What remains unknown |
| --- | --- | --- | --- |
| [Flatiron School](https://close.com/customers/flatiron-school) | A Salesforce migration, +75% conversion within 60 days, 91% lower acquisition cost and over $200K annual savings; faster applicant response and follow-up | Track time to first completed conversation and useful adoption, rather than only trial volume | Causal contribution of CRM, process changes, sourcing changes and other interventions |
| [RevPilot](https://close.com/customers/revpilot) | 20–30% revenue improvements without new ad spend, with simpler processes and disciplined follow-up | A partner's implementation expertise may improve acquired-account readiness; test partner cohort quality and capacity | Generalizability, selection effects, net margins and incremental acquisition impact |
| [Hownd](https://close.com/customers/hownd) | 80% CRM-cost reduction and over $110K annual savings after leaving Salesforce | Account value can include consolidated software and reduced admin burden; distinguish migration needs from net-new CRM adoption | Customer-specific counterfactual, long-run outcomes and Close's own economics |

These are vendor-published customer accounts, not randomized studies. Their outcomes belong to these customers, not to Close's own GTM funnel. They motivate proposed metrics; they are never loaded into the synthetic dataset or presented as model validation.

## Competitive assessment

| Alternative | Verified basis | Implication and testable hypothesis |
| --- | --- | --- |
| HubSpot | [Prospecting Agent documentation](https://knowledge.hubspot.com/prospecting/use-the-prospecting-agent) describes personalized outreach, buying signals and credit consumption | A native agent is not unique to Close. Test whether a simpler communication-first workflow attracts and activates the intended segment. |
| Pipedrive | [AI documentation](https://support.pipedrive.com/en/article/pipedrive-ai) lists AI reporting and a contextual Sales Assistant, with feature availability and beta caveats | Generic AI/reporting messaging may be weak differentiation. Measure activation and paid conversion, not page engagement alone. |
| Salesforce | Flatiron and Hownd document migration from Salesforce; [Salesforce's small-business offering](https://www.salesforce.com/small-business/) is a direct alternative | Migration friction, data quality and admin burden may distinguish switching accounts. Capture prior CRM before exposure if used for experiment segmentation. |
| GoHighLevel | Named in Close's company comparison set; RevPilot discusses working across Close, HubSpot and GoHighLevel. [HighLevel](https://www.gohighlevel.com/) markets an integrated business platform. | Agencies have multiple substitutes. Partner-sourced intent and buyer readiness can confound channel comparisons. No price or feature-parity claim is made. |
| Existing stack or inaction | The documented workarounds and separate tools in customer stories | Measure time to first useful workflow and migration completion. The relevant alternative may be keeping the current process. |

No unsupported market-share ranking, competitor win rate, ARR estimate or total-addressable-market number is included. Website feature lists cannot establish comparative performance or adoption quality.

## Recommended original angle

**“More trials. Better business?”** connects the role's immediate questions with the current AI positioning. The project demonstrates three different standards of evidence: descriptive standardization, randomized lift estimation and assumption-based economics. It refuses to silently turn any one into another.

Follow-on ideas, ranked by feasibility after data access:

1. **AI-message quality test:** randomize acquisition messaging, then compare trial and mature paid outcomes. It directly checks whether top-of-funnel gains survive downstream.
2. **Partner readiness study:** measure whether implementation support predicts faster activation. Use observational findings to design an onboarding encouragement experiment, not to claim causality.
3. **Switching-friction study:** identify where prior-CRM cohorts fail to import data, invite teammates or complete conversations. Validate event coverage before ranking friction.
4. **Contribution-aware learning agenda:** use experiments to calibrate channel incrementality, then evaluate bounded budget scenarios. Defer an optimizer until marginal response and uncertainty are credible.

## Method and implementation sources

- [dbt data tests](https://docs.getdbt.com/docs/build/data-tests): model assertions and business-specific failure queries.
- [Google Conversion Lift](https://support.google.com/google-ads/answer/12003020?hl=en): controlled incrementality measurement; platform availability is not assumed.
- [Close Event Log](https://developer.close.com/api/resources/events): only 30 days of history, updated/consolidated events and object semantics.

The public Close CRM API describes a customer's CRM objects. It is not a source for Close's own trial signup, billing and product telemetry. Confusing those systems would undermine this project's credibility; the production plan keeps that distinction explicit.
