# research/

Reports produced by the `ads-market-research` agent live here.

## Conventions

- **Filename:** `YYYY-MM-DD-short-topic-slug.md` (e.g., `2026-04-30-pmax-vs-meta-advantage-plus-smb.md`)
- **Template:** start from `_TEMPLATE.md` and delete sections that don't apply.
- **One report = one PM decision.** If a topic spans multiple decisions, split it.

## How to ask for a report

Invoke the agent with a prompt that names:

1. The **PM decision** the research informs.
2. The **lifecycle stage** in scope ([Acquisition] / [Activation] / [Spend] / [Retention] / [ROI]).
3. The **segment** (defaults to SMB-leaning).
4. The **format** you want (structured briefing, long-form report, or comparison table).

Example:
> Use the ads-market-research agent to produce a long-form report comparing AI-driven onboarding flows on Meta Advantage+, Microsoft Copilot in Ads, and Google Ads' Smart Mode for SMB advertisers. Decision: should we prioritize an AI onboarding wizard on business.google.com in H2? Lifecycle: [Activation]. Save to research/.
