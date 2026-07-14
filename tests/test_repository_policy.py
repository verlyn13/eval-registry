from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path
from types import ModuleType

ROOT = Path(__file__).resolve().parents[1]


def load_module(name: str, relative_path: str) -> ModuleType:
    spec = importlib.util.spec_from_file_location(name, ROOT / relative_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {relative_path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


validator = load_module("validate_repository", "scripts/validate_repository.py")
append_only = load_module("check_append_only", "scripts/check_append_only.py")
attestation = load_module(
    "validate_pr_attestation", "scripts/validate_pr_attestation.py"
)

HEAD_SHA = "0123456789abcdef0123456789abcdef01234567"
AUTHOR = "verlyn13"


def valid_attestation_body() -> str:
    declarations = "\n".join(
        f"- [x] {declaration}" for declaration in attestation.REQUIRED_DECLARATIONS
    )
    return (
        f"{attestation.START}\n"
        f"review_mode: {attestation.REVIEW_MODE}\n"
        f"reviewed_by: {AUTHOR}\n"
        f"reviewed_head_sha: {HEAD_SHA}\n\n"
        f"{declarations}\n"
        f"{attestation.END}"
    )


def pull_request_event(body: str | None = None) -> dict[str, object]:
    return {
        "pull_request": {
            "body": valid_attestation_body() if body is None else body,
            "head": {"sha": HEAD_SHA},
            "user": {"login": AUTHOR},
        }
    }


class ExactJsonTests(unittest.TestCase):
    def test_duplicate_keys_are_refused(self) -> None:
        with self.assertRaises(validator.DuplicateKeyError):
            validator.parse_json_text('{"stage":"d2_scaffold","stage":"d3"}')

    def test_nonfinite_numbers_are_refused(self) -> None:
        with self.assertRaises(ValueError):
            validator.parse_json_text('{"value":NaN}')


class AuthorizationTests(unittest.TestCase):
    def test_repository_state_is_exact_d2(self) -> None:
        state = validator.load_json(ROOT / "policy/authorization-state.json")
        self.assertEqual(validator.validate_authorization_state(state), [])

    def test_record_publication_cannot_be_enabled_silently(self) -> None:
        state = validator.load_json(ROOT / "policy/authorization-state.json")
        state["record_publication_approved"] = True
        self.assertNotEqual(validator.validate_authorization_state(state), [])

    def test_historical_v1_shape_is_known_but_not_current(self) -> None:
        historical_v1 = {
            "schema_version": "eval-registry.authorization-state.v1",
            "stage": "d2_scaffold",
            "repository_creation_approved": True,
            "signer_workflow_approved": False,
            "external_authorities_approved": False,
            "record_publication_approved": False,
            "effective_date": "2026-07-13",
        }
        self.assertEqual(
            validator.validate_authorization_state_contract(historical_v1), []
        )
        self.assertNotEqual(validator.validate_authorization_state(historical_v1), [])

    def test_v1_cannot_carry_the_v2_review_field(self) -> None:
        state = validator.load_json(ROOT / "policy/authorization-state.json")
        state["schema_version"] = "eval-registry.authorization-state.v1"
        self.assertNotEqual(validator.validate_authorization_state_contract(state), [])

    def test_v2_requires_the_review_field(self) -> None:
        state = validator.load_json(ROOT / "policy/authorization-state.json")
        del state["pull_request_review_mode"]
        self.assertNotEqual(validator.validate_authorization_state_contract(state), [])

    def test_nonstring_authorization_version_is_refused(self) -> None:
        self.assertNotEqual(
            validator.validate_authorization_state_contract(
                {"schema_version": ["eval-registry.authorization-state.v2"]}
            ),
            [],
        )

    def test_authorization_state_schemas_are_distinct_and_closed(self) -> None:
        v1 = validator.load_json(ROOT / "schemas/authorization-state.v1.schema.json")
        v2 = validator.load_json(ROOT / "schemas/authorization-state.v2.schema.json")
        self.assertFalse(v1["additionalProperties"])
        self.assertFalse(v2["additionalProperties"])
        self.assertEqual(
            set(v1["required"]),
            set(
                validator.AUTHORIZATION_STATE_KEYS[
                    "eval-registry.authorization-state.v1"
                ]
            ),
        )
        self.assertEqual(
            set(v2["required"]),
            set(
                validator.AUTHORIZATION_STATE_KEYS[
                    "eval-registry.authorization-state.v2"
                ]
            ),
        )
        self.assertNotIn("pull_request_review_mode", v1["required"])
        self.assertIn("pull_request_review_mode", v2["required"])

    def test_all_record_namespaces_are_frozen(self) -> None:
        self.assertTrue(
            validator.is_record_path("records/registrations/x/statement.json")
        )
        self.assertTrue(
            validator.is_record_path("records/dispositions/x/statement.json")
        )
        self.assertTrue(validator.is_record_path("trust/policy.json"))
        self.assertFalse(
            validator.is_record_path("schemas/registration-receipt.v1.schema.json")
        )


class SoloMaintainerAttestationTests(unittest.TestCase):
    def test_exact_head_attestation_is_accepted(self) -> None:
        attestation.validate_event(pull_request_event())

    def test_stale_head_is_refused(self) -> None:
        event = pull_request_event()
        pull_request = event["pull_request"]
        assert isinstance(pull_request, dict)
        head = pull_request["head"]
        assert isinstance(head, dict)
        head["sha"] = "f" * 40
        with self.assertRaisesRegex(attestation.AttestationError, "stale"):
            attestation.validate_event(event)

    def test_author_mismatch_is_refused(self) -> None:
        event = pull_request_event()
        pull_request = event["pull_request"]
        assert isinstance(pull_request, dict)
        user = pull_request["user"]
        assert isinstance(user, dict)
        user["login"] = "another-actor"
        with self.assertRaisesRegex(attestation.AttestationError, "author login"):
            attestation.validate_event(event)

    def test_unchecked_declaration_is_refused(self) -> None:
        body = valid_attestation_body().replace(
            "- [x] I reviewed", "- [ ] I reviewed", 1
        )
        with self.assertRaisesRegex(attestation.AttestationError, "unchecked"):
            attestation.validate_event(pull_request_event(body))

    def test_duplicate_block_is_refused(self) -> None:
        body = f"{valid_attestation_body()}\n{valid_attestation_body()}"
        with self.assertRaisesRegex(attestation.AttestationError, "exactly one"):
            attestation.validate_event(pull_request_event(body))


class AppendOnlyTests(unittest.TestCase):
    def test_schema_and_record_modification_is_refused(self) -> None:
        problems = append_only.violations(
            [
                ("M", "schemas/registration-receipt.v1.schema.json"),
                ("D", "records/registrations/x/statement.json"),
            ]
        )
        self.assertEqual(len(problems), 2)

    def test_additions_are_permitted_by_diff_guard(self) -> None:
        self.assertEqual(
            append_only.violations(
                [
                    ("A", "schemas/registration-receipt.v2.schema.json"),
                    ("A", "records/registrations/x/statement.json"),
                ]
            ),
            [],
        )


if __name__ == "__main__":
    unittest.main()
