# Pull request

## Scope

- [ ] This change stays within the registry's public commitment-plane charter.
- [ ] The authorization state permits every proposed action.
- [ ] No private plan, nonce, schedule, outcome, response, decision, secret, sensitive identity,
      or private workspace/repository name is present.

## Immutability

- [ ] No existing versioned schema or record byte is modified, renamed, or deleted.
- [ ] Any future record addition is covered by the required signer/publication authorizations.
- [ ] Corrections are represented as new append-only records.

## Verification

- [ ] `python3 scripts/validate_repository.py`
- [ ] `python3 -m unittest discover -s tests -v`
- [ ] The diff received a separate public-boundary review.
