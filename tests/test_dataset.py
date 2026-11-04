"""Data-integrity checks for the version-controlled sovereign yield sample.

Run from repository root: python -m unittest discover -s tests -v
These tests validate input shape and ranges, not regression inference.
"""
import csv
import math
import unittest
from pathlib import Path

DATA_FILE = Path(__file__).resolve().parents[1] / "bond_yield_data.csv"


class SovereignDatasetTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with DATA_FILE.open(encoding="utf-8", newline="") as handle:
            reader = csv.DictReader(handle)
            cls.columns = reader.fieldnames
            cls.rows = list(reader)

    def test_expected_columns(self):
        self.assertEqual(self.columns, ["Country", "Yield", "Debt", "Inflation", "Rating"])

    def test_fifty_unique_countries(self):
        self.assertEqual(len(self.rows), 50)
        names = [row["Country"].strip() for row in self.rows]
        self.assertTrue(all(names))
        self.assertEqual(len(set(names)), len(names))

    def test_numeric_inputs_finite_and_positive_for_log_transforms(self):
        for row in self.rows:
            for key in ("Yield", "Debt", "Inflation", "Rating"):
                with self.subTest(country=row["Country"], field=key):
                    value = float(row[key])
                    self.assertTrue(math.isfinite(value))
                    self.assertGreater(value, 0.0)

    def test_yield_summary_matches_documented_sample(self):
        yields = sorted(float(row["Yield"]) for row in self.rows)
        self.assertAlmostEqual(min(yields), 0.9, places=6)
        self.assertAlmostEqual(max(yields), 55.0, places=6)
        self.assertAlmostEqual((yields[24] + yields[25]) / 2, 4.3, places=6)
        self.assertAlmostEqual(sum(yields) / len(yields), 7.78, delta=0.05)


if __name__ == "__main__":
    unittest.main()
