# Pull request

<!-- solo-maintainer-attestation:v1 -->
review_mode: solo_maintainer_attestation_v1
reviewed_by: REPLACE_WITH_PULL_REQUEST_AUTHOR_LOGIN
reviewed_head_sha: REPLACE_WITH_FULL_40_CHARACTER_HEAD_SHA

- [ ] I reviewed the complete final diff at the recorded head SHA.
- [ ] I reviewed the public-content boundary and found no prohibited private material.
- [ ] I ran or verified the required repository checks for this exact revision.
- [ ] I disclosed scope limits, residual risks, and any unresolved concern.
- [ ] I understand this is solo-maintainer self-review, not independent approval.
<!-- /solo-maintainer-attestation:v1 -->

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
