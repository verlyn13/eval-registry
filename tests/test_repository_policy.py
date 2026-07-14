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
