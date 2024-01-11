import requests
from datetime import datetime, timedelta, time

from pydantic import BaseModel, Field

from services import utils
from services.settings import settings

UNITS = "metric"


url = "http://api.openweathermap.org/data/2.5/forecast"


class City(BaseModel):
    timezone: int
    name: str


class Temperature(BaseModel):
    temp: float


class Weather(BaseModel):
    description: str
    code: int = Field(..., alias="id")


class Forecast(BaseModel):
    dt_txt: datetime
    main: Temperature
    weather: list[Weather]


class WeatherResponse(BaseModel):
    city: City
    list: list[Forecast]


def _fetch_forecast() -> WeatherResponse:
    params = {
        "q": settings.consts.WEATHER_CITY,
        "appid": settings.config.OWM__API_KEY,
        "units": UNITS,
        "lang": settings.consts.LANGUAGE,
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    return WeatherResponse(**response.json())


def _get_forecasts_in_timeframe(
    response: WeatherResponse, tomorrow: bool
) -> list[Forecast]:
    target_date = utils.get_target_date(response.city.timezone, tomorrow)
    min_datetime = datetime.combine(target_date, time(hour=8))
    max_datetime = datetime.combine(target_date, time(hour=18))

    min_datetime_utc = min_datetime - timedelta(seconds=response.city.timezone)
    max_datetime_utc = max_datetime - timedelta(seconds=response.city.timezone)

    in_timeframe = []
    for forecast in response.list:
        if min_datetime_utc <= forecast.dt_txt <= max_datetime_utc:
            in_timeframe.append(forecast)
    return in_timeframe


def get_weather(tomorrow: bool) -> WeatherResponse:
    weather_response = _fetch_forecast()
    forecasts = _get_forecasts_in_timeframe(weather_response, tomorrow)
    weather_response.list = forecasts
    return weather_response
