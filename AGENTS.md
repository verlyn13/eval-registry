# Public evaluation registry agent contract

## Purpose and public boundary

This public repository owns the append-only commitment index, registration schemas, verification policy, authorization-state contract, and public discoverability. It does not own evaluation execution, model routing, model bytes, deployment state, evidence analysis, or operational traces.

The machine-readable authorization state is the gate. A proposal, credential, schema, test, or convenient implementation does not open a signer, external-authority, or record-publication lane.

## Start every task

1. Use the `project-status` skill.
2. Read `policy/authorization-state.json`, `README.md`, `docs/architecture.md`, `docs/verification-policy.md`, and `docs/append-only-review.md`.
3. Inspect the current branch, HEAD, working tree, and relevant diff. Preserve unrelated work.
4. Keep repository bytes, local Git, authorization state, remote review state, and any future external authority as separate evidence lanes.

## Durable rules

- Signatures and commitments bind exact bytes. Never substitute canonical reconstruction or semantic equivalence in a verification path.
- Fail closed when trust policy, authorization, bundle material, timestamp proof, or log inclusion is missing. Do not substitute Git time, caller time, or log integration time.
- While the authorization state keeps record publication closed, do not commit receipts, dispositions, incidents, recovery artifacts, examples, fixtures, synthetic records, or trust material.
- Do not configure a signer, OIDC write permission, key, issuer identity, trust root, timestamp endpoint, or transparency-log endpoint unless the corresponding authorization field is open through its governed process.
- After activation, records are append-only. Corrections are new signed records; never modify, rename, or delete an existing record.
- Published schemas and authorization/trust contracts are immutable. An incompatible change creates a new version plus an explicit migration and compatibility statement.
- Commit public-safe content only. Never include private workspace names, plans, schedules, outcomes, model responses, credentials, nonces, or sensitive identities.
- Preserve reviewed, signed, linear history and exact-head review controls. Never describe self-review as independent approval.

## Engineering policy

Prefer forward migrations through new contract versions and explicit compatibility rules. Do not weaken a validator or roll tooling back to accept an obsolete format. Project agents inherit the user-selected model.

## Validation and handoff

Run:

```bash
python3 scripts/check_agent_contract.py
python3 scripts/validate_repository.py
python3 -m unittest discover -s tests -v
```

Pull requests also run the exact-head attestation and append-only history checks in `.github/workflows/validate.yml`. Report authorization state separately from implementation readiness and external authority state.
