import logging
import os
from logging.handlers import RotatingFileHandler
from time import sleep

from parse_google_sheet import update_supplies
from settiings import PATH_TO_LOGS


def create_logger() -> logging.Logger:
    """Create logger."""
    if not os.path.exists(PATH_TO_LOGS):
        os.makedirs(PATH_TO_LOGS)
    logging_level = os.getenv('LOGGING_LEVEL', 'INFO')
    logger = logging.getLogger()
    file_handler = RotatingFileHandler(f'{PATH_TO_LOGS}/main.log', maxBytes=10 * 1024 * 1024, backupCount=10)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    console_handler.setLevel(logging_level)
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    logger.setLevel(logging_level)
    return logger


if __name__ == '__main__':
    logger = create_logger()
    while True:
        try:
            update_supplies()
        except Exception as e:
            logger.error(e, exc_info=True)
        sleep(1)
