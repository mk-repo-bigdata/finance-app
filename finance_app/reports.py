"""Summary computations and text bar chart rendering."""
from datetime import date
from typing import Dict, List

from .db import DatabaseManager
from .display import print_summary

def _sep(char: str = "-", width: int = 55) -> str:
    return char * width
from .models import Transaction, TransactionType

_BAR_WIDTH = 20


def compute_summary(transactions: List[Transaction]) -> Dict:
    income = sum(t.amount for t in transactions if t.type == TransactionType.INCOME)
    expenses = sum(t.amount for t in transactions if t.type == TransactionType.EXPENSE)
    by_category: Dict[str, float] = {}
    for t in transactions:
        if t.type == TransactionType.EXPENSE:
            by_category[t.category] = by_category.get(t.category, 0.0) + t.amount
    return {"income": income, "expenses": expenses, "balance": income - expenses, "by_category": by_category}


def print_category_bar_chart(by_category: Dict[str, float], total: float) -> None:
    if not by_category:
        print("  No expense data available.")
        return

    max_amt = max(by_category.values())
    print(_sep())
    print("  Expenses by Category")
    print(_sep())
    for cat, amt in sorted(by_category.items(), key=lambda x: x[1], reverse=True):
        filled = round(_BAR_WIDTH * amt / max_amt) if max_amt > 0 else 0
        bar = "#" * filled + "." * (_BAR_WIDTH - filled)
        pct = (amt / total * 100) if total > 0 else 0
        print(f"  {cat:<15} {bar}  ${amt:>9,.2f}  {pct:5.1f}%")
    print(_sep())
    print(f"  {'Total':<15} {'':20}  ${total:>9,.2f}")
    print(_sep())


def _get_and_show(db: DatabaseManager, start: date | None, end: date | None, label: str) -> None:
    txs = db.get_all(start_date=start, end_date=end, sort_by="date", sort_dir="ASC")
    data = compute_summary(txs)
    print(f"\n  --- {label} ---")
    print_summary(data["income"], data["expenses"])


def summary_flow(db: DatabaseManager) -> None:
    while True:
        print("\n  SUMMARY / REPORTS")
        print("  [1] Overall balance")
        print("  [2] This month")
        print("  [3] Custom date range")
        print("  [4] Expenses by category")
        print("  [0] Back")
        choice = input("  Choose: ").strip()

        if choice == "1":
            _get_and_show(db, None, None, "All Time")

        elif choice == "2":
            today = date.today()
            start = today.replace(day=1)
            _get_and_show(db, start, today, f"{today.strftime('%B %Y')}")

        elif choice == "3":
            start = _prompt_date("  Start date (YYYY-MM-DD): ")
            end = _prompt_date("  End date   (YYYY-MM-DD): ")
            if start and end:
                _get_and_show(db, start, end, f"{start} to {end}")

        elif choice == "4":
            txs = db.get_all(type_filter=TransactionType.EXPENSE)
            data = compute_summary(txs)
            print()
            print_category_bar_chart(data["by_category"], data["expenses"])

        elif choice == "0":
            break
        else:
            print("  Invalid choice.")


def _prompt_date(prompt: str) -> date | None:
    while True:
        raw = input(prompt).strip()
        if not raw:
            return None
        try:
            return date.fromisoformat(raw)
        except ValueError:
            print("  Format: YYYY-MM-DD (e.g. 2026-04-16)")
