"""
logger.py - Simple logging for Expense Tracker
Handles INFO and WARNING logs, ensures log file exists.
"""

import logging
import os

# Path to log file
LOG_FILE = os.path.join(os.path.dirname(__file__), "..", "logs", "app.log")


def setup_logger():
    """Set up the logger with INFO and WARNING handlers."""
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)

    logger = logging.getLogger("expense_tracker")
    logger.setLevel(logging.DEBUG)  # Capture all levels

    # Avoid duplicate handlers on repeated imports
    if not logger.handlers:
        # File handler
        fh = logging.FileHandler(LOG_FILE, encoding="utf-8")
        fh.setLevel(logging.DEBUG)
        formatter = logging.Formatter(
            "%(asctime)s - %(levelname)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
        )
        fh.setFormatter(formatter)
        logger.addHandler(fh)

    return logger


# Initialize global logger
logger = setup_logger()


# ──────────────────────────────────────────
# Helper logging functions
# ──────────────────────────────────────────


def ensure_log_file():
    """Ensure the log file exists."""
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
    if not os.path.exists(LOG_FILE):
        # Create empty file
        with open(LOG_FILE, "w", encoding="utf-8") as f:
            pass


def log_info(message):
    """Log an INFO message."""
    ensure_log_file()
    logger.info(message)


def log_warning(message):
    """Log a WARNING message."""
    ensure_log_file()
    logger.warning(message)


def reset_log_file_for_test():
    """Clear log file for testing purposes."""
    ensure_log_file()
    with open(LOG_FILE, "w", encoding="utf-8") as f:
        f.truncate(0)
