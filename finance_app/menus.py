"""All CLI menu logic and input handling."""
from datetime import date

from .csv_export import export_to_csv, prompt_export_filename
from .db import DatabaseManager
from .display import clear_screen, print_table, prompt_choice
from .models import CATEGORIES, Transaction, TransactionType
from .reports import summary_flow


# ---------------------------------------------------------------------------
# Input helpers
# ---------------------------------------------------------------------------

def _prompt_float(prompt: str) -> float:
    while True:
        raw = input(prompt).strip()
        try:
            val = float(raw)
            if val > 0:
                return val
        except ValueError:
            pass
        print("  Please enter a positive number (e.g. 42.50).")


def _prompt_date(prompt: str, default: date | None = None) -> date:
    default = default or date.today()
    while True:
        raw = input(f"{prompt} [{default}]: ").strip()
        if not raw:
            return default
        try:
            return date.fromisoformat(raw)
        except ValueError:
            print("  Format: YYYY-MM-DD (e.g. 2026-04-16).")


def _prompt_type() -> TransactionType:
    print("  Transaction type:")
    idx = prompt_choice(["Income", "Expense"])
    return TransactionType.INCOME if idx == 0 else TransactionType.EXPENSE


def _prompt_category(tx_type: TransactionType) -> str:
    cats = CATEGORIES[tx_type]
    print(f"  Category:")
    idx = prompt_choice(cats)
    return cats[idx]


def _prompt_id(db: DatabaseManager, action: str) -> int | None:
    txs = db.get_all(sort_by="date", sort_dir="DESC")
    print_table(txs[:20])
    raw = input(f"  Enter ID to {action} (or Enter to cancel): ").strip()
    if not raw:
        return None
    try:
        tx_id = int(raw)
        if db.get_by_id(tx_id) is not None:
            return tx_id
        print(f"  No transaction with ID {tx_id}.")
    except ValueError:
        print("  Invalid ID.")
    return None


# ---------------------------------------------------------------------------
# Flow functions
# ---------------------------------------------------------------------------

def add_transaction_flow(db: DatabaseManager) -> None:
    print("\n  ADD TRANSACTION")
    tx_type = _prompt_type()
    category = _prompt_category(tx_type)
    amount = _prompt_float("  Amount: $")
    tx_date = _prompt_date("  Date")
    description = input("  Description (optional): ").strip()[:80]

    tx = Transaction(date=tx_date, type=tx_type, category=category,
                     amount=amount, description=description)
    new_id = db.add(tx)
    print(f"  Transaction #{new_id} added successfully.")


def view_transactions_flow(db: DatabaseManager) -> None:
    while True:
        print("\n  VIEW TRANSACTIONS")
        print("  [1] All")
        print("  [2] Income only")
        print("  [3] Expenses only")
        print("  [4] Filter by date range")
        print("  [5] Filter by category")
        print("  [0] Back")
        choice = input("  Choose: ").strip()

        if choice == "1":
            print_table(db.get_all())

        elif choice == "2":
            print_table(db.get_all(type_filter=TransactionType.INCOME))

        elif choice == "3":
            print_table(db.get_all(type_filter=TransactionType.EXPENSE))

        elif choice == "4":
            start = _prompt_date("  Start date", date.today().replace(day=1))
            end = _prompt_date("  End date", date.today())
            print_table(db.get_all(start_date=start, end_date=end))

        elif choice == "5":
            all_cats = CATEGORIES[TransactionType.INCOME] + CATEGORIES[TransactionType.EXPENSE]
            unique_cats = list(dict.fromkeys(all_cats))
            print("  Select category:")
            idx = prompt_choice(unique_cats)
            print_table(db.get_all(category=unique_cats[idx]))

        elif choice == "0":
            break
        else:
            print("  Invalid choice.")


