import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def handler(event, context):
    try:
        logging.info("Got event")

        from services.settings import settings

        settings.init()

        from controllers.secrets import update_secrets_for_weather_bot

        update_secrets_for_weather_bot()

        from controllers.weather import start

        start()

    except Exception:
        logging.exception("Lambda function failed")
        raise
