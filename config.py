import logging
from logging import Logger


def setup_logging(name: str, log_level: int = logging.INFO) -> Logger:
    formatter = logging.Formatter('%(asctime)s | %(levelname)-8s | %(name)s.%(funcName)s:%(lineno)d | %(message)s')

    handler = logging.StreamHandler()
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.addHandler(handler)
    logger.setLevel(log_level)

    return logger
