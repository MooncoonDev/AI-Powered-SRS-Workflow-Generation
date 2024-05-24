import logging
from logging import Logger
from pathlib import Path


DATA_DIR = Path("data")
RAW_DATA_DIR = DATA_DIR / "raw"
RAW_SRS_DIR = RAW_DATA_DIR / "pdf"
GROUND_TRUTH_DATA_DIR = RAW_DATA_DIR / "reference-dot"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
PROCESSED_DOT_DATA_DIR = PROCESSED_DATA_DIR / "dot"
PROCESSED_TXT_DATA_DIR = PROCESSED_DATA_DIR / "txt"

HF_MODEL = ""


def setup_logging(name: str, log_level: int = logging.INFO) -> Logger:
    formatter = logging.Formatter('%(asctime)s | %(levelname)-8s | %(name)s.%(funcName)s:%(lineno)d | %(message)s')

    handler = logging.StreamHandler()
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.addHandler(handler)
    logger.setLevel(log_level)

    return logger
