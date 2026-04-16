"""Data models and constants for the personal finance app."""
from dataclasses import dataclass
from datetime import date
from enum import Enum


class TransactionType(str, Enum):
    INCOME = "income"
    EXPENSE = "expense"


CATEGORIES = {
    TransactionType.INCOME: ["Salary", "Freelance", "Investment", "Gift", "Other"],
    TransactionType.EXPENSE: [
        "Food", "Housing", "Transport", "Health",
        "Entertainment", "Utilities", "Shopping", "Other",
    ],
}


@dataclass
class Transaction:
    date: date
    type: TransactionType
    category: str
    amount: float        # always positive
    description: str
    id: int | None = None  # None before INSERT

    def signed_amount(self) -> float:
        return self.amount if self.type == TransactionType.INCOME else -self.amount
