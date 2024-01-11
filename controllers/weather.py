import logging

from services import open_weather
from services.post_builder import weather_post
from services import twitter_client


def start(tomorrow: bool = True):
    twitter_client.twitter_client.start()
    logging.info("Starting weather")
    weather = open_weather.get_weather(tomorrow)
    post = weather_post.build_post(weather, tomorrow)
    post_trimmed = post.replace("\n", "   ")
    logging.info(f"Post built successfully: '{post_trimmed}'")
    post_id = twitter_client.post_tweet(post)
    logging.info(f"Post created successfully: '{post_id}'")
