import dataclasses
import os

from dotenv import load_dotenv


@dataclasses.dataclass
class Config:
    TWITTER__ACCESS_KEY: str = None
    TWITTER__ACCESS_SECRET: str = None
    TWITTER__CONSUMER_KEY: str = None
    TWITTER__CONSUMER_SECRET: str = None
    TWITTER__BEARER: str = None

    GCP__CREDENTIALS_JSON: str = None

    AWS__REGION: str = None

    OWM__API_KEY: str = None

    def __init__(self):
        self.TWITTER__ACCESS_KEY: str = os.getenv("TWITTER__ACCESS_KEY")
        self.TWITTER__ACCESS_SECRET: str = os.getenv("TWITTER__ACCESS_SECRET")
        self.TWITTER__CONSUMER_KEY: str = os.getenv("TWITTER__CONSUMER_KEY")
        self.TWITTER__CONSUMER_SECRET: str = os.getenv("TWITTER__CONSUMER_SECRET")
        self.TWITTER__BEARER: str = os.getenv("TWITTER__BEARER")

        self.GCP__CREDENTIALS_JSON: str = os.getenv("GCP__CREDENTIALS_JSON")

        self.AWS__REGION: str = os.getenv("AWS__REGION")

        self.OWM__API_KEY: str = os.getenv("OWM__API_KEY")


class Settings:
    _config = None

    @classmethod
    def init(cls):
        load_dotenv()
        cls._config = Config()

    @property
    def config(self) -> Config:
        if self._config is not None:
            return self._config
        raise Exception("Config not initialized")


settings = Settings()
