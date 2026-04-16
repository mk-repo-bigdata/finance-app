"""SQLite database layer for the personal finance app."""
import sqlite3
from datetime import date
from pathlib import Path
from typing import Optional

from .models import Transaction, TransactionType

DB_PATH = Path(__file__).parent.parent / "data" / "finance.db"

_SCHEMA = """
CREATE TABLE IF NOT EXISTS transactions (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    date        TEXT    NOT NULL,
    type        TEXT    NOT NULL CHECK(type IN ('income','expense')),
    category    TEXT    NOT NULL,
    amount      REAL    NOT NULL CHECK(amount > 0),
    description TEXT    NOT NULL DEFAULT ''
);
"""


class DatabaseManager:
    def __init__(self, db_path: Path = DB_PATH) -> None:
        db_path.parent.mkdir(parents=True, exist_ok=True)
        self._conn = sqlite3.connect(str(db_path))
        self._conn.row_factory = sqlite3.Row
        self._init_schema()

    def _init_schema(self) -> None:
        with self._conn:
            self._conn.executescript(_SCHEMA)

    def _row_to_tx(self, row: sqlite3.Row) -> Transaction:
        return Transaction(
            id=row["id"],
            date=date.fromisoformat(row["date"]),
            type=TransactionType(row["type"]),
            category=row["category"],
            amount=row["amount"],
            description=row["description"],
        )

    def add(self, tx: Transaction) -> int:
        with self._conn:
            cur = self._conn.execute(
                "INSERT INTO transactions (date, type, category, amount, description) "
                "VALUES (?, ?, ?, ?, ?)",
                (tx.date.isoformat(), tx.type.value, tx.category, tx.amount, tx.description),
            )
        return cur.lastrowid

    def get_all(
        self,
        type_filter: Optional[TransactionType] = None,
        category: Optional[str] = None,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
        sort_by: str = "date",
        sort_dir: str = "DESC",
    ) -> list[Transaction]:
        allowed_sort = {"date", "amount", "category", "id"}
        allowed_dir = {"ASC", "DESC"}
        sort_by = sort_by if sort_by in allowed_sort else "date"
        sort_dir = sort_dir.upper() if sort_dir.upper() in allowed_dir else "DESC"

        conditions: list[str] = []
        params: list = []

        if type_filter is not None:
            conditions.append("type = ?")
            params.append(type_filter.value)
        if category is not None:
            conditions.append("category = ?")
            params.append(category)
        if start_date is not None:
            conditions.append("date >= ?")
            params.append(start_date.isoformat())
        if end_date is not None:
            conditions.append("date <= ?")
            params.append(end_date.isoformat())

        where = ("WHERE " + " AND ".join(conditions)) if conditions else ""
        sql = f"SELECT * FROM transactions {where} ORDER BY {sort_by} {sort_dir}"
        rows = self._conn.execute(sql, params).fetchall()
        return [self._row_to_tx(r) for r in rows]

    def get_by_id(self, tx_id: int) -> Optional[Transaction]:
        row = self._conn.execute(
            "SELECT * FROM transactions WHERE id = ?", (tx_id,)
        ).fetchone()
        return self._row_to_tx(row) if row else None

    def update(self, tx: Transaction) -> None:
        with self._conn:
            self._conn.execute(
                "UPDATE transactions SET date=?, type=?, category=?, amount=?, description=? "
                "WHERE id=?",
                (tx.date.isoformat(), tx.type.value, tx.category, tx.amount, tx.description, tx.id),
            )

    def delete(self, tx_id: int) -> None:
        with self._conn:
            self._conn.execute("DELETE FROM transactions WHERE id = ?", (tx_id,))

    def close(self) -> None:
        self._conn.close()
