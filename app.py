"""Odia Panji converter: a simple Streamlit front end for the odia-panji library.

Run locally:
    py -m pip install -r requirements.txt
    py -m streamlit run app.py
"""

from __future__ import annotations

import calendar
from datetime import date, datetime, timedelta, timezone
from typing import Any, Dict, List, Optional, Tuple, TypeVar, Union

import streamlit as st

from odia_panji import (
    GAJAPATI_REIGNS,
    HistoricalStyle,
    OdiaCalendarError,
    __version__,
    convert,
    format_historical,
    is_valid_anka,
    lunar_date,
    odia_solar_date,
    shaka_year,
    to_english,
    to_odia_numerals,
    utkalabda_year,
)
from odia_panji.constants import (
    ENGLISH_WEEKDAYS,
    LUNAR_MONTHS,
    ODIA_WEEKDAYS,
    RASHI,
    TITHI_NAMES,
)

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
</style>
"""

T = TypeVar("T")


# ---- Pure helpers (no Streamlit calls) ------------------------------------
def required(value: Optional[T]) -> T:
    """Narrow an Optional widget value (None only when there are no options)."""
    if value is None:
        raise ValueError("A required input has no value.")
    return value


def clamp_date(day: date) -> date:
    """Limit ``day`` to the supported range MIN_DATE..MAX_DATE."""
    return max(MIN_DATE, min(MAX_DATE, day))


def today_ist() -> date:
    """Today in Puri; the server clock is often UTC, which lags IST."""
    return clamp_date(datetime.now(IST).date())


def parse_date_param(raw: Optional[str]) -> Optional[date]:
    """Parse an ISO date from a query parameter; None if missing or invalid."""
    if not raw:
        return None
    try:
        return clamp_date(date.fromisoformat(raw))
    except ValueError:
        return None


def tithi_options(paksha: str) -> List[str]:
    """Tithis 1-14, then Purnima (Shukla) or Amabasya (Krushna)."""
    return TITHI_NAMES + (["Purnima"] if paksha == "Shukla" else ["Amabasya"])


def lunar_text(result: Dict[str, Any]) -> str:
    """Lunar date as text, e.g. ``"Adhika Jyestha Shukla Dasami"``."""
    prefix = "Adhika " if result["adhika"] else ""
    return f"{prefix}{result['lunar_month']} {result['paksha']} {result['tithi']}"


def display_number(number: int, odia_digits: bool) -> Union[int, str]:
    """Return ``number`` unchanged, or in Odia digits when requested."""
    return to_odia_numerals(number) if odia_digits else number


def index_of(options: List[str], value: Any, fallback: int = 0) -> int:
    """Position of ``value`` in ``options``, or ``fallback`` if absent."""
    return options.index(value) if value in options else fallback


def month_label(month: int) -> str:
    """Selectbox label for a month number, e.g. 10 -> ``"Oct"``."""
    return MONTH_ABBR[month - 1]


# ---- Cached library calls (the astronomy is computed) ---------------------
@st.cache_data(show_spinner=False)
def cached_convert(day: date) -> Dict[str, Any]:
    """Full English -> Odia conversion, including the Anka."""
    return dict(convert(day))


@st.cache_data(show_spinner=False)
def cached_basic(day: date) -> Dict[str, Any]:
    """Conversion without the Anka, for dates before the earliest reign."""
    lunar = lunar_date(day)
    solar = odia_solar_date(day)
    return {
        "english_date": day.strftime("%d-%m-%Y"),
        "weekday": ENGLISH_WEEKDAYS[day.weekday()],
        "bara": ODIA_WEEKDAYS[day.weekday()],
        "utkalabda": utkalabda_year(day),
        "lunar_month": lunar.month,
        "adhika": lunar.adhika,
        "paksha": lunar.paksha,
        "tithi": lunar.tithi,
        "solar_month": solar.month,
        "solar_day": solar.day,
        "solar_month_lunar_equivalent": solar.lunar_equivalent,
        "shakabda": shaka_year(day),
    }


@st.cache_data(show_spinner=False)
def cached_to_english(
    month: str,
    day: Optional[int] = None,
    paksha: Optional[str] = None,
    tithi: Optional[str] = None,
    adhika: bool = False,
    utkalabda: Optional[int] = None,
    anka: Optional[int] = None,
    gajapati: Optional[str] = None,
) -> date:
    """Odia -> English conversion; see :func:`odia_panji.to_english`."""
    return to_english(
        month,
        day,
        paksha=paksha,
        tithi=tithi,
        adhika=adhika,
        utkalabda=utkalabda,
        anka=anka,
        gajapati=gajapati,
    )


# ---- Details view ---------------------------------------------------------
def get_details(day: date) -> Tuple[Dict[str, Any], bool]:
    """Return (conversion result, whether Anka data is available)."""
    has_anka = day >= EARLIEST_ANKA_DATE
    result = cached_convert(day) if has_anka else cached_basic(day)
    return result, has_anka


def today_defaults() -> Dict[str, Any]:
    """Today's Odia date (IST), used to pre-fill the Odia -> English form."""
    result, _ = get_details(today_ist())
    return result


