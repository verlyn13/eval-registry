# Architecture and package boundary

Eval Registry is one deliberately narrow plane: public custody and discovery of future signed,
append-only registration records. It does not observe runs and therefore cannot manufacture model,
deployment, outcome, or evidence facts.

## Receipt package

A future registration receipt is a three-file package:

1. `receipt.json` — the exact bytes signed by the authorized identity. Its contents conform to
   `registration-receipt.v1.schema.json` and carry fixed relative references to the two sidecars.
2. `signature.bundle.json` — the sidecar signature/timestamp/transparency bundle over those exact
   receipt bytes.
3. `verification.json` — informational verifier output conforming to
   `verification-result.v1.schema.json`.

This split avoids a circular construction: a signature bundle cannot be embedded in the bytes that
the same bundle signs. Fixed relative sidecar paths are signed, but sidecar content and digests are
not embedded in `receipt.json`. The verifier never reconstructs or canonicalizes the receipt. It
reads its bytes as stored. `registration_receipt_sha256` is SHA-256 of exact `receipt.json` bytes.

The referenced `verification.json` is an index aid, not a trust root. Its `authoritative` field is
fixed to `false`. A consumer must independently verify the exact receipt and bundle and recompute
all digests and checks.

## Hiding commitments

Private or low-entropy inputs use:

```text
HMAC-SHA256(key=nonce, msg=domain || exact_file_bytes)
```

The nonce is at least 256 CSPRNG bits and is never registry content. The exact UTF-8 domain byte
strings, each ending in one NUL byte, are:

- plan: `eval-registry.plan.v1\0`
- task set: `eval-registry.task-set.v1\0`
- campaign family: `eval-registry.campaign-family.v1\0`

Plan and task-set nonces are fresh per commitment. A campaign-family nonce is deliberately stable
within one family so its public commitment remains stable across attempt ordinals. Reveal
verification takes the original exact bytes and nonce; nonce loss is permanent unverifiability,
never permission to regenerate a replacement.

## Dispositions

A disposition is a separate signed package, never a field added to a registration receipt. Its
terminal value is `reported`, `abandoned`, or `aborted`; the latter two require a public-safe
reason. Disposition publication remains unauthorized in the current D2 state.

## Evidence precedence

A future valid receipt establishes at most `T_receipt`, the RFC 3161 time verified over the exact
signature bytes. A receipt-before-evidence claim additionally requires a separately signed and
timestamped evidence bundle that binds the exact receipt digest, producing verified
`T_evidence`, with `T_receipt < T_evidence`. Neither side may substitute a self-asserted time.