def edit_transaction_flow(db: DatabaseManager) -> None:
    print("\n  EDIT TRANSACTION")
    tx_id = _prompt_id(db, "edit")
    if tx_id is None:
        return

    tx = db.get_by_id(tx_id)
    print(f"\n  Editing transaction #{tx_id} (press Enter to keep current value)")

    # Type
    print(f"  Current type: {tx.type.value}")
    raw = input("  New type [income/expense]: ").strip().lower()
    if raw in ("income", "expense"):
        tx.type = TransactionType(raw)

    # Category
    cats = CATEGORIES[tx.type]
    print(f"  Current category: {tx.category}")
    print("  New category (or Enter to keep):")
    for i, c in enumerate(cats, 1):
        print(f"    [{i}] {c}")
    raw = input(f"  Choose (1-{len(cats)}): ").strip()
    try:
        idx = int(raw) - 1
        if 0 <= idx < len(cats):
            tx.category = cats[idx]
    except ValueError:
        pass

    # Amount
    print(f"  Current amount: ${tx.amount:,.2f}")
    raw = input("  New amount (or Enter to keep): $").strip()
    if raw:
        try:
            val = float(raw)
            if val > 0:
                tx.amount = val
            else:
                print("  Invalid amount; keeping current.")
        except ValueError:
            print("  Invalid amount; keeping current.")

    # Date
    print(f"  Current date: {tx.date}")
    raw = input(f"  New date (YYYY-MM-DD, or Enter to keep) [{tx.date}]: ").strip()
    if raw:
        try:
            tx.date = date.fromisoformat(raw)
        except ValueError:
            print("  Invalid date; keeping current.")

    # Description
    print(f"  Current description: {tx.description!r}")
    raw = input("  New description (or Enter to keep): ").strip()
    if raw:
        tx.description = raw[:80]

    db.update(tx)
    print(f"  Transaction #{tx_id} updated.")


def delete_transaction_flow(db: DatabaseManager) -> None:
    print("\n  DELETE TRANSACTION")
    tx_id = _prompt_id(db, "delete")
    if tx_id is None:
        return

    tx = db.get_by_id(tx_id)
    print_table([tx])
    confirm = input("  Confirm delete? [y/N]: ").strip().lower()
    if confirm == "y":
        db.delete(tx_id)
        print(f"  Transaction #{tx_id} deleted.")
    else:
        print("  Cancelled.")


def export_transactions_flow(db: DatabaseManager) -> None:
    print("\n  EXPORT TRANSACTIONS")
    print("  [1] Export all transactions")
    print("  [2] Export income only")
    print("  [3] Export expenses only")
    print("  [4] Export by date range")
    print("  [0] Cancel")
    choice = input("  Choose: ").strip()

    transactions = None

    if choice == "1":
        transactions = db.get_all(sort_by="date", sort_dir="ASC")
        label = "All transactions"
    elif choice == "2":
        transactions = db.get_all(type_filter=TransactionType.INCOME, sort_by="date", sort_dir="ASC")
        label = "Income transactions"
    elif choice == "3":
        transactions = db.get_all(type_filter=TransactionType.EXPENSE, sort_by="date", sort_dir="ASC")
        label = "Expense transactions"
    elif choice == "4":
        start = _prompt_date("  Start date", date.today().replace(day=1))
        end = _prompt_date("  End date", date.today())
        transactions = db.get_all(start_date=start, end_date=end, sort_by="date", sort_dir="ASC")
        label = f"Transactions from {start} to {end}"
    elif choice == "0":
        return
    else:
        print("  Invalid choice.")
        return

    if not transactions:
        print("  No transactions found to export.")
        return

    try:
        filename = prompt_export_filename()
        filepath = export_to_csv(transactions, filename)
        print(f"  ✓ Successfully exported {len(transactions)} {label} to:")
        print(f"    {filepath}")
    except (ValueError, IOError) as e:
        print(f"  ✗ Export failed: {e}")


# ---------------------------------------------------------------------------
# Main menu
# ---------------------------------------------------------------------------

def main_menu(db: DatabaseManager) -> None:
    while True:
        clear_screen()
        print("=" * 50)
        print("       PERSONAL FINANCE MANAGER")
        print("=" * 50)
        print("  [1] Add Transaction")
        print("  [2] View Transactions")
        print("  [3] Edit Transaction")
        print("  [4] Delete Transaction")
        print("  [5] Summary / Reports")
        print("  [6] Export to CSV")
        print("  [0] Quit")
        print("=" * 50)
        choice = input("  Choose: ").strip()

        if choice == "1":
            add_transaction_flow(db)
        elif choice == "2":
            view_transactions_flow(db)
        elif choice == "3":
            edit_transaction_flow(db)
        elif choice == "4":
            delete_transaction_flow(db)
        elif choice == "5":
            summary_flow(db)
        elif choice == "6":
            export_transactions_flow(db)
        elif choice == "0":
            print("\n  Goodbye!")
            break
        else:
            print("  Invalid choice.")

        if choice != "0":
            input("\n  Press Enter to continue...")
