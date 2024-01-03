import logging


def handler(event, context):
    try:
        from services.settings import settings

        settings.init()

        _init_logger()
        logging.info("Got event")

        from controllers.secrets import update_secrets

        update_secrets()

        from controllers.patents import start

        start()

    except Exception:
        logging.exception("Lambda function failed")
        raise


def _init_logger():
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
