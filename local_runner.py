import logging

import lambda_function


def handle():
    _init_logger()


def _init_logger():
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    logger.addHandler(console_handler)
    lambda_function.handler(None, None)


if __name__ == "__main__":
    handle()
