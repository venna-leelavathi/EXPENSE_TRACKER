import csv
import importlib
import os
import tempfile
import unittest
from unittest.mock import patch, call

# Import module with hyphenated name
import importlib.util

spec = importlib.util.spec_from_file_location(
    "expense_tracker",
    os.path.join(os.path.dirname(__file__), "EXPENSE-TRACKER.py"),
)
et = importlib.util.module_from_spec(spec)
spec.loader.exec_module(et)


class _TempCSVTestCase(unittest.TestCase):
    """Base class that redirects FILE_NAME to a temp file for every test."""

    def setUp(self):
        self.tmp = tempfile.NamedTemporaryFile(
            delete=False, suffix=".csv", mode="w", newline=""
        )
        self.tmp.close()
        self._orig_file_name = et.FILE_NAME
        et.FILE_NAME = self.tmp.name

    def tearDown(self):
        et.FILE_NAME = self._orig_file_name
        if os.path.exists(self.tmp.name):
            os.unlink(self.tmp.name)

    # ---- helpers ----
    def _seed_csv(self, rows):
        """Write header + data rows to the temp CSV."""
        with open(et.FILE_NAME, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["id", "date", "description", "amount", "category"])
            for row in rows:
                writer.writerow(row)

    def _read_csv(self):
        """Return all data rows (list of dicts) from the temp CSV."""
        with open(et.FILE_NAME, "r") as f:
            return list(csv.DictReader(f))


# ─────────────────────────────────────────────
# initialize_file
# ─────────────────────────────────────────────
class TestInitializeFile(_TempCSVTestCase):
    def test_creates_file_with_header_when_missing(self):
        os.unlink(self.tmp.name)  # remove so it doesn't exist
        et.initialize_file()
        self.assertTrue(os.path.exists(et.FILE_NAME))
        rows = self._read_csv()
        self.assertEqual(rows, [])  # header only, no data

    def test_does_not_overwrite_existing_file(self):
        self._seed_csv([["1", "2026-01-01", "Lunch", "100", "Food"]])
        et.initialize_file()
        rows = self._read_csv()
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["description"], "Lunch")


# ─────────────────────────────────────────────
# generate_id
# ─────────────────────────────────────────────
class TestGenerateId(unittest.TestCase):
    def test_returns_int(self):
        result = et.generate_id()
        self.assertIsInstance(result, int)

    def test_returns_positive(self):
        self.assertGreater(et.generate_id(), 0)

    def test_based_on_timestamp(self):
        from datetime import datetime as real_dt
        from unittest.mock import MagicMock

        fixed = real_dt(2026, 6, 1, 12, 0, 0)
        orig_datetime = et.datetime
        mock_dt = MagicMock(wraps=real_dt)
        mock_dt.now.return_value = fixed
        et.datetime = mock_dt
        try:
            self.assertEqual(et.generate_id(), int(fixed.timestamp()))
        finally:
            et.datetime = orig_datetime


# ─────────────────────────────────────────────
# add_expense
# ─────────────────────────────────────────────
class TestAddExpense(_TempCSVTestCase):
    def setUp(self):
        super().setUp()
        self._seed_csv([])  # empty CSV with header

    @patch("builtins.input", side_effect=["2026-03-14", "Lunch", "120", "Food"])
    @patch("builtins.print")
    def test_adds_valid_expense(self, mock_print, mock_input):
        et.add_expense()
        rows = self._read_csv()
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["date"], "2026-03-14")
        self.assertEqual(rows[0]["description"], "Lunch")
        self.assertEqual(rows[0]["amount"], "120.0")
        self.assertEqual(rows[0]["category"], "Food")
        mock_print.assert_called_with("Expense added successfully")

    @patch("builtins.input", side_effect=["2026-03-14", "Lunch", "not_a_number", "Food"])
    @patch("builtins.print")
    def test_rejects_non_numeric_amount(self, mock_print, mock_input):
        et.add_expense()
        rows = self._read_csv()
        self.assertEqual(len(rows), 0)
        mock_print.assert_called_with("Amount must be numeric")

    @patch("builtins.input", side_effect=["2026-03-14", "Lunch", "50", ""])
    @patch("builtins.print")
    def test_rejects_empty_category(self, mock_print, mock_input):
        et.add_expense()
        rows = self._read_csv()
        self.assertEqual(len(rows), 0)
        mock_print.assert_called_with("Category cannot be empty")

    @patch("builtins.input", side_effect=["2026-03-14", "Lunch", "50", "   "])
    @patch("builtins.print")
    def test_rejects_whitespace_only_category(self, mock_print, mock_input):
        et.add_expense()
        rows = self._read_csv()
        self.assertEqual(len(rows), 0)
        mock_print.assert_called_with("Category cannot be empty")


