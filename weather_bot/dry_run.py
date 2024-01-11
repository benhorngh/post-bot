from unittest.mock import patch

from controllers import secrets
from services import twitter_client, firebase_client
from weather_bot import lambda_function


@patch.object(secrets, "update_secrets_for_weather_bot")
@patch.object(twitter_client, "post_tweet", return_value="123")
def dry_run_weather_bot(post_tweet_mock, update_secrets_for_weather_bot):
    lambda_function.handler(None, None)
    print(post_tweet_mock.call_args[0][0])


if __name__ == "__main__":
    dry_run_weather_bot()
