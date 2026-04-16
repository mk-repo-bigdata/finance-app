"""Terminal display helpers — no external dependencies."""
import os
from typing import List

from .models import Transaction, TransactionType

# Column widths
_W_ID   = 5
_W_DATE = 12
_W_TYPE = 9
_W_CAT  = 15
_W_AMT  = 12
_W_DESC = 28

_TOTAL_WIDTH = _W_ID + _W_DATE + _W_TYPE + _W_CAT + _W_AMT + _W_DESC + 5  # 5 separators


def clear_screen() -> None:
    os.system("cls" if os.name == "nt" else "clear")


def _sep(char: str = "-") -> str:
    return char * _TOTAL_WIDTH


def _trunc(text: str, width: int) -> str:
    if len(text) > width:
        return text[: width - 1] + ">"
    return text


def format_amount(amount: float, tx_type: TransactionType) -> str:
    sign = "+" if tx_type == TransactionType.INCOME else "-"
    return f"{sign}${amount:,.2f}"


def print_table(transactions: List[Transaction]) -> None:
    header = (
        "ID".rjust(_W_ID) + " "
        + "Date".ljust(_W_DATE) + " "
        + "Type".ljust(_W_TYPE) + " "
        + "Category".ljust(_W_CAT) + " "
        + "Amount".rjust(_W_AMT) + " "
        + "Description".ljust(_W_DESC)
    )
    print(_sep())
    print(header)
    print(_sep())

    if not transactions:
        msg = "No transactions found."
        print(msg.center(_TOTAL_WIDTH))
    else:
        for tx in transactions:
            amt_str = format_amount(tx.amount, tx.type)
            row = (
                str(tx.id).rjust(_W_ID) + " "
                + tx.date.isoformat().ljust(_W_DATE) + " "
                + tx.type.value.ljust(_W_TYPE) + " "
                + _trunc(tx.category, _W_CAT).ljust(_W_CAT) + " "
                + amt_str.rjust(_W_AMT) + " "
                + _trunc(tx.description, _W_DESC).ljust(_W_DESC)
            )
            print(row)

    print(_sep())


def print_summary(income: float, expenses: float) -> None:
    balance = income - expenses
    bal_str = f"${balance:,.2f}" if balance >= 0 else f"-${abs(balance):,.2f} !!!"
    print(_sep())
    print(f"  {'Total Income':<20} {'$' + f'{income:,.2f}':>15}")
    print(f"  {'Total Expenses':<20} {'-$' + f'{expenses:,.2f}':>15}")
    print(_sep("─"))
    print(f"  {'Balance':<20} {bal_str:>15}")
    print(_sep())


def prompt_choice(options: List[str], prompt: str = "Choose") -> int:
    """Print numbered options and return 0-based index of chosen item."""
    for i, opt in enumerate(options, 1):
        print(f"  [{i}] {opt}")
    while True:
        raw = input(f"{prompt} (1-{len(options)}): ").strip()
        try:
            idx = int(raw) - 1
            if 0 <= idx < len(options):
                return idx
        except ValueError:
            pass
        print(f"  Please enter a number between 1 and {len(options)}.")
