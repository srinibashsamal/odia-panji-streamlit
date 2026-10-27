"""Constants for the Odia Panji Streamlit app (dates, labels, styles, CSS)."""

from __future__ import annotations

from datetime import date, timedelta, timezone

from odia_panji import GAJAPATI_REIGNS, HistoricalStyle, utkalabda_year

# ---- Constants ------------------------------------------------------------
IST = timezone(timedelta(hours=5, minutes=30), name="IST")

# Dates the library is trusted for (see the README's "Limitations").
MIN_DATE: date = date(1800, 1, 1)
MAX_DATE: date = date(2100, 12, 31)
EARLIEST_ANKA_DATE: date = GAJAPATI_REIGNS[0].accession

# Derived from the library: Utkalabda changes mid-year, so "year - 592" is
# off by one for part of every year.
MIN_UTKALABDA: int = utkalabda_year(MIN_DATE)
MAX_UTKALABDA: int = utkalabda_year(MAX_DATE)

REIGN_NAMES: list[str] = [
    reign.name for reign in reversed(GAJAPATI_REIGNS)
]  # current first
MONTH_ABBR: list[str] = "Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec".split()
YEARS: list[int] = list(range(MIN_DATE.year, MAX_DATE.year + 1))
PAKSHAS: list[str] = ["Shukla", "Krushna"]

STYLES: dict[str, HistoricalStyle] = {
    "Full": "full",
    "Compact (one line)": "compact",
    "Lunar first": "lunar",
    "Solar first": "solar",
}
JATAKA_STYLE: str = "Jataka"

JATAKA_TITLES: str = (
    "Shree Shree Shree Veerashree Gajapati Gaudeshwara "
    "Nava Koti Karnatotkala Kalabargeshwara Abhiraya Bhuta Bhairaba "
    "Duhsaha Duhshasana Anikarane Rautaraya Shasanotteerna "
    "Atulabala Parakrama Sangrame Sahasrabahu Kshatriyakula Dhumaketu "
    "Airi Dalaganjana Matta Gaja Veeradhiveerabara "
    "Prabala Pratapi Maharajadhiraja"
)

# Width of the square icon columns (refresh button and calendar picker).
ICON_COL_WIDTH: str = "2.6rem"

# Base64-encoded Material "calendar_month" SVG: more reliable in CSS masks
# than the plain utf8 data URI (older Firefox was picky about it).
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

LAYOUT_CSS = """
<style>
.st-key-en_date_row [data-testid="stHorizontalBlock"],
.st-key-od_head_row [data-testid="stHorizontalBlock"],
[class*="st-key-metrics_"] [data-testid="stHorizontalBlock"] {
    flex-wrap: nowrap !important;
    gap: 0.5rem !important;
}
.st-key-en_date_row [data-testid="stColumn"],
.st-key-en_date_row [data-testid="column"],
.st-key-od_head_row [data-testid="stColumn"],
.st-key-od_head_row [data-testid="column"],
[class*="st-key-metrics_"] [data-testid="stColumn"],
[class*="st-key-metrics_"] [data-testid="column"] {
    min-width: 0 !important;
}

/* Icon columns: fixed square width on every screen size, so the icons
   never get squeezed on phones. The other columns share the rest. */
.st-key-en_date_row [data-testid="stColumn"]:nth-child(n+4),
.st-key-en_date_row [data-testid="column"]:nth-child(n+4),
.st-key-od_head_row [data-testid="stColumn"]:last-child,
.st-key-od_head_row [data-testid="column"]:last-child {
    flex: 0 0 ICON_W !important;
    width: ICON_W !important;
    max-width: ICON_W !important;
}

/* Refresh buttons: no inner padding, so the icon stays centred. */
.st-key-btn_today button,
.st-key-btn_od_today button {
    padding: 0 !important;
    min-width: 0 !important;
    width: 100% !important;
    justify-content: center !important;
}

/* Make every wrapper inside a metric column respect the column width,
   so long text wraps instead of spilling into the next column. */
[class*="st-key-metrics_"] [data-testid="stColumn"] > *,
[class*="st-key-metrics_"] [data-testid="stColumn"] [data-testid="stElementContainer"],
[class*="st-key-metrics_"] [data-testid="stMetric"] {
    width: 100% !important;
    min-width: 0 !important;
    max-width: 100% !important;
}

[class*="st-key-metrics_"] [data-testid="stMetricValue"] {
    font-size: 1.4rem !important;
}

/* Let a long Gajapati name wrap (applies to the value and all its children). */
[class*="st-key-metrics_"] [data-testid="stMetricValue"],
[class*="st-key-metrics_"] [data-testid="stMetricValue"] * {
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
.st-key-en_picker {
    position: relative;
    cursor: pointer;
}
.st-key-en_picker [data-testid="stDateInput"] *,
.st-key-en_picker input {
    color: transparent !important;
    -webkit-text-fill-color: transparent !important;
    caret-color: transparent !important;
    cursor: pointer;
}

/* No coloured band: clear the highlight on the date text and its parts. */
.st-key-en_picker [data-testid="stDateInput"] *,
.st-key-en_picker [data-testid="stDateInput"] *::selection {
    background-color: transparent !important;
    box-shadow: none !important;
}

/* Look like the refresh button: plain box, theme border, no red focus. */
.st-key-en_picker [data-baseweb="input"],
.st-key-en_picker [data-baseweb="input"]:focus-within {
    background-color: transparent !important;
    border: 1px solid rgba(128, 128, 128, 0.4) !important;
    border-radius: 0.5rem;
}
.st-key-en_picker:hover [data-baseweb="input"] {
    border-color: currentColor !important;
}

/* Material "calendar_month" icon, drawn in the theme's text colour. */
.st-key-en_picker::after {
    content: "";
    position: absolute;
    left: 50%;
    top: 50%;
    width: 1.1rem;
    height: 1.1rem;
    transform: translate(-50%, -50%);
    background-color: currentColor;
    -webkit-mask: CAL_SVG center / contain no-repeat;
    mask: CAL_SVG center / contain no-repeat;
    pointer-events: none;
}
</style>
""".replace("ICON_W", ICON_COL_WIDTH).replace("CAL_SVG", _CALENDAR_SVG)
