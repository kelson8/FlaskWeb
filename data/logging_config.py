import logging
from logging.handlers import TimedRotatingFileHandler

# Moved logging into here, this avoids circular imports in login_pages.py.

def setup_logging():
    # Create a handler that rotates logs at midnight
    handler = TimedRotatingFileHandler("flask.log", when='midnight', interval=1, backupCount=7)

    # Set the format for the log messages
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)

    # Get the logger
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    logger.addHandler(handler)
    return logger
