import logging
from logging.handlers import RotatingFileHandler
from sys import stdout


def console_logging(name: str):

    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    handler = logging.StreamHandler(stdout)
    handler.setLevel(logging.DEBUG)
    formatter = logging.\
        Formatter('%(asctime)s - %(levelname)s - %(filename)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.propagate = False

    return logger


def log_file_logger(name):

    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    stream_handler = logging.StreamHandler(stdout)

    handler = RotatingFileHandler(f'{name}_logfile.log', maxBytes=200000, backupCount=0)  # noqa: E501
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(filename)s - %(message)s')  # noqa: E501
    handler.setFormatter(formatter)
    stream_handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.addHandler(stream_handler)
    logger.propagate = False

    return logger
