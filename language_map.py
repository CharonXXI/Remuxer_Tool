LANGUAGE_MAP = {
    "af": "AFRIKAANS",
    "sq": "ALBANIAN",
    "ar": "ARABIC",
    "hy": "ARMENIAN",
    "bn": "BENGALI",
    "bs": "BOSNIAN",
    "ca": "CATALAN",
    "hr": "CROATIAN",
    "cs": "CZECH",
    "da": "DANISH",
    "nl": "DUTCH",
    "en": "ENGLISH",
    "eo": "ESPERANTO",
    "et": "ESTONIAN",
    "tl": "FILIPINO (TAGALOG)",
    "fi": "FINNISH",
    "fr": "FRENCH",
    "fa": "FARSI",
    "de": "GERMAN",
    "el": "GREEK",
    "gu": "GUJARATI",
    "hi": "HINDI",
    "hu": "HUNGARIAN",
    "is": "ICELANDIC",
    "id": "INDONESIAN",
    "it": "ITALIAN",
    "ja": "JAPANESE",
    "jw": "JAVANESE",
    "ka": "GEORGIAN",
    "km": "KHMER",
    "kn": "KANNADA",
    "ko": "KOREAN",
    "la": "LATIN",
    "lv": "LATVIAN",
    "lt": "LITHUANIAN",
    "mk": "MACEDONIAN",
    "ml": "MALAYALAM",
    "mr": "MARATHI",
    "ne": "NEPALI",
    "pl": "POLISH",
    "pt": "PORTUGUESE",
    "pa": "PUNJABI",
    "ro": "ROMANIAN",
    "ru": "RUSSIAN",
    "sr": "SERBIAN",
    "si": "SINHALA",
    "sk": "SLOVAK",
    "sl": "SLOVENIAN",
    "es": "SPANISH",
    "su": "SUNDANESE",
    "sw": "SWAHILI",
    "sv": "SWEDISH",
    "ta": "TAMIL",
    "te": "TELUGU",
    "th": "THAI",
    "tr": "TURKISH",
    "uk": "UKRAINIAN",
    "ur": "URDU",
    "vi": "VIETNAMESE",
    "cy": "WELSH",
    "xh": "XHOSA",
    "yi": "YIDDISH",
    "zu": "ZULU",
}

def get_full_name(code: str) -> str:
    """Retourne le nom complet (ex: English) à partir de code ISO-639-1."""
    iso1 = get_iso1(code)
    return iso1_to_name.get(iso1, iso1.capitalize())

def get_iso1(code: str) -> str:
    """Convertit un code de langue en code ISO-639-1."""
    code = code.lower()
    # Si le code est déjà en ISO-639-1, le retourner tel quel
    if code in LANGUAGE_MAP:
        return code
    # Sinon, essayer de le convertir
    for iso1, name in LANGUAGE_MAP.items():
        if code in name.lower():
            return iso1
    return code
