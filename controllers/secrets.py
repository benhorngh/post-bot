import os

from services import aws_secrets
from services.aws_secrets import secret_manager_client, SecretId
from services.settings import settings


def update_secrets_for_weather_bot():
    secrets_ids = [SecretId.weather]
    _update_secrets(secrets_ids)


def update_secrets_for_patent_bot():
    secrets_ids = [SecretId.patent, SecretId.gcp_credentials]
    _update_secrets(secrets_ids)


def _update_secrets(secrets_ids: list[SecretId]):
    secret_manager_client.start(region_name=settings.config.AWS__REGION)
    for secret_id in secrets_ids:
        secrets = aws_secrets.get_secret(secret_id)
        for key, value in secrets.items():
            os.environ[key] = value
    settings.init()  # refresh configs
