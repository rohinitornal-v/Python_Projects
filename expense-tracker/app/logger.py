"""
logger.py - Application Logging Setup
Handles all logging for the Expense Tracker application.
Writes INFO and WARNING messages to logs/app.log
"""

import logging
import os

# path to log file
LOG_FILE = "logs/app.log"


def setup_logger():
    """Set up the logger for the application.
    - Creates the logs directory if it doesn't exist
    - Writes logs to app.log with INFO level and a specific format
    - Logs include INFO timestamp, log level, and WARNING message"""

    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
    logging.basicConfig(
        filename=LOG_FILE,
        level=logging.DEBUG,
        format="%(asctime)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    return logging.getLogger(__name__)


# Initialize the logger
logger = setup_logger()

# ----------------------------
# Logging Functions
# ----------------------------


def log_info(message):
    """Log an INFO message."""
    logger.info(message)


def log_warning(message):
    """Log a WARNING message."""
    logger.warning(message)
