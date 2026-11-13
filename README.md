# Privi DAO — Privi AI Operations & Governance

Privi World Corp's AI-assisted operations and governance project.

## What is implemented
- Read-only public HTTPS endpoint checks with a configurable service inventory (`dao/targets.json`).
- JSON evidence reports and maintenance investigation proposals (`dao/operator.py`).
- Unit tests and a scheduled hourly GitHub Actions monitor.
- No automatic production modifications, token transfers, or wallet signing.

This is the **first operational foundation**, not a deployed on-chain DAO or autonomous AI reasoning service. Monitoring health does not establish mainnet readiness.

## Run
```bash
python3 -m unittest discover -s tests -v
python3 -m dao.operator --config dao/targets.json --output reports/latest.json
```

The GitHub Actions workflow also supports manual invocation. Download each run's `privi-dao-report` artifact to review findings. Scheduled runs start only after the workflow lands on the repository default branch and Actions are enabled.

## Governance guardrails
Privi AI may monitor, summarize, prioritize, and propose. Owner approval is mandatory for deployments, merges, security changes, validator/mainnet changes, token issuance, treasury transfers, and any action using privileged credentials. Future on-chain governance should use a human-controlled multisig, timelock, audit trail, roles, quorum, and emergency pause. No unrestricted AI custody of treasury funds.

## Roadmap
1. Integrate read-only scoped GitHub and Render service health access.
2. Inventory all Privi repos, validators, APIs, websites, and dependencies.
3. Build AI proposal review and evidence dashboard, with human approval controls.
4. Implement audited governance contracts with multisig/timelocks on the production chain after security review and launch readiness.
5. Anchor signed governance receipts to Privi when the mainnet is verified healthy.

Copyright © 2026 Privi World Corp. All rights reserved.
