"""
utils/logger.py
────────────────
Centralised logging configuration for the automation framework.

Usage
-----
    from utils.logger import get_logger
    logger = get_logger(__name__)
    logger.info("This message goes to console AND logs/automation.log")
"""

import logging
import os
from logging.handlers import RotatingFileHandler

# Directory for log files
LOGS_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "logs"
)


def get_logger(name: str = "automation") -> logging.Logger:
    """
    Return a logger that writes to both the console and a rotating log file.

    Parameters
    ----------
    name : logger name (typically __name__ of the calling module)

    Returns
    -------
    Configured logging.Logger instance.
    """
    os.makedirs(LOGS_DIR, exist_ok=True)

    logger = logging.getLogger(name)

    # Avoid adding duplicate handlers when the same logger is requested twice
    if logger.handlers:
        return logger

    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter(
        fmt="%(asctime)s  [%(levelname)-8s]  %(name)s : %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # ── Console handler ────────────────────────────────────────────────────────
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)

    # ── Rotating file handler (max 5 MB × 3 backups) ──────────────────────────
    log_file = os.path.join(LOGS_DIR, "automation.log")
    file_handler = RotatingFileHandler(
        log_file, maxBytes=5 * 1024 * 1024, backupCount=3, encoding="utf-8"
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger
