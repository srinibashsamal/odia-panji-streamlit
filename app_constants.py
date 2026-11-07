"""Constants for the Odia Panji Streamlit app (dates, styles, CSS).

All on-screen text lives in ``app_text_en.py`` and ``app_text_od.py``.
"""

from __future__ import annotations

from datetime import date, timedelta, timezone

from odia_panji import GAJAPATI_REIGNS, HistoricalStyle, utkalabda_year
from odia_panji.constants import LUNAR_MONTHS, RASHI, TITHI_NAMES

# ---- Time & date range ----------------------------------------------------

IST = timezone(timedelta(hours=5, minutes=30), name="IST")

# Dates the library is trusted for (see the README's "Limitations").
MIN_DATE: date = date(1800, 1, 1)
MAX_DATE: date = date(2100, 12, 31)
EARLIEST_ANKA_DATE: date = GAJAPATI_REIGNS[0].accession

# Utkalabda changes mid-year, so "year - 592" is off by one for part of every year.
MIN_UTKALABDA: int = utkalabda_year(MIN_DATE)
MAX_UTKALABDA: int = utkalabda_year(MAX_DATE)

# ---- Option lists ---------------------------------------------------------

REIGN_NAMES: list[str] = [
    reign.name for reign in reversed(GAJAPATI_REIGNS)
]  # current first
YEARS: list[int] = list(range(MIN_DATE.year, MAX_DATE.year + 1))
PAKSHAS: list[str] = ["Shukla", "Krushna"]

# Radio / select values used as both widget values and TEXT keys.
YEAR_UTKALABDA: str = "Utkalabda"
YEAR_ANKA: str = "Anka"
YEAR_TYPES: list[str] = [YEAR_UTKALABDA, YEAR_ANKA]

DATE_SOLAR: str = "Solar"
DATE_LUNAR: str = "Lunar"
DATE_TYPES: list[str] = [DATE_SOLAR, DATE_LUNAR]

# Citation styles: library styles first, then the app's own Jataka style.
# Display labels come from STYLE_LABELS in the text modules.
STYLES: list[HistoricalStyle] = ["full", "compact", "lunar", "solar"]
JATAKA_STYLE: str = "jataka"

# Same label in both languages, so the switch is readable either way.
LANGUAGE_TOGGLE_LABEL: str = "ଓଡ଼ିଆ (Odia)"

# ---- Layout ---------------------------------------------------------------

# Width of the square icon columns (refresh button and calendar picker).
ICON_COL_WIDTH: str = "2.6rem"

# Column width ratios for the main form rows and metrics.
EN_DATE_COLS: list[float] = [1.1, 1.4, 1.5, 0.55, 0.55]
OD_HEAD_COLS: list[float] = [2, 2, 0.55]
METRICS_COLS: list[float] = [1, 0.7, 2.6, 1]


# ---- Widget, container and session-state keys -----------------------------


class SessionKey:
    """Central place for Streamlit widget, container and session-state keys.

    LAYOUT_CSS below targets several of these through Streamlit's
    ``st-key-<key>`` classes, so renaming a key here also updates the CSS.
    """

    # Language
    ODIA_MODE = "odia_mode"

    # English → Odia
    EN_DATE_ROW = "en_date_row"  # container
    EN_DAY = "en_day"
    EN_MONTH = "en_month"
    EN_YEAR = "en_year"
    EN_PICKER = "en_picker"
    BTN_TODAY = "btn_today"
    CLAMPED_FROM = "_clamped_from"

    # Odia → English
    OD_HEAD_ROW = "od_head_row"  # container
    OD_YEAR_TYPE = "od_year_type"
    OD_DATE_TYPE = "od_date_type"
    OD_UTKALABDA = "od_utkalabda"
    OD_ANKA = "od_anka"
    OD_GAJAPATI = "od_gajapati"
    OD_RASHI = "od_rashi"
    OD_SOLAR_DAY = "od_solar_day"
    OD_LUNAR_MONTH = "od_lunar_month"
    LUNAR_PAKSHA = "lunar_paksha"
    LUNAR_TITHI = "lunar_tithi"
    OD_ADHIKA = "od_adhika"
    BTN_OD_TODAY = "btn_od_today"

    # Details panel (suffixed with "en" / "od" per tab)
    METRICS_PREFIX = "metrics_"  # container
    STYLE_PREFIX = "style_"


# ---- Translated selectboxes -----------------------------------------------

# Streamlit stores a selectbox value as its *label*, so after a language
# switch the old label no longer matches. restore_selectbox_values() maps
# labels back to the underlying values before the widgets are drawn.

