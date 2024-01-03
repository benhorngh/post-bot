import os

from services import aws_secrets
from services.aws_secrets import secret_manager_client
from services.settings import settings


def update_secrets():
    secret_manager_client.start(region_name=settings.config.AWS__REGION)
    secrets = aws_secrets.get_secrets()
    for key, value in secrets.items():
        os.environ[key] = value
    settings.init()  # refresh configs
