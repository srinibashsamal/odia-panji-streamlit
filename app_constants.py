"""Constants for the Odia Panji Streamlit app (dates, labels, styles, CSS)."""

from __future__ import annotations

from datetime import date, timedelta, timezone
from typing import Dict, List

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

REIGN_NAMES: List[str] = [
    reign.name for reign in reversed(GAJAPATI_REIGNS)
]  # current first
MONTH_ABBR: List[str] = "Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec".split()
YEARS: List[int] = list(range(MIN_DATE.year, MAX_DATE.year + 1))
PAKSHAS: List[str] = ["Shukla", "Krushna"]

STYLES: Dict[str, HistoricalStyle] = {
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

LAYOUT_CSS = """
<style>
.st-key-en_date_row [data-testid="stHorizontalBlock"],
[class*="st-key-metrics_"] [data-testid="stHorizontalBlock"] {
    flex-wrap: nowrap !important;
    gap: 0.5rem !important;
}
.st-key-en_date_row [data-testid="stColumn"],
.st-key-en_date_row [data-testid="column"],
[class*="st-key-metrics_"] [data-testid="stColumn"],
[class*="st-key-metrics_"] [data-testid="column"] {
    min-width: 0 !important;
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

/* Refresh buttons: hide the font-icon (it gets clipped in narrow columns)
   and draw the icon with a mask, like the calendar button. */
.st-key-btn_today button,
.st-key-btn_od_today button {
    position: relative;
    padding: 0 !important;
    min-width: 0 !important;
    overflow: visible !important;
}
.st-key-btn_today button > *,
.st-key-btn_od_today button > * {
    visibility: hidden;
}
.st-key-btn_today button::after,
.st-key-btn_od_today button::after {
    content: "";
    position: absolute;
    left: 50%;
    top: 50%;
    width: 1.1rem;
    height: 1.1rem;
    transform: translate(-50%, -50%);
    background-color: currentColor;
    -webkit-mask: url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 -960 960 960'><path d='M480-160q-134 0-227-93t-93-227q0-134 93-227t227-93q69 0 132 28.5T720-690v-110h80v280H520v-80h168q-32-56-87.5-88T480-720q-100 0-170 70t-70 170q0 100 70 170t170 70q77 0 139-44t87-116h84q-28 106-114 173t-196 67Z'/></svg>") center / contain no-repeat;
    mask: url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 -960 960 960'><path d='M480-160q-134 0-227-93t-93-227q0-134 93-227t227-93q69 0 132 28.5T720-690v-110h80v280H520v-80h168q-32-56-87.5-88T480-720q-100 0-170 70t-70 170q0 100 70 170t170 70q77 0 139-44t87-116h84q-28 106-114 173t-196 67Z'/></svg>") center / contain no-repeat;
    pointer-events: none;
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
    -webkit-mask: url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 -960 960 960'><path d='M200-80q-33 0-56.5-23.5T120-160v-560q0-33 23.5-56.5T200-800h40v-80h80v80h320v-80h80v80h40q33 0 56.5 23.5T840-720v560q0 33-23.5 56.5T760-80H200Zm0-80h560v-400H200v400Zm0-480h560v-80H200v80Zm0 0v-80 80Zm280 240q-17 0-28.5-11.5T440-440q0-17 11.5-28.5T480-480q17 0 28.5 11.5T520-440q0 17-11.5 28.5T480-400Zm-160 0q-17 0-28.5-11.5T280-440q0-17 11.5-28.5T320-480q17 0 28.5 11.5T360-440q0 17-11.5 28.5T320-400Zm320 0q-17 0-28.5-11.5T600-440q0-17 11.5-28.5T640-480q17 0 28.5 11.5T680-440q0 17-11.5 28.5T640-400ZM480-240q-17 0-28.5-11.5T440-280q0-17 11.5-28.5T480-320q17 0 28.5 11.5T520-280q0 17-11.5 28.5T480-240Zm-160 0q-17 0-28.5-11.5T280-280q0-17 11.5-28.5T320-320q17 0 28.5 11.5T360-280q0 17-11.5 28.5T320-240Zm320 0q-17 0-28.5-11.5T600-280q0-17 11.5-28.5T640-320q17 0 28.5 11.5T680-280q0 17-11.5 28.5T640-240Z'/></svg>") center / contain no-repeat;
    mask: url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 -960 960 960'><path d='M200-80q-33 0-56.5-23.5T120-160v-560q0-33 23.5-56.5T200-800h40v-80h80v80h320v-80h80v80h40q33 0 56.5 23.5T840-720v560q0 33-23.5 56.5T760-80H200Zm0-80h560v-400H200v400Zm0-480h560v-80H200v80Zm0 0v-80 80Zm280 240q-17 0-28.5-11.5T440-440q0-17 11.5-28.5T480-480q17 0 28.5 11.5T520-440q0 17-11.5 28.5T480-400Zm-160 0q-17 0-28.5-11.5T280-440q0-17 11.5-28.5T320-480q17 0 28.5 11.5T360-440q0 17-11.5 28.5T320-400Zm320 0q-17 0-28.5-11.5T600-440q0-17 11.5-28.5T640-480q17 0 28.5 11.5T680-440q0 17-11.5 28.5T640-400ZM480-240q-17 0-28.5-11.5T440-280q0-17 11.5-28.5T480-320q17 0 28.5 11.5T520-280q0 17-11.5 28.5T480-240Zm-160 0q-17 0-28.5-11.5T280-280q0-17 11.5-28.5T320-320q17 0 28.5 11.5T360-280q0 17-11.5 28.5T320-240Zm320 0q-17 0-28.5-11.5T600-280q0-17 11.5-28.5T640-320q17 0 28.5 11.5T680-280q0 17-11.5 28.5T640-240Z'/></svg>") center / contain no-repeat;
    pointer-events: none;
}
</style>
"""
