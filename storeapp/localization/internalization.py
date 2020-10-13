import json

default_locale = "en-gb"
cached_strings = {}


def refresh():
    global default_locale
    with open(f"locale-strings/{default_locale}.json") as f:
        cached_strings = json.load(f)


def gettext(name):
    return cached_strings[name]

def set_locale(locale):
    global default_locale
    default_locale = locale

refresh()