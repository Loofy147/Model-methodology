# Jules for Hugging Face - Structured Logging

import logging
import json
from .config import config

class JsonFormatter(logging.Formatter):
    """
    Formats log records as JSON strings.
    """
    def format(self, record):
        log_record = {
            "timestamp": self.formatTime(record, self.datefmt),
            "level": record.levelname,
            "name": record.name,
            "message": record.getMessage()
        }
        if record.exc_info:
            log_record['exc_info'] = self.formatException(record.exc_info)

        # Add extra context if available
        if hasattr(record, 'extra_context'):
            log_record['extra_context'] = record.extra_context

        return json.dumps(log_record)

def setup_logging():
    """
    Configures the root logger for the application.
    """
    log_level = config.get('logging', {}).get('level', 'INFO').upper()
    log_format = config.get('logging', {}).get('format', 'text')
    log_file = config.get('logging', {}).get('file', None)

    logger = logging.getLogger("jules_hf")
    logger.setLevel(log_level)

    # Prevent duplicate handlers if called multiple times
    if logger.hasHandlers():
        logger.handlers.clear()

    handler = logging.StreamHandler() # Default to console
    if log_file:
        handler = logging.FileHandler(log_file)

    if log_format == 'json':
        formatter = JsonFormatter()
    else:
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    handler.setFormatter(formatter)
    logger.addHandler(handler)

def get_logger(name: str) -> logging.Logger:
    """
    Returns a logger instance for a given module.
    """
    return logging.getLogger(f"jules_hf.{name}")
