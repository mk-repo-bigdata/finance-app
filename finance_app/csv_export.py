"""CSV export functionality for transactions."""
import csv
from datetime import date
from pathlib import Path
from typing import List, Optional

from .models import Transaction


def export_to_csv(
    transactions: List[Transaction],
    filename: Optional[str] = None
) -> Path:
    """
    Export transactions to CSV file.

    Args:
        transactions: List of Transaction objects to export
        filename: Optional custom filename. Defaults to transactions_YYYY-MM-DD.csv

    Returns:
        Path to the created CSV file

    Raises:
        ValueError: If no transactions provided
        IOError: If file cannot be written
    """
    if not transactions:
        raise ValueError("No transactions to export")

    # Generate default filename if not provided
    if filename is None:
        today = date.today().isoformat()
        filename = f"transactions_{today}.csv"

    # Ensure filename ends with .csv
    if not filename.endswith(".csv"):
        filename += ".csv"

    # Create export directory if it doesn't exist
    export_dir = Path.home() / "Downloads"
    filepath = export_dir / filename

    try:
        with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['ID', 'Date', 'Type', 'Category', 'Amount', 'Description']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            for tx in transactions:
                writer.writerow({
                    'ID': tx.id,
                    'Date': tx.date.isoformat(),
                    'Type': tx.type.value,
                    'Category': tx.category,
                    'Amount': f"{tx.amount:.2f}",
                    'Description': tx.description,
                })

        return filepath
    except IOError as e:
        raise IOError(f"Failed to write CSV file: {e}")


def prompt_export_filename() -> str:
    """Prompt user for optional custom filename."""
    filename = input("  Enter filename (or press Enter for default): ").strip()
    return filename if filename else None
