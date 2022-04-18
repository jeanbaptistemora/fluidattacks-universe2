import logging
import sys


def get_log(name: str, min_lvl: int = logging.INFO) -> logging.Logger:
    logger_format: str = "[%(levelname)s] %(message)s"
    logger_formatter: logging.Formatter = logging.Formatter(logger_format)

    logger_handler: logging.Handler = logging.StreamHandler(sys.stderr)
    logger_handler.setFormatter(logger_formatter)

    logger: logging.Logger = logging.getLogger(name)
    logger.setLevel(min_lvl)
    logger.addHandler(logger_handler)
    return logger
