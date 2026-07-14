# Agent-identity approval roadmap

## Purpose

The current `solo_maintainer_attestation_v1` mode is a transparent, bounded response to a
single-maintainer repository. It preserves review evidence but cannot create actor-separated
approval. This roadmap defines what must be true before an agent can submit or approve a change as
a distinct accountable actor.

This is a governance roadmap, not an activation. No GitHub App, signer, credential, secret, OIDC
permission, external authority, or record publication is authorized by this document.

## Acceptance properties

The successor system must demonstrate all of the following before it can replace the temporary
mode:

1. **Durable actors.** Submitter and approver have distinct, named identities with separate
   least-privilege GitHub App installations or an equivalent non-shared credential boundary.
2. **Policy separation.** One actor, credential, key, installation, workflow run, or delegated
   principal cannot satisfy both roles for the same revision.
3. **Exact-revision binding.** Approval binds repository, pull request, base revision, head SHA,
   policy version, and decision. A new commit invalidates it.
4. **Verifiable receipt.** Identity, authorization result, evidence references, timestamps, and
   the approved revision are retained in a machine-verifiable approval receipt with a readable
   audit view.
5. **Trusted enforcement.** The required approval check runs from trusted base-branch code or an
   independently controlled verifier, not only from mutable pull-request code.
6. **Lifecycle custody.** Issuance, scope, rotation, revocation, expiration, and compromise
   response have named human custody and produce auditable state changes.
7. **Fail-closed adversarial coverage.** Tests refuse stale-head approval, replay across pull
   requests or repositories, same-principal aliases, revoked credentials, ambiguous delegation,
   missing evidence, and policy bypass.
8. **Truthful disclosure.** Public status distinguishes human approval, agent approval,
   solo-maintainer attestation, and automated validation without conflating them.

## Work sequence

### A. Ratify ownership and threat model

- Assign the implementation owner without widening an existing repository charter by convenience.
- Define principal, delegate, submitter, approver, policy authority, credential custodian, and
  incident responder.
- Model shared-token, same-operator, prompt-injection, confused-deputy, replay, stale-revision,
  compromised-app, and base-workflow tampering threats.

### B. Specify the receipt and policy

- Version a closed approval-receipt schema.
- Bind every decision to exact base and head revisions.
- Define eligibility, separation, expiration, revocation, and re-review rules.
- Keep identity evidence separate from evaluation evidence and registration receipts.

### C. Prototype without merge authority

- Run in report-only mode against synthetic pull requests.
- Exercise identity collision, stale-head, replay, and revocation cases.
- Compare the machine receipt with the human-readable GitHub audit trail.

### D. Enforce and supersede

- Obtain explicit operator acceptance of the threat model, identity policy, and credential custody.
- Require the trusted approval check in the default-branch ruleset.
- Demonstrate that no identity can submit and approve the same revision.
- Record the effective date and retire `solo_maintainer_attestation_v1` prospectively. Historical
  self-reviewed pull requests remain labeled as such.

## Current boundary

This roadmap is not on the critical path to D2 maintenance or zero-cost science preparation. It
becomes effective only through a later explicit decision. Until then, pull requests use the
exact-head solo-maintainer attestation and must not claim independent approval.
