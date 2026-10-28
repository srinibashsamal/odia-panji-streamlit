"""Odia Panji converter: a Streamlit app for the odia-panji library.

Run locally:
    py -m pip install -r requirements.txt
    py -m streamlit run app.py
"""

from __future__ import annotations

import calendar
import json
from datetime import date, datetime
from typing import Any, TypeVar

import streamlit as st
from odia_panji import (
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

from app_constants import (
    EARLIEST_ANKA_DATE,
    IST,
    JATAKA_STYLE,
    JATAKA_TITLES,
    LAYOUT_CSS,
    MAX_DATE,
    MAX_UTKALABDA,
    MIN_DATE,
    MIN_UTKALABDA,
    MONTH_ABBR,
    PAKSHAS,
    REIGN_NAMES,
    STYLES,
    YEARS,
)

T = TypeVar("T")


# ---- Helpers --------------------------------------------------------------
def required(value: T | None) -> T:
    """Narrow an Optional widget value (None only when there are no options)."""
    if value is None:
        raise ValueError("A required input has no value.")
    return value


def clamp_date(day: date) -> date:
    """Limit `day` to the supported range MIN_DATE..MAX_DATE."""
    return max(MIN_DATE, min(MAX_DATE, day))


def today_ist() -> date:
    """Today in Puri; the server clock is often UTC, which lags IST."""
    return clamp_date(datetime.now(IST).date())


def parse_date_param(raw: str | None) -> date | None:
    """Parse an ISO date from a query parameter; None if missing or invalid."""
    if not raw:
        return None
    try:
        return clamp_date(date.fromisoformat(raw))
    except ValueError:
        return None


def tithi_options(paksha: str) -> list[str]:
    """Tithis 1-14, then Purnima (Shukla) or Amabasya (Krushna)."""
    return TITHI_NAMES + (["Purnima"] if paksha == "Shukla" else ["Amabasya"])


def lunar_text(result: dict[str, Any]) -> str:
    """Lunar date as text, e.g. "Adhika Jyestha Shukla Dasami"."""
    prefix = "Adhika " if result["adhika"] else ""
    return f"{prefix}{result['lunar_month']} {result['paksha']} {result['tithi']}"


def format_years(number: int, odia_digits: bool) -> str | int:
    """Show the number in Odia digits if selected."""
    return to_odia_numerals(number) if odia_digits else number


def month_label(month: int) -> str:
    """Month name for the dropdown, e.g. 10 -> "Oct"."""
    return MONTH_ABBR[month - 1]


def jataka_citation(day: date, result: dict[str, Any]) -> str:
    """Build a Jataka-style citation (always uses English digits)."""
    return (
        f"{JATAKA_TITLES} Shree Shree 108 Shree {result['gajapati']} "
        f"Maharajanka Vijaye Shubha Rajya Bardhane "
        f"A{result['anka']}nka Sna {result['utkalabda']} sala "
        f"Ingraji Ta- {day:%d/%m/%Y} rikha "
        f"Sauramana {result['solar_month']} Masa "
        f"Di{result['solar_day']}na "
        f"Chandriyamana {lunar_text(result)} {result['bara']}"
    )


# ---- Cached calculations --------------------------------------------------
@st.cache_data(show_spinner=False)
def cached_convert(day: date) -> dict[str, Any]:
    """Full English -> Odia conversion, with Anka."""
    return dict(convert(day))


@st.cache_data(show_spinner=False)
def cached_basic(day: date) -> dict[str, Any]:
    """Conversion without Anka, for dates before the first Gajapati."""
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


# Cache to_english directly so the cache always matches its parameters.
cached_to_english = st.cache_data(show_spinner=False)(to_english)


# ---- Details view ---------------------------------------------------------
def get_details(day: date) -> tuple[dict[str, Any], bool]:
    """Return (conversion result, whether Anka data is available)."""
    has_anka = day >= EARLIEST_ANKA_DATE
    result = cached_convert(day) if has_anka else cached_basic(day)
    return result, has_anka


def today_defaults() -> dict[str, Any]:
    """Today's Odia date, used to fill the Odia -> English form."""
    result, _ = get_details(today_ist())
    return result


def render_details(
    day: date, result: dict[str, Any], has_anka: bool, odia_digits: bool, key: str
) -> None:
    """Show the details; `key` keeps widget keys unique per tab."""
    with st.container(key=f"metrics_{key}"):
        # Narrow columns for the numbers, a wide one for the Gajapati's name.
        col1, col2, col3, col4 = st.columns([1, 0.7, 2.6, 1], gap="small")
        col1.metric("Utkalabda", format_years(result["utkalabda"], odia_digits))
        if has_anka:
            col2.metric("Anka", format_years(result["anka"], odia_digits))
            col3.metric("Gajapati", result["gajapati"])
        else:
            col2.metric("Anka", "—")
            col3.metric("Gajapati", "—")
        col4.metric("Shakabda", format_years(result["shakabda"], odia_digits))

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

        style_label: str = required(
            st.radio(
                "Citation style",
                list(STYLES) + [JATAKA_STYLE],
                horizontal=True,
                key=f"style_{key}",
            )
        )
        citation: str = (
            jataka_citation(day, result)
            if style_label == JATAKA_STYLE
            else format_historical(day, style=STYLES[style_label])
        )
        st.code(citation, language=None, wrap_lines=True)
    else:
        st.info(
            f"Anka years are available from {EARLIEST_ANKA_DATE:%d-%m-%Y} "
            "(earliest Gajapati in the library)."
        )

    with st.expander("All details"):
        st.code(
            json.dumps(result, indent=4, ensure_ascii=False, default=str),
            language="json",
        )


def show_odia_details(day: date, odia_digits: bool, key: str) -> None:
    """Get and show the Odia details for a date."""
    result, has_anka = get_details(day)
    render_details(day, result, has_anka, odia_digits, key)


# ---- English tab state ----------------------------------------------------
def set_en_date(day: date) -> None:
    """Set the Day, Month and Year dropdowns."""
    st.session_state["en_year"] = day.year
    st.session_state["en_month"] = day.month
    st.session_state["en_day"] = day.day


def set_en_date_today() -> None:
    """Refresh button: set today's date."""
    set_en_date(today_ist())


def set_en_date_from_picker() -> None:
    """Calendar picker: copy the picked date to the dropdowns."""
    set_en_date(st.session_state["en_picker"])


def current_en_date() -> date:
    """The date selected on the English tab."""
    return date(
        st.session_state["en_year"],
        st.session_state["en_month"],
        st.session_state["en_day"],
    )


# ---- Odia tab state -------------------------------------------------------
def od_today_values() -> dict[str, Any]:
    """Today's values for the Odia -> English form."""
    today = today_defaults()
    has_anka = today.get("anka") is not None
    paksha = today["paksha"] if today["paksha"] in PAKSHAS else PAKSHAS[0]
    tithis = tithi_options(paksha)
    return {
        "od_utkalabda": min(max(today["utkalabda"], MIN_UTKALABDA), MAX_UTKALABDA),
        "od_anka": today.get("anka", 2),
        "od_gajapati": (
            today["gajapati"]
            if today.get("gajapati") in REIGN_NAMES
            else REIGN_NAMES[0]
        ),
        "od_rashi": today["solar_month"] if today["solar_month"] in RASHI else RASHI[0],
        "od_solar_day": today["solar_day"],
        "od_lunar_month": (
            today["lunar_month"]
            if today["lunar_month"] in LUNAR_MONTHS
            else LUNAR_MONTHS[0]
        ),
        "lunar_paksha": paksha,
        "lunar_tithi": today["tithi"] if today["tithi"] in tithis else tithis[0],
        "od_adhika": bool(today["adhika"]),
        "od_year_type": "Anka" if has_anka else "Utkalabda",
        "od_date_type": "Solar",
    }


def init_od_inputs() -> None:
    """Fill the Odia form with today's values on first load."""
    for input_key, value in od_today_values().items():
        if input_key not in st.session_state:
            st.session_state[input_key] = value


def reset_od_to_today() -> None:
    """Refresh button: reset the Odia form to today."""
    st.session_state.update(od_today_values())


# ---- Page -----------------------------------------------------------------
st.set_page_config(page_title="Odia Panji Converter", page_icon="📅", layout="centered")
st.markdown(LAYOUT_CSS, unsafe_allow_html=True)

st.title("📅 Odia Panji Converter")
st.caption(
    "Convert between English (Gregorian) dates and the Odia calendar: "
    "Utkalabda, Anka, tithi, solar month, Shakabda and bara."
)

odia_digits: bool = st.toggle("Show years in Odia digits (୧୪୩୪)", key="digits_shared")

english_tab, odia_tab, about_tab = st.tabs(
    ["English → Odia", "Odia → English", "About"]
)

# ---- English -> Odia
with english_tab:
    # First load: use the date from the URL, or today.
    if "en_year" not in st.session_state:
        initial = parse_date_param(st.query_params.get("date")) or today_ist()
        set_en_date(initial)

    st.markdown("**English (Gregorian) Date**")
    with st.container(key="en_date_row"):
        col_day, col_month, col_year, col_today, col_pick = st.columns(
            [1.1, 1.4, 1.5, 0.55, 0.55], vertical_alignment="bottom"
        )
        # Fix the day if the month is shorter (e.g. 31 Jan -> Feb).
        days_in_month: int = calendar.monthrange(
            st.session_state["en_year"], st.session_state["en_month"]
        )[1]
        if st.session_state["en_day"] > days_in_month:
            st.session_state["_clamped_from"] = st.session_state["en_day"]
            st.session_state["en_day"] = days_in_month

        # Sync the calendar with the dropdowns (must run before it is drawn).
        st.session_state["en_picker"] = current_en_date()

        col_day.selectbox("Day", list(range(1, days_in_month + 1)), key="en_day")
        col_month.selectbox(
            "Month",
            list(range(1, 13)),
            format_func=month_label,
            key="en_month",
        )
        col_year.selectbox("Year", YEARS, key="en_year")
        col_today.button(
            ":material/refresh:",
            on_click=set_en_date_today,
            key="btn_today",
            help="Today",
            width="stretch",
        )
        col_pick.date_input(
            "Pick a date",
            min_value=MIN_DATE,
            max_value=MAX_DATE,
            format="DD/MM/YYYY",
            key="en_picker",
            on_change=set_en_date_from_picker,
            label_visibility="collapsed",
            help="Pick a date",
        )

    if "_clamped_from" in st.session_state:
        clamped_from = st.session_state.pop("_clamped_from")
        st.toast(
            f"Day adjusted from {clamped_from} "
            f"to {st.session_state['en_day']} "
            f"({month_label(st.session_state['en_month'])} has "
            f"{days_in_month} days)."
        )

    picked: date = current_en_date()

    # Update the URL only when the date changes (avoids extra reruns).
    if st.query_params.get("date") != picked.isoformat():
        st.query_params["date"] = picked.isoformat()

    st.caption("The page link updates with the date, so you can copy it to share.")

    try:
        with st.spinner("Calculating..."):
            show_odia_details(picked, odia_digits, key="en")
    except OdiaCalendarError as exc:
        st.error(str(exc))

# ---- Odia -> English
with odia_tab:
    init_od_inputs()

    with st.container(key="od_head_row"):
        col_year_type, col_date_type, col_od_today = st.columns(
            [2, 2, 0.55], vertical_alignment="bottom"
        )
        year_type = col_year_type.radio(
            "Year given as",
            ["Utkalabda", "Anka"],
            horizontal=True,
            key="od_year_type",
        )
        date_type = col_date_type.radio(
            "Date given as",
            ["Solar", "Lunar"],
            horizontal=True,
            key="od_date_type",
        )
        col_od_today.button(
            ":material/refresh:",
            on_click=reset_od_to_today,
            key="btn_od_today",
            help="Today",
            width="stretch",
        )

    utkalabda: int | None = None
    anka: int | None = None
    gajapati: str | None = None
    ready: bool = True

    if year_type == "Utkalabda":
        utkalabda = int(
            st.number_input(
                "Utkalabda year",
                min_value=MIN_UTKALABDA,
                max_value=MAX_UTKALABDA,
                step=1,
                key="od_utkalabda",
            )
        )
    else:
        col_anka, col_king = st.columns([1, 2])
        anka = int(col_anka.number_input("Anka", min_value=2, step=1, key="od_anka"))
        gajapati = col_king.selectbox("Gajapati", REIGN_NAMES, key="od_gajapati")
        if not is_valid_anka(anka):
            ready = False
            st.warning(
                f"{anka} is not a valid Anka. Ankas skip 1, and any number "
                "ending in 6 or 0 (except 10)."
            )

    month: str
    solar_day: int | None = None
    paksha: str | None = None
    tithi: str | None = None
    adhika: bool = False

    if date_type == "Solar":
        col_rashi, col_solar_day = st.columns([2, 1])
        month = required(
            col_rashi.selectbox("Solar month (rashi)", RASHI, key="od_rashi")
        )
        solar_day = int(
            col_solar_day.number_input(
                "Day", min_value=1, max_value=32, step=1, key="od_solar_day"
            )
        )
    else:
        month = required(
            st.selectbox("Lunar month", LUNAR_MONTHS, key="od_lunar_month")
        )
        col_paksha, col_tithi = st.columns(2)
        paksha = required(col_paksha.selectbox("Paksha", PAKSHAS, key="lunar_paksha"))

        # When paksha changes, swap Purnima <-> Amabasya instead of resetting.
        options: list[str] = tithi_options(paksha)
        current: str | None = st.session_state.get("lunar_tithi")
        if current not in options:
            st.session_state["lunar_tithi"] = options[-1]

        tithi = required(col_tithi.selectbox("Tithi", options, key="lunar_tithi"))
        adhika = st.checkbox(
            "Adhika (intercalary) month",
            help="Set from today on first load; keeps your choice after that.",
            key="od_adhika",
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
            show_odia_details(result_date, odia_digits, key="od")
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
