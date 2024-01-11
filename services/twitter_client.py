import logging

import tweepy

from services.settings import settings


class TwitterClient:
    _client: tweepy.Client = None

    @classmethod
    def start(
        cls,
        bearer: str = None,
        access_token: str = None,
        access_token_secret: str = None,
        consumer_key: str = None,
        consumer_secret: str = None,
    ):
        bearer = bearer or settings.config.TWITTER__BEARER
        access_token = access_token or settings.config.TWITTER__ACCESS_KEY
        access_token_secret = (
            access_token_secret or settings.config.TWITTER__ACCESS_SECRET
        )
        consumer_key = consumer_key or settings.config.TWITTER__CONSUMER_KEY
        consumer_secret = consumer_secret or settings.config.TWITTER__CONSUMER_SECRET
        if cls._client is None:
            cls._client = tweepy.Client(
                bearer_token=bearer,
                access_token=access_token,
                access_token_secret=access_token_secret,
                consumer_key=consumer_key,
                consumer_secret=consumer_secret,
            )

    @property
    def client(self):
        if self._client is None:
            raise Exception("Client not started yet")
        return self._client


twitter_client = TwitterClient()


def post_tweet(content: str) -> str:
    logging.info("Posting a new tweet")
    post_id = twitter_client.client.create_tweet(text=content).data["id"]
    logging.info("Tweet successfully posted")
    return post_id
