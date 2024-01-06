import logging

from weather_bot import lambda_function


def weather():
    lambda_function.handler(None, None)


def _init_logger():
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    logger.addHandler(console_handler)


if __name__ == "__main__":
    _init_logger()
    weather()
