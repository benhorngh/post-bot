import json
from enum import Enum

import boto3
from botocore.exceptions import ClientError

from services.settings import settings


class SecretId(str, Enum):
    patent = "patent"
    gcp_credentials = "patent-gcp-credentials"


class AWSSecretManagerClient:
    _client = None

    @classmethod
    def start(cls, region_name: str = settings.config.AWS__REGION):
        session = boto3.session.Session()
        client = session.client(service_name="secretsmanager", region_name=region_name)
        cls._client = client

    @property
    def client(self):
        if self._client is None:
            raise Exception("Client not started yet")
        return self._client


secret_manager_client = AWSSecretManagerClient()


def _get_secret(secret_id: str) -> dict:
    try:
        get_secret_value_response = secret_manager_client.client.get_secret_value(
            SecretId=secret_id
        )
        secrets = json.loads(get_secret_value_response.get("SecretString"))
    except ClientError as e:
        raise e
    if not secrets:
        raise Exception(
            f"Failed to fetch secrets from AWS secrets manager: {get_secret_value_response}"
        )
    return secrets


def get_secrets() -> dict:
    all_secrets = {}
    for secret_id in SecretId:
        secrets = _get_secret(secret_id)
        all_secrets.update(secrets)
    return all_secrets