# ─────────────────────────────────────────────
# view_expenses
# ─────────────────────────────────────────────
class TestViewExpenses(_TempCSVTestCase):
    @patch("builtins.print")
    def test_displays_all_expenses_and_totals(self, mock_print):
        self._seed_csv([
            ["1", "2026-03-14", "Lunch", "120", "Food"],
            ["2", "2026-03-15", "Bus", "50", "Transport"],
        ])
        et.view_expenses()
        # Check that each row was printed
        mock_print.assert_any_call("1", "2026-03-14", "Lunch", "120", "Food")
        mock_print.assert_any_call("2", "2026-03-15", "Bus", "50", "Transport")
        mock_print.assert_any_call("Total Expenses:", 2)
        mock_print.assert_any_call("Total Amount:", 170.0)

    @patch("builtins.print")
    def test_empty_file_shows_zero_totals(self, mock_print):
        self._seed_csv([])
        et.view_expenses()
        mock_print.assert_any_call("Total Expenses:", 0)
        mock_print.assert_any_call("Total Amount:", 0)


# ─────────────────────────────────────────────
# search_category
# ─────────────────────────────────────────────
class TestSearchCategory(_TempCSVTestCase):
    def setUp(self):
        super().setUp()
        self._seed_csv([
            ["1", "2026-03-14", "Lunch", "120", "Food"],
            ["2", "2026-03-15", "Bus", "50", "Transport"],
            ["3", "2026-03-16", "Dinner", "200", "Food"],
        ])

    @patch("builtins.input", return_value="Food")
    @patch("builtins.print")
    def test_finds_matching_category(self, mock_print, mock_input):
        et.search_category()
        mock_print.assert_any_call("1", "2026-03-14", "Lunch", "120", "Food")
        mock_print.assert_any_call("3", "2026-03-16", "Dinner", "200", "Food")
        mock_print.assert_any_call("Subtotal for category:", 320.0)

    @patch("builtins.input", return_value="food")
    @patch("builtins.print")
    def test_case_insensitive_search(self, mock_print, mock_input):
        et.search_category()
        mock_print.assert_any_call("Subtotal for category:", 320.0)

    @patch("builtins.input", return_value="Entertainment")
    @patch("builtins.print")
    def test_no_matches_shows_zero_subtotal(self, mock_print, mock_input):
        et.search_category()
        mock_print.assert_any_call("Subtotal for category:", 0)


# ─────────────────────────────────────────────
# monthly_total
# ─────────────────────────────────────────────
class TestMonthlyTotal(_TempCSVTestCase):
    def setUp(self):
        super().setUp()
        self._seed_csv([
            ["1", "2026-03-14", "Lunch", "120", "Food"],
            ["2", "2026-03-15", "Bus", "50", "Transport"],
            ["3", "2026-04-01", "Dinner", "200", "Food"],
        ])

    @patch("builtins.input", return_value="2026-03")
    @patch("builtins.print")
    def test_sums_correct_month(self, mock_print, mock_input):
        et.monthly_total()
        mock_print.assert_called_with("Total expenses for", "2026-03", "=", 170.0)

    @patch("builtins.input", return_value="2026-04")
    @patch("builtins.print")
    def test_different_month(self, mock_print, mock_input):
        et.monthly_total()
        mock_print.assert_called_with("Total expenses for", "2026-04", "=", 200.0)

    @patch("builtins.input", return_value="2025-01")
    @patch("builtins.print")
    def test_no_expenses_in_month(self, mock_print, mock_input):
        et.monthly_total()
        mock_print.assert_called_with("Total expenses for", "2025-01", "=", 0)


