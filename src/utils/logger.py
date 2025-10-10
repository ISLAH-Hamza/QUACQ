import logging
import os
from datetime import datetime


def setup_logger():
    now = datetime.now()
    date_str = now.strftime("%Y-%m-%d")
    time_str = now.strftime("%H-%M-%S")

    log_dir = os.path.join("logs", "code", date_str)
    os.makedirs(log_dir, exist_ok=True)
    
    log_file = os.path.join(log_dir, f"log_{time_str}.log")

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    # Clear existing handlers to avoid duplicate logs
    logger.handlers = []

    log_format = "%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(funcName)s - %(message)s"
    formatter = logging.Formatter(log_format)

    # FileHandler to log messages to a file
    fh = logging.FileHandler(log_file)
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(formatter)
    logger.addHandler(fh)

    return logger