# Text-valued selectboxes and their real options (library terms).
TRANSLATED_TERMS: dict[str, list[str]] = {
    SessionKey.OD_GAJAPATI: REIGN_NAMES,
    SessionKey.OD_RASHI: RASHI,
    SessionKey.OD_LUNAR_MONTH: LUNAR_MONTHS,
    SessionKey.LUNAR_PAKSHA: PAKSHAS,
    SessionKey.LUNAR_TITHI: [*TITHI_NAMES, "Purnima", "Amabasya"],
}

# Number-valued selectboxes (Day / Month / Year) plus the ones above,
# so a new text dropdown only needs adding to TRANSLATED_TERMS.
TRANSLATED_SELECTBOXES: tuple[str, ...] = (
    SessionKey.EN_DAY,
    SessionKey.EN_MONTH,
    SessionKey.EN_YEAR,
    *TRANSLATED_TERMS,
)

# ---- Calendar icon (base64 SVG for CSS mask) ------------------------------

# Base64-encoded Material "calendar_month" SVG: more reliable in CSS masks
# than a plain utf-8 data URI (older Firefox was picky about it).
_CALENDAR_SVG_B64: str = (
    "PHN2ZyB4bWxucz0naHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmcnIHZpZXdCb3g9"
    "JzAgLTk2MCA5NjAgOTYwJz48cGF0aCBkPSdNMjAwLTgwcS0zMyAwLTU2LjUtMjMuNVQx"
    "MjAtMTYwdi01NjBxMC0zMyAyMy41LTU2LjVUMjAwLTgwMGg0MHYtODBoODB2ODBoMzIw"
    "di04MGg4MHY4MGg0MHEzMyAwIDU2LjUgMjMuNVQ4NDAtNzIwdjU2MHEwIDMzLTIzLjUg"
    "NTYuNVQ3NjAtODBIMjAwWm0wLTgwaDU2MHYtNDAwSDIwMHY0MDBabTAtNDgwaDU2MHYt"
    "ODBIMjAwdjgwWm0wIDB2LTgwIDgwWm0yODAgMjQwcS0xNyAwLTI4LjUtMTEuNVQ0NDAt"
    "NDQwcTAtMTcgMTEuNS0yOC41VDQ4MC00ODBxMTcgMCAyOC41IDExLjVUNTIwLTQ0MHEw"
    "IDE3LTExLjUgMjguNVQ0ODAtNDAwWm0tMTYwIDBxLTE3IDAtMjguNS0xMS41VDI4MC00"
    "NDBxMC0xNyAxMS41LTI4LjVUMzIwLTQ4MHExNyAwIDI4LjUgMTEuNVQzNjAtNDQwcTAg"
    "MTctMTEuNSAyOC41VDMyMC00MDBabTMyMCAwcS0xNyAwLTI4LjUtMTEuNVQ2MDAtNDQw"
    "cTAtMTcgMTEuNS0yOC41VDY0MC00ODBxMTcgMCAyOC41IDExLjVUNjgwLTQ0MHEwIDE3"
    "LTExLjUgMjguNVQ2NDAtNDAwWk00ODAtMjQwcS0xNyAwLTI4LjUtMTEuNVQ0NDAtMjgw"
    "cTAtMTcgMTEuNS0yOC41VDQ4MC0zMjBxMTcgMCAyOC41IDExLjVUNTIwLTI4MHEwIDE3"
    "LTExLjUgMjguNVQ0ODAtMjQwWm0tMTYwIDBxLTE3IDAtMjguNS0xMS41VDI4MC0yODBx"
    "MC0xNyAxMS41LTI4LjVUMzIwLTMyMHExNyAwIDI4LjUgMTEuNVQzNjAtMjgwcTAgMTct"
    "MTEuNSAyOC41VDMyMC0yNDBabTMyMCAwcS0xNyAwLTI4LjUtMTEuNVQ2MDAtMjgwcTAt"
    "MTcgMTEuNS0yOC41VDY0MC0zMjBxMTcgMCAyOC41IDExLjVUNjgwLTI4MHEwIDE3LTEx"
    "LjUgMjguNVQ2NDAtMjQwWicvPjwvc3ZnPg=="
)
_CALENDAR_SVG: str = 'url("data:image/svg+xml;base64,' + _CALENDAR_SVG_B64 + '")'

