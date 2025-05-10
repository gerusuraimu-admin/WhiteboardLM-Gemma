from logging import Logger, getLogger, Formatter, INFO, StreamHandler

log_format = '[%(asctime)s][%(name)s][%(levelname)s] %(message)s'
date_format = '%Y/%m/%d-%H:%M:%S'


def get_logger(name: str) -> Logger:
    logger = getLogger(name)
    formatter = Formatter(log_format, date_format)
    handler = StreamHandler()
    handler.setFormatter(formatter)
    logger.setLevel(INFO)

    if not logger.handlers:
        logger.addHandler(handler)
    logger.propagate = False

    return logger
