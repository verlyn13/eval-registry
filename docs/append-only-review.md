# Append-only review workflow

## Default-branch contract

The default branch uses linear history, signed commits, mandatory pull requests, strict required
validation, resolved review conversations, and disabled force pushes/deletion. Host protection is
review hygiene and discoverability; it is not the cryptographic precedence proof.

GitHub does not allow a pull-request author to approve their own change. This repository currently
has one operator, so D2 enforces the pull-request path with zero required approvals and requires a
recorded self-review as process evidence. The accepted temporary mode is
`solo_maintainer_attestation_v1`. That is not independent review and is never represented as such.
The missing second human is an accepted residual risk and does not independently block a later
publication decision. All other authorization, verification, trusted-base, append-only, and
public-boundary gates remain closed until separately satisfied.

The initial D2 scaffold is a single signed bootstrap commit pushed before protection can exist on a
new empty repository. It contains no record instances. Protection is applied immediately after that
bootstrap and is part of D2 closeout.

## D2 freeze

While `policy/authorization-state.json` is `d2_scaffold`:

- no path under `records/` may exist;
- CI has read-only repository permissions and no OIDC token permission;
- no workflow may sign, timestamp, contact a transparency log, or resolve a secret; and
- changing the authorization state requires a separately recorded operator decision.

## Future append-only paths

Later authorizations may create these dedicated namespaces:

- `records/registrations/`
- `records/dispositions/`
- `records/incidents/`
- `records/recovery/`

Once created, files under `records/` are immutable: additions only, with no edits, renames,
type-changes, or deletions. Corrections and revocations are new signed records referring to the
prior record. Versioned schemas are likewise add-only; an incompatible contract gets a new file.

## Review requirements

Every change must:

1. arrive through a pull request;
2. have a signed commit and linear-history merge;
3. pass the `validate` status check;
4. carry the review record required by the current authorization state, bound to the exact current
   pull-request head SHA;
5. preserve existing schema and record bytes; and
6. pass a public-boundary review independent of the automated generic scan.

Automated validation and human review are both necessary because neither proves the other's
invariant. In D2, the sole maintainer performs and records the human review; actor separation is not
available. Every pull-request body must contain exactly one `solo-maintainer-attestation:v1` block
whose `reviewed_by` value is the pull-request author, whose `reviewed_head_sha` is the current
40-character head SHA, and whose declarations are checked. A later push invalidates the prior
attestation and required validation fails until the body is updated. A host administrator can still
override host controls; externally held signed bundles are therefore required for future recovery
and verification.

The D2 status check executes workflow and validator code from the proposed revision. Pinning the
required check to the GitHub Actions application does not prove that an unchanged validator emitted
that check. In D2, publication remains explicitly unauthorized and the current validator refuses
record paths, but mutable pull-request code is not trusted mechanical enforcement. Before any record
publication, append-only enforcement must execute trusted base-branch code (or an independently
controlled verifier). The temporary self-review model does not satisfy or weaken that trusted-base
requirement.

The pull-request body remains editable and is process evidence, not a durable approval receipt.
The check validates that the declaration matched the event head at check time; it cannot prove the
declared review occurred or stop later body edits. The successor system must retain a separate,
exact-revision approval receipt.

## Successor review system

The temporary mode ends only after an accepted agent-identity approval system provides distinct
submitter and approver identities, separate least-privilege credentials, exact-head binding,
machine-verifiable approval receipts, revocation and compromise handling, and fail-closed tests for
stale heads, replay, identity collision, and policy bypass. Two agent labels or two model sessions
without durable identity and credential separation do not qualify. The detailed acceptance path is
documented in [agent-identity-approval-roadmap.md](agent-identity-approval-roadmap.md).
