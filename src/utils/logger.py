import logging
import os
from datetime import datetime


def setup_logger(to_console=True):
    """
    Set up a logger that writes logs to a file (and optionally to the console).

    Args:
        to_console (bool): If True, logs also appear in the terminal. Default is True.
    """
    # Create a log directory based on current date and time
    now = datetime.now()
    date_str = now.strftime("%Y-%m-%d")
    time_str = now.strftime("%H-%M-%S")
    log_dir = os.path.join("logs", "code", date_str)
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, f"log_{time_str}.log")

    # Setup logger
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    # Prevent duplicate handlers
    logger.handlers.clear()

    log_format = "%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(funcName)s - %(message)s"
    formatter = logging.Formatter(log_format)

    # File handler (always active)
    fh = logging.FileHandler(log_file)
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(formatter)
    logger.addHandler(fh)

    # Console handler (optional)
    if to_console:
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)
        ch.setFormatter(formatter)
        logger.addHandler(ch)

    return logger


def log(logger, message, level="info"):
    """
        Log a message with a specific logging level.
    """
    if logger is None:
        return
    level = level.lower()
    if hasattr(logger, level):
        getattr(logger, level)(message)
    else:
        logger.info(message)