# Verification policy

## Status

This is the D2 verification contract, not an operational trust policy. No signer identity, issuer,
trust root, timestamp authority, or transparency-log endpoint is configured. Verification of a
record therefore must refuse in the current `d2_scaffold` state.

## Required verification sequence

When a later authorization installs a versioned trust policy, an independent verifier must perform
the following checks in order and fail closed on any error:

1. Read `receipt.json` (or a separately authorized disposition record) as exact bytes. Reject
   duplicate JSON keys, non-finite numbers, schema violations, extra fields, and unsupported schema
   versions. Never serialize it again for signature verification.
2. Compute SHA-256 over those exact bytes. This is `registration_receipt_sha256` for a registration
   receipt.
3. Read `signature.bundle.json` as exact bytes and compute its SHA-256.
4. Verify that the bundle signature covers the exact signed-record bytes.
5. Require exact equality with the pinned signer identity and exact issuer in the named trust-
   policy version. Wildcards, regex matching, and same-organization substitutions are forbidden.
6. Verify the signing certificate chain against pinned trust roots.
7. Recompute the RFC 3161 message imprint from the exact signature bytes, verify the timestamp
   token and allowed digest algorithm, chain it to the pinned timestamp root, and require its
   verified `genTime` to fall within the signing certificate's validity interval. A timestamp over
   payload bytes is invalid.
8. Verify transparency-log inclusion by recomputing the Merkle root and checking the signed
   checkpoint against the pinned log key. Integration time is metadata, never a precedence time.
9. Validate package structure and independently recompute the result. Ignore referenced
   `verification.json` as a trust input.

No fallback exists to Git commit time, filesystem time, a caller's `registered_at`, an unchecked
log field, live network lookup, or best-effort identity matching.

## Two-anchor claim

Registration verification alone does not prove that registration preceded evidence collection.
That claim requires an independently verified evidence signature/timestamp that binds the exact
registration receipt digest. Only verified `T_receipt < T_evidence` supports the bounded precedence
claim. It still does not prove that no unregistered computation occurred earlier.

## D3 inputs still required

A later operator decision must name the exact signer identity, OIDC issuer, trust roots, timestamp
authority, transparency-log endpoint/key, bundle format, and trust-policy version. Until all are
present and reviewed together, a verifier result is `refused`, not `verified`.
