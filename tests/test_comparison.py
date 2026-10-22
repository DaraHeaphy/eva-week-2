import contextlib
from datetime import datetime
import io
import subprocess
import sys
import unittest
from unittest.mock import patch

from eva_analysis import compare_countries
from evacodev2 import main
from eva_presentation import display_comparison


def record(year, hours, country):
    return (datetime(year, 1, 1), hours, country)


class ComparisonTests(unittest.TestCase):
    def setUp(self):
        self.records = [record(1999, 100, "USA"), record(2000, 1, "USA"),
                        record(2001, 3, "USA"), record(2000, 2, "Russia"),
                        record(2002, 100, "Russia")]

    def test_known_results_include_both_years_and_exclude_neighbours(self):
        result = compare_countries(self.records, " usa ", "RUSSIA", 2000, 2001)
        self.assertEqual(result["first"], {"country": "USA", "count": 2, "total_hours": 4, "average_hours": 2})
        self.assertEqual(result["second"], {"country": "Russia", "count": 1, "total_hours": 2, "average_hours": 2})
        self.assertEqual(result["winner"], "USA")

    def test_single_year_second_country_wins(self):
        self.assertEqual(compare_countries(self.records, "USA", "Russia", 2000, 2000)["winner"], "Russia")

    def test_no_matches_zero_total_unavailable_average(self):
        result = compare_countries(self.records, "USA", "Russia", 2002, 2002)
        self.assertEqual(result["first"], {"country": "USA", "count": 0, "total_hours": 0, "average_hours": None})
        self.assertEqual(result["winner"], "Russia")
        with contextlib.redirect_stdout(io.StringIO()) as output:
            display_comparison(result)
        self.assertIn("USA: 0 EVAs; total 0.00 hours; average unavailable", output.getvalue())

    def test_empty_period_tie_and_positive_tie(self):
        self.assertIsNone(compare_countries(self.records, "USA", "Russia", 1900, 1901)["winner"])
        equal = [record(2000, 2, "A"), record(2000, 2, "B")]
        self.assertIsNone(compare_countries(equal, "A", "B", 2000, 2000)["winner"])

    def test_float_noise_does_not_break_tie_and_zero_duration_counts(self):
        equal = [record(2000, .1, "A"), record(2000, .2, "A"), record(2000, .3, "B"), record(2000, 0, "B")]
        result = compare_countries(equal, "A", "B", 2000, 2000)
        self.assertIsNone(result["winner"])
        self.assertEqual(result["second"]["count"], 2)
        self.assertAlmostEqual(result["second"]["average_hours"], .15)

    def test_same_country_is_allowed(self):
        self.assertIsNone(compare_countries(self.records, "USA", "USA", 2000, 2001)["winner"])

    def test_invalid_year_inputs(self):
        for start, end in [(2001, 2000), (0, 2000), (2000, 10000), (None, None), ("2000", 2001), (True, 2001)]:
            with self.subTest(start=start, end=end), self.assertRaises(ValueError):
                compare_countries(self.records, "USA", "Russia", start, end)

    def test_unknown_country_blank_and_empty_dataset(self):
        for records, country in [(self.records, "Mars"), (self.records, ""), (self.records, None), ([], "USA")]:
            with self.subTest(country=country), self.assertRaisesRegex(ValueError, "Unknown country"):
                compare_countries(records, country, "Russia", 2000, 2000)

    def test_existing_country_total_is_reused(self):
        from eva_analysis import total_duration_for_country
        with patch("eva_analysis.total_duration_for_country", wraps=total_duration_for_country) as total:
            result = compare_countries(self.records, "USA", "Russia", 2000, 2001)
        self.assertEqual(total.call_count, 2)
        self.assertEqual(result["first"]["total_hours"], 4)


class ComparisonApplicationTests(unittest.TestCase):
    def test_comparison_uses_existing_loader_without_prompt_or_plot(self):
        with patch("builtins.input") as prompt, patch("evacodev2.plot_cumulative_duration") as plot, \
             contextlib.redirect_stdout(io.StringIO()) as output:
            self.assertEqual(main(["--compare", "USA", "Russia", "--start-year", "1965", "--end-year", "2013"]), 0)
        self.assertIn("USA: 217 EVAs; total 1257.13 hours; average 5.79 hours", output.getvalue())
        self.assertIn("Russia: 113 EVAs; total 527.90 hours; average 4.67 hours", output.getvalue())
        self.assertIn("Greater total EVA duration: USA", output.getvalue())
        prompt.assert_not_called()
        plot.assert_not_called()

    def test_bad_comparison_inputs_report_controlled_errors(self):
        for args in [["--compare", "USA", "Russia"],
                     ["--compare", "Mars", "USA", "--start-year", "2000", "--end-year", "2001"],
                     ["--compare", "USA", "Russia", "--start-year", "2010", "--end-year", "2000"]]:
            with self.subTest(args=args), contextlib.redirect_stderr(io.StringIO()) as output:
                self.assertEqual(main(args), 2)
                self.assertIn("Error:", output.getvalue())

    def test_year_options_need_comparison_and_nonnumeric_year_is_controlled(self):
        for args in [["--start-year", "2000"], ["--compare", "USA", "Russia", "--start-year", "bad"]]:
            with self.subTest(args=args), contextlib.redirect_stderr(io.StringIO()) as output, self.assertRaises(SystemExit) as error:
                main(args)
            self.assertEqual(error.exception.code, 2)
            self.assertIn("error:", output.getvalue())

    def test_importing_analysis_and_entry_does_not_need_matplotlib_or_prompt(self):
        program = "import sys; sys.modules['matplotlib'] = None; import eva_analysis; import evacodev2"
        result = subprocess.run([sys.executable, "-B", "-c", program], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout, "")
