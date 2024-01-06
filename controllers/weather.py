import logging

from services import open_weather
from services.post_builder import weather_post


def start(tomorrow: bool = False):
    logging.info("Starting weather")
    weather = open_weather.get_weather(tomorrow)
    post = weather_post.build_post(weather, tomorrow)
    logging.info(f"Post built successfully: '{post}'")
