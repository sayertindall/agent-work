"""Check that the validator rejects defects in disposable collection copies."""
import importlib.util
import json
from pathlib import Path
import shutil
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('collection_validator', ROOT / 'scripts/validate.py')
validator = importlib.util.module_from_spec(spec)
spec.loader.exec_module(validator)


class ValidatorTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='agent-work-validator-')
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / 'collection'
        shutil.copytree(ROOT, self.root, ignore=shutil.ignore_patterns('.git', '__pycache__'))

    def errors(self):
        return validator.validate(self.root)[0]

    def test_complete_collection_passes(self):
        self.assertEqual(self.errors(), [])

    def test_missing_reference_fails(self):
        (self.root / 'skills/steady/references/repair.md').unlink()
        self.assertTrue(any('broken file link' in e for e in self.errors()))

    def test_wrong_skill_identity_fails(self):
        path = self.root / 'skills/debug/SKILL.md'
        path.write_text(path.read_text().replace('name: debug', 'name: review'))
        errors = self.errors()
        self.assertTrue(any('name must match' in e for e in errors))
        self.assertTrue(any('duplicate name' in e for e in errors))

    def test_missing_evaluation_contract_fails(self):
        (self.root / 'evals/scenarios.json').write_text('[{"id": "missing-fields"}]')
        self.assertTrue(any('evals/scenarios.json' in e for e in self.errors()))

    def test_unknown_scenario_lane_fails(self):
        path = self.root / 'evals/scenarios.json'
        cases = json.loads(path.read_text())
        cases[0]['entry'] = 'steady/missing-lane'
        path.write_text(json.dumps(cases))
        self.assertTrue(any('unknown scenario lane' in e for e in self.errors()))

    def test_external_file_reference_fails(self):
        path = self.root / 'README.md'
        path.write_text(path.read_text() + '\n[Outside](../../outside.md)\n')
        self.assertTrue(any('link escapes repository' in e for e in self.errors()))

    def test_host_specific_frontmatter_fails(self):
        path = self.root / 'skills/debug/SKILL.md'
        path.write_text(path.read_text().replace('name: debug', 'name: debug\nmodel: fixed-model'))
        self.assertTrue(any('use only name and description' in e for e in self.errors()))

    def test_modified_imported_source_fails(self):
        path = self.root / 'skills/interface/references/library/design-taste/GUIDE.md'
        path.write_text(path.read_text() + '\nUnexpected modification.\n')
        self.assertTrue(any('library integrity mismatch' in e for e in self.errors()))

    def test_nested_skill_discovery_fails(self):
        path = self.root / 'skills/interface/references/library/design-taste/SKILL.md'
        path.write_text('# Accidental second entrypoint\n')
        self.assertTrue(any('nested discoverable skill' in e for e in self.errors()))


if __name__ == '__main__':
    unittest.main()
