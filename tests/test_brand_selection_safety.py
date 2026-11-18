"""Regression tests for selecting one client without directory traversal.

Run: python3 -m unittest tests/test_brand_selection_safety.py
"""
import importlib.util
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, ROOT / path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


context = load("_system/scripts/brand_context.py", "brand_context_safety")
capability = load("_system/scripts/capability.py", "capability_safety")


class BrandSelectionSafety(unittest.TestCase):
    def test_valid_slug_and_active_pointer(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "brands").mkdir()
            (root / "brands" / "active").write_text("client-one\n")
            self.assertEqual(context.resolve_brand_dir(root, None), root / "brands" / "client-one")
            self.assertEqual(capability.resolve_brand_dir(root, None), root / "brands" / "client-one")
            self.assertEqual(context.resolve_brand_dir(root, "other"), root / "brands" / "other")

    def test_rejects_traversal_and_invalid_active_pointer(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "brands").mkdir()
            for slug in ("../elsewhere", "/tmp/elsewhere", ".", "..", "two/parts", "white space"):
                with self.subTest(slug=slug):
                    for fn in (context.resolve_brand_dir, capability.resolve_brand_dir):
                        with self.assertRaises(ValueError):
                            fn(root, slug)
            (root / "brands" / "active").write_text("../outside\n")
            for fn in (context.resolve_brand_dir, capability.resolve_brand_dir):
                with self.assertRaises(ValueError):
                    fn(root, None)

    def test_explicit_brand_dir_rejects_outside_and_nested_paths(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "brands").mkdir()
            (root / "outside").mkdir()
            (root / "brands" / "acme").mkdir()
            for value in ("../outside", "/tmp/outside", "brands/acme/../../outside",
                          "brands/acme/child", "brands/../outside"):
                with self.subTest(value=value):
                    with self.assertRaises(ValueError):
                        capability.validate_brand_dir(root, value)
            self.assertEqual(
                capability.validate_brand_dir(root, "brands/acme").resolve(),
                (root / "brands" / "acme").resolve(),
            )

    def test_explicit_brand_dir_rejects_symlink_escape(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "brands").mkdir()
            (root / "outside").mkdir()
            (root / "brands" / "link").symlink_to(root / "outside", target_is_directory=True)
            with self.assertRaises(ValueError):
                capability.validate_brand_dir(root, "brands/link")

    def test_explicit_brand_dir_rejects_symlink_to_another_client(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "brands" / "client-a").mkdir(parents=True)
            (root / "brands" / "client-b").symlink_to(
                root / "brands" / "client-a", target_is_directory=True
            )
            with self.assertRaises(ValueError):
                capability.validate_brand_dir(root, "brands/client-b")

    def test_rejects_symlink_escape(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "brands").mkdir()
            (root / "outside").mkdir()
            (root / "brands" / "link").symlink_to(root / "outside", target_is_directory=True)
            for fn in (context.resolve_brand_dir, capability.resolve_brand_dir):
                with self.assertRaises(ValueError):
                    fn(root, "link")


if __name__ == "__main__":
    unittest.main()
