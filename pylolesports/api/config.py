from dataclasses import dataclass

ENDPOINT_PERSISTED_URL = 'https://esports-api.lolesports.com/persisted/gw'
ENDPOINT_LIVESTATS_URL = 'https://feed.lolesports.com/livestats/v1'

@dataclass
class Locales:
    czech: str = 'cs-CZ'
    english_australia: str = 'en-AU'
    english_britain: str = 'en-GB'
    english_us: str = 'en-US'
    french_france: str = 'fr-FR'
    german:str = 'de-DE'
    greek:str = 'el-GR'
    hungarian: str = 'hu-HU'
    italian: str = 'it-IT'
    japanese: str = 'ja-JP'
    korean: str = 'ko-KR'
    polish: str = 'pl-PL'
    portuguese_brazil: str = 'pt-BR'
    romanian: str = 'ro-RO'
    russian: str = 'ru-RU'
    spanish_mexico:str = 'es-MX'
    spanish_spain:str = 'es-ES'
    turkish: str = 'tr-TR'