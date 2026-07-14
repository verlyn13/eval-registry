# Eval Registry

Eval Registry is a public commitment-plane repository for discoverable, append-only evaluation
registration records. It is intentionally separate from evaluation execution, model serving,
deployment lifecycle, evidence analysis, and trace storage.

## Current authorization state

As of 2026-07-13, only the D2 scaffold is authorized and present:

- the public repository and its charter;
- versioned record schemas;
- a fail-closed verification policy;
- an append-only review policy and validation-only CI; and
- default-branch protection.

The repository is **not operational**. No signer identity, issuer, trust roots, timestamp authority,
or transparency-log endpoint has been selected or configured. No registration receipt,
disposition, incident record, or recovery record may be added. Those actions require later,
separate authorization.

The machine-readable state is [policy/authorization-state.json](policy/authorization-state.json).

## Proof boundary

Git is a reviewable discovery index, not a precedence authority. A future registration package is
valid only when an independent verifier checks all of the following from exact bytes:

1. the signature over the exact statement bytes;
2. the pinned signer identity, issuer, and trust policy;
3. an RFC 3161 timestamp whose message imprint binds the exact signature bytes;
4. transparency-log inclusion against a pinned signed checkpoint; and
5. the package digests and schema constraints.

The verified RFC 3161 time is the sole precedence anchor. Git timestamps, caller-supplied times,
transparency-log integration times, and a package's own `verification_result` are never trust
inputs.

Even a valid future receipt is a self-binding control. It can prove that committed bytes existed
no later than an externally verified time; it cannot prove that no earlier unregistered work or
abandoned attempt existed.

## Public-content boundary

This repository may contain schemas, public verification policy, opaque identifiers, hiding
commitments, and future authorized signed bundles. It must never contain private plans, commitment
nonces, assignment schedules, outcomes, model responses, promotion decisions, secret material,
sensitive system identities, or private workspace/repository names.

## Layout

- `schemas/` — versioned signed-record and verifier-output schemas; published versions are
  immutable.
- `policy/` — machine-readable authorization posture.
- `docs/` — architecture, verification, and append-only review contracts.
- `scripts/` — standard-library-only structural and diff validators.
- `.github/` — validation-only CI and review metadata; no signing workflow exists.

Record, bundle, and trust-policy directories are deliberately absent while the repository is in
`d2_scaffold` state.

## Validate locally

```sh
python3 scripts/validate_repository.py
python3 -m unittest discover -s tests -v
```

No command above contacts an external service.
