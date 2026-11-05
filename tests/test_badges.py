"""Keep repository-hosted badges aligned with package metadata."""

import unittest
from pathlib import Path

from emdashify import __version__


ROOT = Path(__file__).resolve().parents[1]


class BadgeTests(unittest.TestCase):
    def test_pypi_badge_matches_package_version(self):
        svg = (ROOT / "assets/badges/pypi.svg").read_text(encoding="utf-8")
        self.assertIn(f"<title>PyPI: v{__version__}</title>", svg)

    def test_badge_files_and_readme_links(self):
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        for name in ("pypi", "python"):
            path = ROOT / f"assets/badges/{name}.svg"
            self.assertTrue(path.is_file())
            self.assertIn(
                f"https://raw.githubusercontent.com/edujbarrios/EmDashify/main/assets/badges/{name}.svg",
                readme,
            )


if __name__ == "__main__":
    unittest.main()
