import contextlib
from datetime import datetime
import io
import json
from pathlib import Path
import unittest
from unittest.mock import patch

from eva_analysis import cumulative_duration, total_duration_for_country
from eva_preparation import prepare_records

ROOT = Path(__file__).resolve().parent.parent


class InheritedCalculationsTests(unittest.TestCase):
    def test_known_cumulative_and_country_results(self):
        records = [(datetime(2000, 1, 1), 1.5, "USA"),
                   (datetime(2000, 2, 1), 2, "Russia"),
                   (datetime(2000, 3, 1), 0.5, "USA")]
        dates, totals = cumulative_duration(records)
        self.assertEqual(dates, [row[0] for row in records])
        self.assertEqual(totals, [1.5, 3.5, 4])
        self.assertEqual(total_duration_for_country(records, "uSa"), 2)
        self.assertEqual(total_duration_for_country(records, "unknown"), 0)

    def test_empty_input(self):
        self.assertEqual(cumulative_duration([]), ([], []))
        self.assertEqual(total_duration_for_country([], "USA"), 0)

    def test_preparation_keeps_tuple_conversion_sort_and_skip_rules(self):
        records = prepare_records([
            {"date": "2001-01-01", "duration": "2:30", "country": "Russia"},
            {"date": "2000-01-01", "duration": "0:00", "country": "USA"},
            {"date": "", "duration": "8:00", "country": "USA"},
            {"date": "2000-01-01"}, {"duration": "1:00"}])
        self.assertEqual(records, [(datetime(2000, 1, 1), 0, "USA"),
                                   (datetime(2001, 1, 1), 2.5, "Russia")])
        self.assertIs(type(records[0]), tuple)

    def test_no_new_validation_policy_was_inserted(self):
        # Original conversion accepts 1:60 as 2 hours. Do not silently tighten it.
        records = prepare_records([{"date": "2000-01-01", "duration": "1:60", "country": "USA"}])
        self.assertEqual(records[0][1], 2)
        with self.assertRaises(ValueError):
            prepare_records([{"date": "bad", "duration": "1:00"}])


class InheritedApplicationTests(unittest.TestCase):
    def test_all_original_points_prompt_text_labels_save_and_show(self):
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        import evacodev2
        baseline = json.loads((ROOT / "docs/evidence/inherited-baseline.json").read_text())
        plt.close("all")
        with patch("builtins.input", return_value="  USA  ") as prompt, \
             patch.object(plt, "savefig") as save, patch.object(plt, "show") as show, \
             contextlib.redirect_stdout(io.StringIO()) as output:
            evacodev2.main()
        axes = plt.gca()
        line = axes.lines[0]
        self.assertEqual([date.isoformat() for date in line.get_xdata()], baseline["dates"])
        self.assertEqual(list(line.get_ydata()), baseline["cumulative_hours"])
        self.assertEqual(output.getvalue(), baseline["stdout"])
        prompt.assert_called_once_with(baseline["prompt"])
        save.assert_called_once_with(baseline["output"])
        self.assertEqual(show.call_count, baseline["show_calls"])
        self.assertEqual(axes.get_xlabel(), baseline["xlabel"])
        self.assertEqual(axes.get_ylabel(), baseline["ylabel"])
        plt.close("all")
