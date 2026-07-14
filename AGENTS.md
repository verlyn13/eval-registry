# AGENTS.md — Eval Registry Operating Charter

This repository is a public, append-only commitment index. It owns registration-record custody,
schema and verification policy, and public discoverability. It does not own evaluation execution,
model routing, model bytes, deployment reality, evidence analysis, or operational traces.

## Current gate

Only D2 scaffold work is authorized. D3 signer/external-authority setup and D4 record publication
are closed. A proposal, schema, test, or convenient credential never opens either gate.

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

## STOP and escalate if

- work requires any secret, nonce, signer credential, or external trust decision;
- a requested change would publish any record before its publication gate is signed;
- a change would expose private or sensitive content;
- an existing versioned schema or future record would need mutation or deletion; or
- branch protection, signed-history enforcement, or required validation cannot remain fail-closed.
