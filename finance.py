#!/usr/bin/env python3
"""Personal Finance CLI — entry point.

Usage:
    python finance.py
"""
from finance_app.db import DatabaseManager
from finance_app.logger import logger
from finance_app.menus import main_menu


def main() -> None:
    logger.info("=== Application started ===")
    db = DatabaseManager()
    try:
        main_menu(db)
    except KeyboardInterrupt:
        logger.info("Application interrupted by user (Ctrl+C)")
        print("\n\n  Goodbye.")
    except Exception as e:
        logger.error(f"Unexpected error: {e}", exc_info=True)
        raise
    finally:
        db.close()
        logger.info("=== Application ended ===")


if __name__ == "__main__":
    main()
