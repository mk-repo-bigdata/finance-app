"""PDF export functionality for financial reports."""
from datetime import date
from pathlib import Path
from typing import List, Optional

from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib import colors

from .models import Transaction, TransactionType


def generate_transaction_report_pdf(
    transactions: List[Transaction],
    title: str = "Financial Report",
    filename: Optional[str] = None,
    include_summary: bool = True
) -> Path:
    """
    Generate a PDF report of transactions.

    Args:
        transactions: List of Transaction objects to include in report
        title: Report title
        filename: Optional custom filename. Defaults to report_YYYY-MM-DD.pdf
        include_summary: Whether to include summary statistics

    Returns:
        Path to the created PDF file

    Raises:
        ValueError: If no transactions provided
        IOError: If file cannot be written
    """
    if not transactions:
        raise ValueError("No transactions to export")

    # Generate default filename if not provided
    if filename is None:
        today = date.today().isoformat()
        filename = f"report_{today}.pdf"

    # Ensure filename ends with .pdf
    if not filename.endswith(".pdf"):
        filename += ".pdf"

    # Create export directory if it doesn't exist
    export_dir = Path.home() / "Downloads"
    filepath = export_dir / filename

    try:
        # Create PDF document
        doc = SimpleDocTemplate(str(filepath), pagesize=letter)
        story = []
        styles = getSampleStyleSheet()

        # Add title
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#1f4788'),
            spaceAfter=30,
            alignment=1  # Center alignment
        )
        story.append(Paragraph(title, title_style))

        # Add report date
        report_date = date.today().strftime("%B %d, %Y")
        date_style = ParagraphStyle(
            'DateStyle',
            parent=styles['Normal'],
            fontSize=10,
            textColor=colors.grey,
            spaceAfter=20,
            alignment=1
        )
        story.append(Paragraph(f"Generated on {report_date}", date_style))
        story.append(Spacer(1, 0.2 * inch))

        # Calculate summary if requested
        if include_summary:
            income = sum(t.amount for t in transactions if t.type == TransactionType.INCOME)
            expenses = sum(t.amount for t in transactions if t.type == TransactionType.EXPENSE)
            balance = income - expenses

            summary_data = [
                ['Total Income', f"${income:,.2f}", colors.HexColor('#27ae60')],
                ['Total Expenses', f"${expenses:,.2f}", colors.HexColor('#e74c3c')],
                ['Balance', f"${balance:,.2f}", colors.HexColor('#3498db')],
            ]

            summary_table = Table(summary_data, colWidths=[2*inch, 1.5*inch, 1*inch])
            summary_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (2, 2), colors.HexColor('#ecf0f1')),
                ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 11),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
                ('TOPPADDING', (0, 0), (-1, -1), 12),
                ('GRID', (0, 0), (-1, -1), 1, colors.grey),
            ]))
            story.append(summary_table)
            story.append(Spacer(1, 0.3 * inch))

        # Add transactions table
        transactions_heading = ParagraphStyle(
            'Heading',
            parent=styles['Heading2'],
            fontSize=14,
            textColor=colors.HexColor('#1f4788'),
            spaceAfter=12,
        )
        story.append(Paragraph("Transaction Details", transactions_heading))
        story.append(Spacer(1, 0.1 * inch))

        # Build transaction table data
        table_data = [['ID', 'Date', 'Type', 'Category', 'Amount', 'Description']]
        for tx in transactions:
            amount_str = f"${tx.amount:,.2f}"
            tx_type_color = colors.HexColor('#27ae60') if tx.type == TransactionType.INCOME else colors.HexColor('#e74c3c')
            table_data.append([
                str(tx.id),
                tx.date.isoformat(),
                tx.type.value.capitalize(),
                tx.category,
                amount_str,
                tx.description[:30] + "..." if len(tx.description) > 30 else tx.description,
            ])

        # Create and style table
        tx_table = Table(table_data, colWidths=[0.6*inch, 1*inch, 0.8*inch, 1.2*inch, 0.9*inch, 1.5*inch])
        tx_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#34495e')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('TOPPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f5f5f5')]),
            ('FONTSIZE', (0, 1), (-1, -1), 9),
            ('ALIGN', (4, 1), (4, -1), 'RIGHT'),  # Right align amounts
        ]))
        story.append(tx_table)

        # Build PDF
        doc.build(story)
        return filepath

    except IOError as e:
        raise IOError(f"Failed to write PDF file: {e}")


def prompt_pdf_filename() -> str:
    """Prompt user for optional custom PDF filename."""
    filename = input("  Enter filename (or press Enter for default): ").strip()
    return filename if filename else None


def prompt_include_summary() -> bool:
    """Prompt user whether to include summary statistics."""
    choice = input("  Include summary statistics? [Y/n]: ").strip().lower()
    return choice != 'n'