def render_details(
    day: date, result: Dict[str, Any], has_anka: bool, odia_digits: bool, key: str
) -> None:
    """Render the details; ``key`` keeps widget keys unique across tabs."""
    # Four metrics on one row; the container key lets the CSS above stop
    # them stacking on phones.
    with st.container(key=f"metrics_{key}"):
        # Narrow columns for the numbers, a wide one for the Gajapati's name.
        col1, col2, col3, col4 = st.columns([1, 0.7, 2.6, 1], gap="small")
        col1.metric("Utkalabda", display_number(result["utkalabda"], odia_digits))
        if has_anka:
            col2.metric("Anka", display_number(result["anka"], odia_digits))
            col3.metric("Gajapati", result["gajapati"])
        else:
            col2.metric("Anka", "—")
            col3.metric("Gajapati", "—")
        col4.metric("Shakabda", display_number(result["shakabda"], odia_digits))

    st.markdown(f"**Day:** {result['bara']} ({result['weekday']})")
    st.markdown(f"**Lunar date:** {lunar_text(result)}")
    st.markdown(
        f"**Solar date:** {result['solar_day']} {result['solar_month']} "
        f"(lunar equivalent: {result['solar_month_lunar_equivalent']})"
    )

    if has_anka:
        st.markdown(
            f"**Gajapati:** {result['gajapati']} "
            f"(acceded {result['gajapati_accession']})"
        )
        st.markdown(
            f"**Odia year:** {result['odia_year_start']} to {result['odia_year_end']} "
            f"(Sunia: {result['sunia_of_year']})"
        )
        if result["is_accession_day"]:
            st.info(
                "This is a Gajapati accession day; it is credited to the "
                "incoming monarch."
            )

        style_label = required(
            st.radio(
                "Citation style", list(STYLES), horizontal=True, key=f"style_{key}"
            )
        )
        st.code(
            format_historical(day, style=STYLES[style_label]),
            language=None,
            wrap_lines=True,
        )
    else:
        st.info(
            f"Anka years are available from {EARLIEST_ANKA_DATE:%d-%m-%Y} "
            "(earliest Gajapati in the library)."
        )

    with st.expander("All details"):
        st.json(result)


def show_odia_details(day: date, odia_digits: bool, key: str) -> None:
    """Look up and render the Odia details for ``day``."""
    result, has_anka = get_details(day)
    render_details(day, result, has_anka, odia_digits, key)


# ---- English date picker state --------------------------------------------
def set_en_date(day: date) -> None:
    """Store ``day`` in the Day / Month / Year selectboxes."""
    st.session_state["en_year"] = day.year
    st.session_state["en_month"] = day.month
    st.session_state["en_day"] = day.day


