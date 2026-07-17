---
title: AGENTS — Operating Charter for eval-registry
category: governance
component: eval-registry
status: active
version: 0.1.0
last_updated: 2026-07-17
tags: [agents, charter, registry, append-only, commitment-index, public]
priority: high
---

# AGENTS.md — Eval Registry Operating Charter

One-line: **a public, append-only commitment index and D2 scaffold — it registers and
verifies records; it must NOT become an evaluation runner, a router, a model store, a
deployment surface, or a live signer/records store before D3/D4 are signed open.**

This repository owns registration-record custody, schema and verification policy, and
public discoverability. It does not own evaluation execution, model routing, model bytes,
deployment reality, evidence analysis, or operational traces.

## Boundaries — this repo owns / does not own

- **Owns:** the registration-record custody contract, the schema and verification policy,
  the authorization-state contract, and public discoverability of the commitment index.
- **Does NOT own:** evaluation execution, model routing, model bytes, deployment reality,
  evidence analysis, or operational traces. Those belong to sibling repos and must never
  be reimplemented or mirrored here.

## Current gate

Only D2 scaffold work is authorized. D3 signer/external-authority setup and D4 record
publication are closed. A proposal, schema, test, or convenient credential never opens
either gate.

## Hard rules

1. **Exact bytes are the artifact.** Signatures and commitments bind exact bytes. No canonical JSON
   reconstruction, reformatting, or semantic-equivalence shortcut may appear in a verification
   path.
2. **Fail closed.** Missing trust-policy values, bundle material, timestamp proof, log inclusion,
   or authorization is a refusal. There is no fallback to Git time, caller time, or log integration
   time.
3. **D2 is record-frozen.** While `policy/authorization-state.json` says `d2_scaffold`, no receipt,
   disposition, incident, recovery, example, fixture, or synthetic record may be committed.
4. **No signer or authority activation.** Do not add signing workflows, OIDC permissions, keys,
   issuer identities, trust roots, timestamp endpoints, or transparency-log endpoints without an
   explicit later authorization.
5. **Public-safe content only.** Never commit private plans, nonces, schedules, outcomes, model
   responses, decisions, credentials, sensitive identities, or private workspace/repository names.
6. **Append only after activation.** Existing files under any future `records/` path may never be
   modified, renamed, or deleted. Corrective information is a new signed record.
7. **Version contracts.** A published schema, authorization-state contract, or trust policy is
   immutable. Incompatible change means a new version and an explicit migration/compatibility
   statement.
8. **Reviewed, signed history.** The default branch requires pull requests, signed commits, linear
   history, and the repository validation check. While there is one eligible maintainer,
   `solo_maintainer_attestation_v1` requires a self-review bound to the exact pull-request head.
   This accepted temporary control is not independent approval and must never be described as
   such. Never bypass a failing check.
9. **No ambient network behavior.** Repository validation is standard-library-only and does not
   contact signers, timestamp authorities, transparency logs, model services, or deployment
   providers.

## Gate parity — local == CI

Run the exact merge gate before claiming done (mirrors `.github/workflows/`):

```bash
python3 scripts/validate_repository.py && python3 -m unittest discover -s tests -v
```

Validation is standard-library-only and must stay fail-closed; never `--no-verify` past a
failing check, and never soften a refusal into a pass to make the gate green.

## Frozen / do-not-edit-in-place

These are byte-exact or contract-pinned; an incidental reformat or value change trips
validation on purpose:

- `policy/authorization-state.json` — exact-equality checked; the current authorization
  state (`d2_scaffold`) is the gate that keeps records frozen. Change it only under an
  explicit, signed D3/D4 authorization, never as a convenience.
- Published schemas and the authorization-state / trust-policy contracts — immutable once
  published. A new version plus a migration/compatibility statement is the only legitimate
  change (Hard rule 7).

## Safe vs held commands

| Safe (returns real output today) | Held / fail-closed (returns refusal or needs authorization) |
|---|---|
| `python3 scripts/validate_repository.py` | committing any receipt/disposition/incident/record — held while state is `d2_scaffold` |
| `python3 -m unittest discover -s tests -v` | adding any signer, OIDC, key, trust root, timestamp, or transparency-log endpoint — held pending D3 |
| reading/editing schemas as new versions | publishing a record — held pending a signed D4 publication gate |

A refusal from a held path is the system working as designed — read the hold/gate
rationale before treating it as a bug.

## Truth lanes (keep separate — do not conflate)

Authoritative state lives in `policy/authorization-state.json` (machine gate), with
`README.md` Status and the D2 scaffold docs as the human-readable lane. Repo docs, git
state, and the authorization-state contract are SEPARATE lanes; do not infer one from
another, and never over-claim a held/planned D3/D4 capability as implemented.

## STOP and escalate if

- work requires any secret, nonce, signer credential, or external trust decision;
- a requested change would publish any record before its publication gate is signed;
- a change would expose private or sensitive content;
- an existing versioned schema or future record would need mutation or deletion; or
- branch protection, signed-history enforcement, or required validation cannot remain fail-closed.

A blocked task reported honestly is success; a guessed-past gate is not.

## Cross-repo

This repository is a public D2 scaffold and is intentionally self-contained: it names no
private repositories and holds no pointers into private workspaces. It shares the public
evidence contract and identity-domain conventions of the public methodology core; downstream
parity is governed there, never by editing frozen constants in place here.
