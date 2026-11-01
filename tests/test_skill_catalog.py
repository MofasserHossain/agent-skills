"""Catalog identity and metadata must survive source organization."""
import json
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
from skill_catalog import ALIASES, discover, validate_interface


class CatalogTests(unittest.TestCase):
    def test_duplicate_installed_names_are_rejected_across_categories(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for category in ('engineering', 'productivity'):
                entry = root / 'skills' / category / 'review' / 'SKILL.md'
                entry.parent.mkdir(parents=True)
                entry.write_text('review')
            with self.assertRaisesRegex(ValueError, 'Duplicate installed skill name'):
                discover(root)

    def test_flat_legacy_and_categorized_sources_keep_names(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for relative in ('skills/grill/SKILL.md', 'skills/engineering/pr/SKILL.md'):
                entry = root / relative
                entry.parent.mkdir(parents=True)
                entry.write_text('skill')
            self.assertEqual(set(discover(root)), {'grill', 'pr'})
            self.assertEqual(ALIASES['pull-request'], 'pr')

    def test_wrong_invocation_in_metadata_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            entry = Path(directory) / 'pr/SKILL.md'
            metadata = entry.parent / 'agents/openai.yaml'
            metadata.parent.mkdir(parents=True)
            fields = {'display_name': 'PR', 'short_description': 'Prepare project-specific pull requests', 'default_prompt': 'Use $pull-request to deliver this change.'}
            metadata.write_text('interface:\n' + ''.join('  '+key+': '+json.dumps(value)+'\n' for key, value in fields.items()))
            with self.assertRaisesRegex(ValueError, 'inconsistent'):
                validate_interface(entry)

    def test_symlink_category_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / 'skills').mkdir()
            (root / 'outside').mkdir()
            (root / 'skills/engineering').symlink_to(root / 'outside', target_is_directory=True)
            with self.assertRaisesRegex(ValueError, 'symlinked'):
                discover(root)