def set_en_date_today() -> None:
    """Callback for the "Today" button."""
    set_en_date(today_ist())


# ---- Page -----------------------------------------------------------------
st.set_page_config(page_title="Odia Panji Converter", page_icon="📅", layout="centered")
st.markdown(LAYOUT_CSS, unsafe_allow_html=True)

st.title("📅 Odia Panji Converter")
st.caption(
    "Convert between English (Gregorian) dates and the Odia calendar: "
    "Utkalabda, Anka, tithi, solar month, Shakabda and bara."
)

english_tab, odia_tab, about_tab = st.tabs(
    ["English → Odia", "Odia → English", "About"]
)

# ---- English -> Odia
with english_tab:
    # Initialise once, from a shared link (?date=YYYY-MM-DD) or today.
    if "en_year" not in st.session_state:
        set_en_date(parse_date_param(st.query_params.get("date")) or today_ist())

    st.markdown("**English (Gregorian) Date**")
    with st.container(key="en_date_row"):
        col_day, col_month, col_year, col_today = st.columns(
            [1.1, 1.4, 1.5, 1.4], vertical_alignment="bottom"
        )
        # Clamp the day when month/year change (e.g. 31 Jan -> Feb).
        days_in_month: int = calendar.monthrange(
            st.session_state["en_year"], st.session_state["en_month"]
        )[1]
        if st.session_state["en_day"] > days_in_month:
            st.session_state["en_day"] = days_in_month

        col_day.selectbox("Day", list(range(1, days_in_month + 1)), key="en_day")
        col_month.selectbox(
            "Month",
            list(range(1, 13)),
            format_func=month_label,
            key="en_month",
        )
        col_year.selectbox("Year", YEARS, key="en_year")
        col_today.button(
            "Today", on_click=set_en_date_today, key="btn_today", width="stretch"
        )

    picked: date = date(
        st.session_state["en_year"],
        st.session_state["en_month"],
        st.session_state["en_day"],
    )

    # Writing a query param triggers a rerun, so only write when it changed.
    if st.query_params.get("date") != picked.isoformat():
        st.query_params["date"] = picked.isoformat()
    st.caption("The page link updates with the date, so you can copy it to share.")

    odia_digits: bool = st.toggle("Show years in Odia digits (୧୪୩୪)", key="digits_en")
    try:
        with st.spinner("Calculating..."):
            show_odia_details(picked, odia_digits, key="en")
    except OdiaCalendarError as exc:
        st.error(str(exc))

