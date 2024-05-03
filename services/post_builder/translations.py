from enum import Enum

from services.settings import settings


class K(str, Enum):
    tomorrow = "tomorrow"
    today = "today"
    no_rain = "no_rain"
    clear_sky = "clear_sky"


translations = {
    K.tomorrow: {"he": "מחר", "en": "tomorrow"},
    K.today: {"he": "היום", "en": "today"},
    K.no_rain: {"he": "ללא גשם", "en": "no rain"},
    K.clear_sky: {"he": "בהיר", "en": "clear"},
}


def t(translation_key: K):
    return translations[translation_key][settings.consts.LANGUAGE]
