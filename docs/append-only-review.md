# Append-only review workflow

## Default-branch contract

The default branch uses linear history, signed commits, mandatory pull requests, strict required
validation, resolved review conversations, and disabled force pushes/deletion. Host protection is
review hygiene and discoverability; it is not the cryptographic precedence proof.

GitHub does not allow a pull-request author to approve their own change. This repository currently
has one operator, so D2 enforces the pull-request path with zero required approvals and requires a
recorded self-review as process evidence. That is not independent review and is not represented as
such. Before any record publication, either a second trusted reviewer must make one approval
enforceable or a later operator decision must explicitly accept and bound the self-review weakness.

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
4. carry the review record required by the current authorization state;
5. preserve existing schema and record bytes; and
6. pass a public-boundary review independent of the automated generic scan.

Automated validation and human review are both necessary because neither proves the other's
invariant. In D2, human review is recorded but not independently enforced. A host administrator can
still override host controls; externally held signed bundles are therefore required for future
recovery and verification.

The D2 status check executes workflow and validator code from the proposed revision. Pinning the
required check to the GitHub Actions application does not prove that an unchanged validator emitted
that check. This is acceptable only while record publication is mechanically forbidden. Before any
record publication, append-only enforcement must execute trusted base-branch code (or an
independently controlled verifier), and workflow changes must receive independent approval.
