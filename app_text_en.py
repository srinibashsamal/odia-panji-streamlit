"""English text for the Odia Panji Streamlit app.

Must define the same names and TEXT keys as ``app_text_od.py``.
"""

from __future__ import annotations

# Digits stay as they are (1434); app_text_od.py sets this to True.
USE_ODIA_DIGITS: bool = False

# Library terms (months, tithis, baras, Gajapatis...) are already English.
NAMES: dict[str, str] = {}

MONTHS: list[str] = "Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec".split()
MONTHS_LONG: list[str] = [
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December",
]

STYLE_LABELS: dict[str, str] = {
    "full": "Full",
    "compact": "Compact (one line)",
    "lunar": "Lunar first",
    "solar": "Solar first",
    "jataka": "Jataka",
}

GAJAPATI_UPADHI: str = (
    "Shree Shree Shree Veerashree Gajapati Gaudeshwara "
    "Nava Koti Karnatotkala Kalabargeshwara Abhiraya Bhuta Bhairaba "
    "Duhsaha Duhshasana Anikarane Rautaraya Shasanotteerna "
    "Atulabala Parakrama Sangrame Sahasrabahu Kshatriyakula Dhumaketu "
    "Airi Dalaganjana Matta Gaja Veeradhiveerabara "
    "Prabala Pratapi Maharajadhiraja"
)

# Page / navigation
PAGE_TEXT: dict[str, str] = {
    "page_title": "Odia Panji Converter",
    "title": "📅 Odia Panji Converter",
    "caption": (
        "Convert between English (Gregorian) dates and the Odia calendar: "
        "Utkalabda, Anka, tithi, solar month, Shakabda and bara."
    ),
    "tab_en": "English → Odia",
    "tab_od": "Odia → English",
    "tab_about": "About",
}

# English → Odia tab
EN_TO_ODIA_TEXT: dict[str, str] = {
    "en_date_heading": "**English (Gregorian) Date**",
    "day": "Day",
    "month": "Month",
    "year": "Year",
    "today": "Today",
    "pick_date": "Pick a date",
    "day_adjusted": "Day adjusted from {old} to {new} ({month} has {days} days).",
    "share_hint": "The page link updates with the date, so you can copy it to share.",
    "calculating": "Calculating...",
}

# Odia → English tab
ODIA_TO_EN_TEXT: dict[str, str] = {
    "year_given_as": "Year given as",
    "date_given_as": "Date given as",
    "Utkalabda": "Utkalabda",
    "Anka": "Anka",
    "Solar": "Solar",
    "Lunar": "Lunar",
    "utkalabda_year": "Utkalabda year",
    "anka": "Anka",
    "gajapati": "Gajapati",
    "invalid_anka": (
        "{anka} is not a valid Anka. Ankas skip 1, and any number "
        "ending in 6 or 0 (except 10)."
    ),
    "solar_month": "Solar month (rashi)",
    "lunar_month": "Lunar month",
    "paksha": "Paksha",
    "tithi": "Tithi",
    "adhika_label": "Adhika (intercalary) month",
    "adhika_help": "Set from today on first load; keeps your choice after that.",
    "searching": "Searching...",
    "result_date": "**{weekday}, {day} {month} {year}**",
}

# Panchanga / result details
DETAIL_TEXT: dict[str, str] = {
    "m_utkalabda": "Utkalabda",
    "m_anka": "Anka",
    "m_gajapati": "Gajapati",
    "m_shakabda": "Shakabda",
    "adhika_prefix": "Adhika ",
    "day_line": "**Day:** {bara} ({weekday})",
    "lunar_line": "**Lunar date:** {lunar}",
    "solar_line": "**Solar date:** {day} {month} (lunar equivalent: {equivalent})",
    "gajapati_line": "**Gajapati:** {gajapati} (acceded {accession})",
    "year_line": "**Odia year:** {start} to {end} (Sunia: {sunia})",
    "accession_day": "This is a Gajapati accession day; it is credited to the incoming monarch.",
    "citation_style": "Citation style",
    "no_anka": (
        "Anka years are available from {date} (earliest Gajapati in the library)."
    ),
    "all_details": "All details",
    "error": "Could not convert the date. ({error})",
}

# Citation formats
CITATION_TEXT: dict[str, str] = {
    # English uses the library's format_historical for most styles;
    # these keys are needed for the Jataka style and for Odia mode.
    "jataka": (
        "{titles} Shree Shree 108 Shree {gajapati} "
        "Maharajanka Vijaye Shubha Rajya Bardhane "
        "A{anka}nka Sna {utkalabda} sala "
        "Ingraji Ta- {date} rikha "
        "Sauramana {solar_month} Masa "
        "Di{solar_day}na "
        "Chandriyamana {lunar} {bara}"
    ),
    "cite_english": "{day} {month} {year}",
    "cite_utkalabda": "{year} Utkalabda",
    "cite_anka": "Anka {anka} of {gajapati}",
    "cite_shakabda": "Shakabda {year}",
    "cite_solar": "{day} {month}",
}

# Combined lookup for backward compatibility
TEXT: dict[str, str] = {
    **PAGE_TEXT,
    **EN_TO_ODIA_TEXT,
    **ODIA_TO_EN_TEXT,
    **DETAIL_TEXT,
    **CITATION_TEXT,
}

ABOUT: str = """
Built on [**odia-panji**](https://pypi.org/project/odia-panji/) v{version}
by Srinibash Samal ([GitHub](https://github.com/srinibashsamal/odia-panji)).

- Sunia, tithis and sankrantis are **computed** from the Sun and Moon, observed
  from **Puri** in **IST**.
- Lunar months are **Purnimanta**; a tithi belongs to the day whose sunrise
  falls inside it.
- Results are trusted for roughly **{min_year}-{max_year}**, so this app is
  limited to that range.
- Anka years are available from **{earliest}**.
- Printed panjis can differ by a day near a boundary.
"""

INSPIRATION_TITLE: str = "💡 Inspiration"
INSPIRATION: str = """
The inspiration behind this project came when I encountered a Jataka (ଜାତକ) that
recorded only the traditional Odia year and Anka. When I tried to convert these
dates into their corresponding Gregorian dates and years, I faced several
challenges.

That experience led me to think: *Why not build a simple tool that makes these
conversions easier and more accessible?*

That idea eventually led to the development of **odia-panji**, a Python library
for Odia calendar conversions, and this Streamlit web application built on top
of it.
"""

PURPOSE_TITLE: str = "🎯 Purpose"
PURPOSE: str = """
The goal is to make Odia calendar date conversions accessible and hassle-free
for everyone. I hope this tool will be useful to historians, researchers,
genealogists, and anyone interested in exploring Odisha's history, heritage, and
traditional calendar system.

By bridging traditional Odia dates with the Gregorian calendar, I hope to make
historical records easier to interpret and help people connect with Odisha's
rich cultural past.
"""
