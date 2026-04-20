#!/usr/bin/env python3
"""Personal Finance CLI — entry point.

Usage:
    python finance.py
"""
from finance_app.db import DatabaseManager
from finance_app.menus import main_menu


def main() -> None:
    db = DatabaseManager()
    try:
        main_menu(db)
    except KeyboardInterrupt:
        print("\n\n  Goodbye.")
    finally:
        db.close()


if __name__ == "__main__":
    main()
