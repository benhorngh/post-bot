from enum import Enum

from services.settings import settings


class K(str, Enum):
    tomorrow = ("tomorrow",)
    today = ("today",)
    no_rain = "no_rain"


translations = {
    K.tomorrow: {"he": "מחר", "en": "tomorrow"},
    K.today: {"he": "היום", "en": "today"},
    K.no_rain: {"he": "ללא גשם", "en": "no rain"},
}


def t(translation_key: K):
    return translations[translation_key][settings.consts.LANGUAGE]