# Placeholders (__NAME__) are filled from SessionKey and the values above,
# so the CSS selectors always match the keys used in app.py.
_CSS_TEMPLATE = """
<style>
.st-key-__EN_DATE_ROW__ [data-testid="stHorizontalBlock"],
.st-key-__OD_HEAD_ROW__ [data-testid="stHorizontalBlock"],
[class*="st-key-__METRICS__"] [data-testid="stHorizontalBlock"] {
    flex-wrap: nowrap !important;
    gap: 0.5rem !important;
}
.st-key-__EN_DATE_ROW__ [data-testid="stColumn"],
.st-key-__EN_DATE_ROW__ [data-testid="column"],
.st-key-__OD_HEAD_ROW__ [data-testid="stColumn"],
.st-key-__OD_HEAD_ROW__ [data-testid="column"],
[class*="st-key-__METRICS__"] [data-testid="stColumn"],
[class*="st-key-__METRICS__"] [data-testid="column"] {
    min-width: 0 !important;
}

/* Icon columns: fixed square width on every screen size, so the icons
   never get squeezed on phones. The other columns share the rest. */
.st-key-__EN_DATE_ROW__ [data-testid="stColumn"]:nth-child(n+4),
.st-key-__EN_DATE_ROW__ [data-testid="column"]:nth-child(n+4),
.st-key-__OD_HEAD_ROW__ [data-testid="stColumn"]:last-child,
.st-key-__OD_HEAD_ROW__ [data-testid="column"]:last-child {
    flex: 0 0 __ICON_W__ !important;
    width: __ICON_W__ !important;
    max-width: __ICON_W__ !important;
}

/* Refresh buttons: no inner padding, so the icon stays centred. */
.st-key-__BTN_TODAY__ button,
.st-key-__BTN_OD_TODAY__ button {
    padding: 0 !important;
    min-width: 0 !important;
    width: 100% !important;
    justify-content: center !important;
}

/* Make every wrapper inside a metric column respect the column width,
   so long text wraps instead of spilling into the next column. */
[class*="st-key-__METRICS__"] [data-testid="stColumn"] > *,
[class*="st-key-__METRICS__"] [data-testid="stColumn"] [data-testid="stElementContainer"],
[class*="st-key-__METRICS__"] [data-testid="stMetric"] {
    width: 100% !important;
    min-width: 0 !important;
    max-width: 100% !important;
}

[class*="st-key-__METRICS__"] [data-testid="stMetricValue"] {
    font-size: 1.4rem !important;
}

/* Let a long Gajapati name wrap (applies to the value and all its children). */
[class*="st-key-__METRICS__"] [data-testid="stMetricValue"],
[class*="st-key-__METRICS__"] [data-testid="stMetricValue"] * {
    white-space: normal !important;
    overflow: visible !important;
    text-overflow: clip !important;
    overflow-wrap: anywhere !important;
    word-break: normal;
    line-height: 1.2;
}

/* Calendar picker: hide the date text and show only an icon.
   Targets the whole widget, so it works whichever inner elements
   (input box or day / month / year segments) Streamlit renders. */
.st-key-__EN_PICKER__ {
    position: relative;
    cursor: pointer;
}
.st-key-__EN_PICKER__ [data-testid="stDateInput"] *,
.st-key-__EN_PICKER__ input {
    color: transparent !important;
    -webkit-text-fill-color: transparent !important;
    caret-color: transparent !important;
    cursor: pointer;
}

/* No coloured band: clear the highlight on the date text and its parts. */
.st-key-__EN_PICKER__ [data-testid="stDateInput"] *,
.st-key-__EN_PICKER__ [data-testid="stDateInput"] *::selection {
    background-color: transparent !important;
    box-shadow: none !important;
}

/* Look like the refresh button: plain box, theme border, no red focus. */
.st-key-__EN_PICKER__ [data-baseweb="input"],
.st-key-__EN_PICKER__ [data-baseweb="input"]:focus-within {
    background-color: transparent !important;
    border: 1px solid rgba(128, 128, 128, 0.4) !important;
    border-radius: 0.5rem;
}
.st-key-__EN_PICKER__:hover [data-baseweb="input"] {
    border-color: currentColor !important;
}

/* Material "calendar_month" icon, drawn in the theme's text colour. */
.st-key-__EN_PICKER__::after {
    content: "";
    position: absolute;
    left: 50%;
    top: 50%;
    width: 1.1rem;
    height: 1.1rem;
    transform: translate(-50%, -50%);
    background-color: currentColor;
    -webkit-mask: __CAL_SVG__ center / contain no-repeat;
    mask: __CAL_SVG__ center / contain no-repeat;
    pointer-events: none;
}
</style>
"""

_CSS_VALUES: dict[str, str] = {
    "__EN_DATE_ROW__": SessionKey.EN_DATE_ROW,
    "__OD_HEAD_ROW__": SessionKey.OD_HEAD_ROW,
    "__METRICS__": SessionKey.METRICS_PREFIX,
    "__BTN_TODAY__": SessionKey.BTN_TODAY,
    "__BTN_OD_TODAY__": SessionKey.BTN_OD_TODAY,
    "__EN_PICKER__": SessionKey.EN_PICKER,
    "__ICON_W__": ICON_COL_WIDTH,
    "__CAL_SVG__": _CALENDAR_SVG,
}

LAYOUT_CSS: str = _CSS_TEMPLATE
for _placeholder, _value in _CSS_VALUES.items():
    LAYOUT_CSS = LAYOUT_CSS.replace(_placeholder, _value)
