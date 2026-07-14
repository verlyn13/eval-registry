# Authorization-state versioning

## Contract

`policy/authorization-state.json` is a closed, versioned policy-state contract. Its
`schema_version` selects an immutable schema under `schemas/`. Adding, removing, or changing a
required field is incompatible and requires a new schema version plus a compatibility statement.

The repository validator separately checks two properties:

1. the object has the exact field set for its declared contract version; and
2. the current file is the exact operator-authorized state for this repository.

A historical version may remain a valid historical shape without being an authorized current state.

## Versions

### `eval-registry.authorization-state.v1`

The D2 bootstrap contract at commit `ab79c9c253cb6677fa3d8c0fbb6801241feb7939`. It does not include
a review-mode field.

### `eval-registry.authorization-state.v2`

Adds mandatory `pull_request_review_mode`. The current authorized value is
`solo_maintainer_attestation_v1`; every other D2 authorization value is unchanged.

This is an incompatible closed-shape change. A v1 consumer must upgrade before consuming v2. No
record schema, signer approval, external-authority approval, or record-publication approval changes.

## Transitional correction

Commit `7d53959ec18a3b2c0c24b28ae508fa8c4533e284` briefly added
`pull_request_review_mode` while retaining the v1 identifier. Both validator generations used exact
object equality, so the two shapes were incompatible despite sharing the name. The v2 change records
and corrects that versioning defect; it does not rewrite the transitional commit or pretend it was
compatible.
