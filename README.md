# Personal Finance Manager

A command-line personal finance application built with Python for managing transactions, generating reports, and exporting financial data.

## Features

- **Add Transactions**: Track income and expenses with categories, dates, and descriptions
- **View Transactions**: Display all transactions with filtering options (by type, category, date range)
- **Edit Transactions**: Modify existing transaction details
- **Delete Transactions**: Remove transactions from your records
- **Summary & Reports**: Generate financial summaries with bar charts by category
- **Export to CSV**: Export transactions to CSV format for data analysis
- **Export to PDF**: Generate professional PDF reports with transaction details and statistics
- **Multi-category Support**: Pre-defined categories for income and expenses

## Categories

### Income
- Salary
- Freelance
- Investment
- Gift
- Other

### Expenses
- Food
- Housing
- Transport
- Health
- Entertainment
- Utilities
- Shopping
- Other

## Installation

### Requirements
- Python 3.13+
- pip or uv package manager

### Setup

```bash
# Clone the repository
git clone https://github.com/mk-repo-bigdata/finance-app.git
cd finance-app

# Install dependencies
pip install -r requirements.txt
# or
uv install
```

## Usage

```bash
# Run the application
python finance.py
```

### Main Menu Options

1. **Add Transaction** - Create a new income or expense transaction
2. **View Transactions** - Display transactions with various filters
3. **Edit Transaction** - Modify existing transaction details
4. **Delete Transaction** - Remove a transaction
5. **Summary / Reports** - View financial summaries and expense breakdowns
6. **Export to CSV** - Export transactions to CSV file
7. **Export to PDF** - Generate professional PDF reports
0. **Quit** - Exit the application

## Data Storage

- Transactions are stored in SQLite database: `data/finance.db`
- CSV exports saved to: `~/Downloads/transactions_YYYY-MM-DD.csv`
- PDF reports saved to: `~/Downloads/report_YYYY-MM-DD.pdf`

## Project Structure

```
finance-app/
├── finance.py                 # Main entry point
├── finance_app/
│   ├── __init__.py
│   ├── db.py                 # Database operations
│   ├── models.py             # Data models
│   ├── menus.py              # CLI menu logic
│   ├── display.py            # Terminal display helpers
│   ├── reports.py            # Report generation
│   ├── csv_export.py         # CSV export functionality
│   ├── pdf_export.py         # PDF export functionality
│   └── logger.py             # Logging configuration
├── data/
│   └── finance.db            # SQLite database (auto-created)
├── logs/
│   └── finance_app.log       # Application logs
└── README.md                 # This file

```

## Development

### Dependencies

- `reportlab` - PDF generation

### Running Tests

Tests can be added to verify core functionality:
- Database operations (CRUD)
- Report generation
- Export functionality

## Future Enhancements

- Budget tracking and alerts
- Recurring transactions
- Multi-currency support
- Data visualization with charts
- Web interface
- Mobile app

## License

MIT License

## Contributing

Feel free to submit issues and pull requests to improve the application.

## Support

For issues or questions, please open an issue on GitHub.

---

**Version**: 0.1.0  
**Last Updated**: April 2026