# ---- Odia -> English
with odia_tab:
    defaults = today_defaults()

    col_year_type, col_date_type = st.columns(2)
    year_type = col_year_type.radio(
        "Year given as", ["Utkalabda", "Anka"], horizontal=True
    )
    date_type = col_date_type.radio(
        "Date given as", ["Solar", "Lunar"], horizontal=True
    )

    utkalabda: Optional[int] = None
    anka: Optional[int] = None
    gajapati: Optional[str] = None
    ready: bool = True

    if year_type == "Utkalabda":
        utkalabda = int(
            st.number_input(
                "Utkalabda year",
                min_value=MIN_UTKALABDA,
                max_value=MAX_UTKALABDA,
                value=min(max(defaults["utkalabda"], MIN_UTKALABDA), MAX_UTKALABDA),
                step=1,
            )
        )
    else:
        col_anka, col_king = st.columns([1, 2])
        anka = int(
            col_anka.number_input(
                "Anka", min_value=2, value=defaults.get("anka", 2), step=1
            )
        )
        gajapati = col_king.selectbox("Gajapati", REIGN_NAMES)
        if not is_valid_anka(anka):
            ready = False
            st.warning(
                f"{anka} is not a valid Anka: 1, numbers ending in 6, and "
                "numbers ending in 0 (except 10) are skipped."
            )

    month: str
    solar_day: Optional[int] = None
    paksha: Optional[str] = None
    tithi: Optional[str] = None
    adhika: bool = False

    if date_type == "Solar":
        col_rashi, col_solar_day = st.columns([2, 1])
        month = required(
            col_rashi.selectbox(
                "Solar month (rashi)",
                RASHI,
                index=index_of(RASHI, defaults["solar_month"]),
            )
        )
        solar_day = int(
            col_solar_day.number_input(
                "Day", min_value=1, max_value=32, value=defaults["solar_day"], step=1
            )
        )
    else:
        month = required(
            st.selectbox(
                "Lunar month",
                LUNAR_MONTHS,
                index=index_of(LUNAR_MONTHS, defaults["lunar_month"]),
            )
        )
        col_paksha, col_tithi = st.columns(2)
        paksha = required(
            col_paksha.selectbox(
                "Paksha",
                PAKSHAS,
                index=index_of(PAKSHAS, defaults["paksha"]),
                key="lunar_paksha",
            )
        )

        # Keep the tithi when the paksha changes: only the 15th entry differs
        # (Purnima <-> Amabasya), so map it across instead of resetting.
        options: List[str] = tithi_options(paksha)
        current: Optional[str] = st.session_state.get("lunar_tithi")
        if current is None:
            st.session_state["lunar_tithi"] = (
                defaults["tithi"] if defaults["tithi"] in options else options[0]
            )
        elif current not in options:
            st.session_state["lunar_tithi"] = options[-1]

        tithi = required(col_tithi.selectbox("Tithi", options, key="lunar_tithi"))
        adhika = st.checkbox(
            "Adhika (intercalary) month",
            value=defaults["adhika"],
            help="Starts ticked only if today falls in an adhika month.",
        )

    st.divider()
    if ready:
        try:
            with st.spinner("Searching..."):
                result_date = cached_to_english(
                    month,
                    day=solar_day,
                    paksha=paksha,
                    tithi=tithi,
                    adhika=adhika,
                    utkalabda=utkalabda,
                    anka=anka,
                    gajapati=gajapati,
                )
            st.success(f"**{result_date:%A, %d %B %Y}**")
            odia_digits_rev: bool = st.toggle(
                "Show years in Odia digits (୧୪୩୪)", key="digits_od"
            )
            show_odia_details(result_date, odia_digits_rev, key="od")
        except OdiaCalendarError as exc:
            st.error(str(exc))

# ---- About
with about_tab:
    st.markdown(f"""
Built on [**odia-panji**](https://pypi.org/project/odia-panji/) v{__version__}
by Srinibash Samal ([GitHub](https://github.com/srinibashsamal/odia-panji)).

- Sunia, tithis and sankrantis are **computed** from the Sun and Moon, observed
  from **Puri** in **IST**.
- Lunar months are **Purnimanta**; a tithi belongs to the day whose sunrise
  falls inside it.
- Results are trusted for roughly **1800-2100**, so this app is limited to
  that range.
- Anka years are available from **{EARLIEST_ANKA_DATE:%d-%m-%Y}**.
- Printed panjis can differ by a day near a boundary.
""")

    with st.expander("💡 Inspiration"):
        st.markdown("""
The inspiration behind this project came when I encountered a Jataka (ଜାତକ) that
recorded only the traditional Odia year and Anka. When I tried to convert these
dates into their corresponding Gregorian dates and years, I faced several
challenges.

That experience led me to think: *Why not build a simple tool that makes these
conversions easier and more accessible?*

That idea eventually led to the development of **odia-panji**, a Python library
for Odia calendar conversions, and this Streamlit web application built on top
of it.
""")

    with st.expander("🎯 Purpose"):
        st.markdown("""
The goal is to make Odia calendar date conversions accessible and hassle-free
for everyone. I hope this tool will be useful to historians, researchers,
genealogists, and anyone interested in exploring Odisha's history, heritage, and
traditional calendar system.

By bridging traditional Odia dates with the Gregorian calendar, I hope to make
historical records easier to interpret and help people connect with Odisha's
rich cultural past.
""")
