import logging

from patent_bot import lambda_function


def patent():
    lambda_function.handler(None, None)


def _init_logger():
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    logger.addHandler(console_handler)


if __name__ == "__main__":
    _init_logger()
    patent()