# ─────────────────────────────────────────────
# delete_expense
# ─────────────────────────────────────────────
class TestDeleteExpense(_TempCSVTestCase):
    def setUp(self):
        super().setUp()
        self._seed_csv([
            ["100", "2026-03-14", "Lunch", "120", "Food"],
            ["200", "2026-03-15", "Bus", "50", "Transport"],
        ])

    @patch("builtins.input", return_value="100")
    @patch("builtins.print")
    def test_deletes_existing_expense(self, mock_print, mock_input):
        et.delete_expense()
        rows = self._read_csv()
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["id"], "200")
        mock_print.assert_called_with("Expense deleted successfully")

    @patch("builtins.input", return_value="999")
    @patch("builtins.print")
    def test_id_not_found(self, mock_print, mock_input):
        et.delete_expense()
        rows = self._read_csv()
        self.assertEqual(len(rows), 2)
        mock_print.assert_called_with("ID not found")

    @patch("builtins.input", return_value="200")
    @patch("builtins.print")
    def test_csv_rewritten_correctly_after_delete(self, mock_print, mock_input):
        et.delete_expense()
        rows = self._read_csv()
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["description"], "Lunch")


# ─────────────────────────────────────────────
# run (menu loop)
# ─────────────────────────────────────────────
class TestRun(_TempCSVTestCase):
    @patch("builtins.input", side_effect=["6"])
    @patch("builtins.print")
    def test_exit_immediately(self, mock_print, mock_input):
        os.unlink(self.tmp.name)
        et.run()
        mock_print.assert_any_call("Exiting program")
        self.assertTrue(os.path.exists(et.FILE_NAME))

    @patch("builtins.input", side_effect=["9", "6"])
    @patch("builtins.print")
    def test_invalid_choice_then_exit(self, mock_print, mock_input):
        os.unlink(self.tmp.name)
        et.run()
        mock_print.assert_any_call("Invalid choice")
        mock_print.assert_any_call("Exiting program")

    @patch(
        "builtins.input",
        side_effect=[
            "1",  # Add Expense
            "2026-06-01", "Coffee", "5", "Food",
            "6",  # Exit
        ],
    )
    @patch("builtins.print")
    def test_add_then_exit(self, mock_print, mock_input):
        self._seed_csv([])
        et.run()
        rows = self._read_csv()
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["description"], "Coffee")

    @patch(
        "builtins.input",
        side_effect=[
            "2",  # View All
            "6",  # Exit
        ],
    )
    @patch("builtins.print")
    def test_view_then_exit(self, mock_print, mock_input):
        self._seed_csv([["1", "2026-01-01", "Test", "10", "Misc"]])
        et.run()
        mock_print.assert_any_call("Total Expenses:", 1)

    @patch(
        "builtins.input",
        side_effect=[
            "3",  # Search
            "Food",
            "6",  # Exit
        ],
    )
    @patch("builtins.print")
    def test_search_then_exit(self, mock_print, mock_input):
        self._seed_csv([["1", "2026-01-01", "Lunch", "100", "Food"]])
        et.run()
        mock_print.assert_any_call("Subtotal for category:", 100.0)

    @patch(
        "builtins.input",
        side_effect=[
            "4",  # Monthly Total
            "2026-01",
            "6",  # Exit
        ],
    )
    @patch("builtins.print")
    def test_monthly_total_then_exit(self, mock_print, mock_input):
        self._seed_csv([["1", "2026-01-15", "Rent", "500", "Housing"]])
        et.run()
        mock_print.assert_any_call("Total expenses for", "2026-01", "=", 500.0)

    @patch(
        "builtins.input",
        side_effect=[
            "5",  # Delete
            "1",
            "6",  # Exit
        ],
    )
    @patch("builtins.print")
    def test_delete_then_exit(self, mock_print, mock_input):
        self._seed_csv([["1", "2026-01-01", "Lunch", "100", "Food"]])
        et.run()
        mock_print.assert_any_call("Expense deleted successfully")
        rows = self._read_csv()
        self.assertEqual(len(rows), 0)


if __name__ == "__main__":
    unittest.main()
