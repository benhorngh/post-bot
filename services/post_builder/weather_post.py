import statistics
from datetime import timedelta

from services import utils
from services.open_weather import WeatherResponse, Forecast, Weather
from services.post_builder.translations import K, t

output_date_format = "%d/%m"


def build_post(response: WeatherResponse, tomorrow: bool) -> str:
    text = ""
    text += _header(response, tomorrow)
    text += "\n"
    text += _emojis(response.list)
    text += "\n"
    text += _body(response)
    return text


def _header(response: WeatherResponse, tomorrow: bool) -> str:
    target_date = utils.get_target_date(response.city.timezone, tomorrow)
    day_description = t(K.tomorrow) if tomorrow else t(K.today)
    text = f"{response.city.name} {day_description} {target_date.strftime(output_date_format)}"
    return text


def _emojis(forecasts: list[Forecast]) -> str:
    text = ""
    text += _get_rain_emoji(forecasts)
    return text


def _body(response: WeatherResponse) -> str:
    if _should_use_hourly_template(response.list):
        return _hourly_body(response)
    else:
        return _daily_body(response)


def _daily_body(response: WeatherResponse) -> str:
    forecasts = response.list
    temps = statistics.mean([f.main.temp for f in forecasts])
    text = _degrees_text(temps)
    weather = _get_weathers(forecasts)
    if not _is_rain_code(weather[0].code):
        text += f", {weather[0].description}"
    return text


def _hourly_body(response: WeatherResponse) -> str:
    text = ""
    text += "\n".join(
        [_hourly_forecast_text(f, response.city.timezone) for f in response.list]
    )
    return text


def _hourly_forecast_text(forecast: Forecast, timezone_in_seconds: int) -> str:
    local_time = forecast.dt_txt + timedelta(seconds=timezone_in_seconds)
    start_time = local_time.hour
    end_time = local_time.hour + 3
    emoji = icon_name_to_emoji(forecast.weather[0].icon)
    return f"{start_time}-{end_time}: {_degrees_text(forecast.main.temp)} {forecast.weather[0].description} {emoji}"


def _get_descriptions(forecasts: list[Forecast]) -> list[str]:
    weathers = _get_weathers(forecasts)
    return [w.description for w in weathers]


def _should_use_hourly_template(forecasts: list[Forecast]):
    temps = [f.main.temp for f in forecasts]
    min_temp, max_temp = min(temps), max(temps)
    if max_temp - min_temp > 3:
        return True
    descriptions = _get_descriptions(forecasts)
    if len(set(descriptions)) > 1:
        return True
    return False


def _get_weathers(forecasts: list[Forecast]) -> list[Weather]:
    return [w for f in forecasts for w in f.weather if w is not None and w.description]


def _get_rain_emoji(forecasts: list[Forecast]) -> str:
    weathers = _get_weathers(forecasts)
    rain = [w for w in weathers if _is_rain_code(w.code)]
    description, code = t(K.no_rain), 0
    if rain:
        rain.sort(key=lambda w: w.code, reverse=True)
        description, code = rain[0].description, rain[0].code
    elif "01d" in [w.icon for w in weathers]:
        description, code = t(K.clear_sky), 800
    emoji = _rain_emoji_by_code(code)
    return f"{description} {emoji}"


def _rain_emoji_by_code(rain_code: int) -> str:
    # https://openweathermap.org/weather-conditions
    if rain_code == 0:
        return "❌"
    elif rain_code == 500:
        return "💧"
    elif rain_code == 501:
        return "🌧️"
    elif 502 <= rain_code <= 531:
        return "⛈️"
    elif rain_code == 800:
        return "☀️"
    elif rain_code == 801:
        return "🌤️"
    elif 802 <= rain_code <= 804:
        return "☁️"


def icon_name_to_emoji(icon_name: str):
    # https://openweathermap.org/weather-conditions#Icon-list
    if icon_name == "01d":
        return "☀️"
    elif icon_name == "01n":
        return "🌝"
    elif icon_name == "02d":
        return "🌤️"
    elif icon_name == "02n":
        return "☁️"
    elif icon_name == "03d":
        return "☁️"
    else:
        return ""


def _is_rain_code(code: int) -> bool:
    return 500 <= code <= 599


def _degrees_text(degrees: float) -> str:
    return f"{round(degrees)}°"
