"""Logging configuration for the personal finance app."""
import logging
import logging.handlers
from pathlib import Path

LOG_DIR = Path(__file__).parent.parent / "logs"


def configure_logging(log_level: str = "INFO") -> logging.Logger:
    """Configure logging with both file and console handlers."""
    LOG_DIR.mkdir(exist_ok=True)

    logger = logging.getLogger("finance_app")
    logger.setLevel(getattr(logging, log_level.upper()))

    # Avoid adding duplicate handlers
    if logger.handlers:
        return logger

    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # File handler - rotates when file size exceeds 5MB
    file_handler = logging.handlers.RotatingFileHandler(
        LOG_DIR / "finance_app.log",
        maxBytes=5 * 1024 * 1024,  # 5MB
        backupCount=3,
    )
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    # Console handler for errors only
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.ERROR)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    return logger


# Initialize logger at module import
logger = configure_logging()
