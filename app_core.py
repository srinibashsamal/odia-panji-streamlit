"""Core logic for the Odia Panji Streamlit app (no page layout).

Contains the language helpers, cached calculations, citations and the
session-state helpers used by the forms. ``app.py`` draws the page.

Note: this module is imported once per server process, so nothing here may
decide the language at import time. Always call ``current_texts()``, which
reads the language from the current session on every call.
"""

from __future__ import annotations

from datetime import date, datetime
from types import ModuleType
from typing import Any, TypedDict, TypeVar

import streamlit as st
from odia_panji import (
    convert,
    format_historical,
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

import app_text_en
import app_text_od
from app_constants import (
    DATE_SOLAR,
    EARLIEST_ANKA_DATE,
    IST,
    JATAKA_STYLE,
    MAX_DATE,
    MAX_UTKALABDA,
    MIN_DATE,
    MIN_UTKALABDA,
    PAKSHAS,
    REIGN_NAMES,
    TRANSLATED_SELECTBOXES,
    TRANSLATED_TERMS,
    YEAR_ANKA,
    YEAR_UTKALABDA,
    YEARS,
    SessionKey,
)

T = TypeVar("T")


# ---- Result shape ---------------------------------------------------------


class ConversionResult(TypedDict, total=False):
    """Shape of the dict returned by convert() / cached_basic().

    Mirrors odia_panji's OdiaConversion. cached_basic() (dates before the
    first Gajapati) fills only the fields that don't need Anka data.
    """

    english_date: str
    weekday: str
    bara: str
    utkalabda: int
    utkalabda_odia: str
    gajapati: str
    gajapati_accession: str
    is_accession_day: bool
    anka: int
    anka_odia: str
    anka_index: int
    years_since_accession: int
    odia_year_start: str
    odia_year_end: str
    sunia_of_year: str
    lunar_month: str
    adhika: bool
    paksha: str
    tithi: str
    solar_rashi: str
    solar_month: str
    solar_day: int
    solar_month_lunar_equivalent: str
    shakabda: int


# ---- Language -------------------------------------------------------------


def is_odia() -> bool:
    """True when the Odia toggle is on for this session."""
    return bool(st.session_state.get(SessionKey.ODIA_MODE, False))


def current_texts() -> ModuleType:
    """Text module for the language selected in this session."""
    return app_text_od if is_odia() else app_text_en


def t(key: str, **values: Any) -> str:
    """Return the text for `key` in the current language, filled with `values`.

    A key missing from only one language file is caught at startup by
    assert_text_keys_match(). This fallback covers a key missing from both
    files (e.g. a typo in app.py): it shows a warning and returns the key.
    """
    template = current_texts().TEXT.get(key)
    if template is None:
        st.warning(f"Missing text key: {key}")
        return key
    return template.format(**values)


def num(value: int | str) -> str:
    """Format a number (or digit-containing text) in Odia digits when selected."""
    return to_odia_numerals(value) if current_texts().USE_ODIA_DIGITS else str(value)


def name(term: str) -> str:
    """Translate a library term (month, tithi, bara, Gajapati…) to the current language."""
    return current_texts().NAMES.get(term, term)


def month_label(month: int) -> str:
    """Short month name for the dropdown, e.g. 10 -> 'Oct' / Odia equivalent."""
    return current_texts().MONTHS[month - 1]


def long_month(month: int) -> str:
    """Full month name, e.g. 10 -> 'October' / Odia equivalent."""
    return current_texts().MONTHS_LONG[month - 1]


def style_label(style: str) -> str:
    """Display label for a citation style."""
    return current_texts().STYLE_LABELS.get(style, style)


def selectbox_labels(key: str, lang: ModuleType) -> dict[str, Any]:
    """Map every label that `lang` shows for the selectbox `key` to its value."""
    digits = to_odia_numerals if lang.USE_ODIA_DIGITS else str
    if key == SessionKey.EN_DAY:
        return {digits(d): d for d in range(1, 32)}
    if key == SessionKey.EN_MONTH:
        return {lang.MONTHS[m - 1]: m for m in range(1, 13)}
    if key == SessionKey.EN_YEAR:
        return {digits(y): y for y in YEARS}
    return {lang.NAMES.get(term, term): term for term in TRANSLATED_TERMS[key]}


def restore_selectbox_values() -> None:
    """Turn a label left over from the other language back into its value.

    Must run before the selectboxes are drawn; setting a widget's key is
    only allowed before the widget is created in the current run.
    """
    for key in TRANSLATED_SELECTBOXES:
        value = st.session_state.get(key)
        if not isinstance(value, str):
            continue
        for lang in (app_text_en, app_text_od):
            labels = selectbox_labels(key, lang)
            if value in labels:
                st.session_state[key] = labels[value]
                break


def assert_text_keys_match() -> None:
    """Fail fast if the English and Odia TEXT dicts don't have the same keys."""
    en_keys = set(app_text_en.TEXT)
    od_keys = set(app_text_od.TEXT)
    if en_keys != od_keys:
        missing_in_od = en_keys - od_keys
        missing_in_en = od_keys - en_keys
        raise RuntimeError(
            f"TEXT key mismatch between languages.\n"
            f"  Missing in Odia: {sorted(missing_in_od)}\n"
            f"  Missing in English: {sorted(missing_in_en)}"
        )


# ---- General helpers ------------------------------------------------------


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
    """Tithis 1–14, then Purnima (Shukla) or Amabasya (Krushna)."""
    return TITHI_NAMES + (["Purnima"] if paksha == "Shukla" else ["Amabasya"])


def lunar_text(result: ConversionResult) -> str:
    """Lunar date as text, e.g. 'Adhika Jyestha Shukla Dasami'."""
    prefix = t("adhika_prefix") if result.get("adhika") else ""
    return (
        f"{prefix}{name(result['lunar_month'])} "
        f"{name(result['paksha'])} {name(result['tithi'])}"
    )


def long_date(day: date) -> str:
    """Long form, e.g. '7 October 2026' / '୭ ଅକ୍ଟୋବର ୨୦୨୬'."""
    return t(
        "cite_english",
        day=num(day.day),
        month=long_month(day.month),
        year=num(day.year),
    )


# ---- Citations ------------------------------------------------------------


def jataka_citation(day: date, result: ConversionResult) -> str:
    """Build a Jataka-style citation in the current language."""
    return t(
        "jataka",
        titles=current_texts().GAJAPATI_UPADHI,
        gajapati=name(result["gajapati"]),
        anka=num(result["anka"]),
        utkalabda=num(result["utkalabda"]),
        date=num(f"{day:%d/%m/%Y}"),
        solar_month=name(result["solar_month"]),
        solar_day=num(result["solar_day"]),
        lunar=lunar_text(result),
        bara=name(result["bara"]),
    )


def odia_citation(day: date, result: ConversionResult, style: str) -> str:
    """Odia version of the library's format_historical (same layouts)."""
    bara = name(result["bara"])
    english = f"{name(result['weekday'])}, {long_date(day)}"
    lunar = lunar_text(result)
    solar = t(
        "cite_solar",
        day=num(result["solar_day"]),
        month=name(result["solar_month"]),
    )
    anka = t("cite_anka", anka=num(result["anka"]), gajapati=name(result["gajapati"]))
    utkalabda = t("cite_utkalabda", year=num(result["utkalabda"]))
    shakabda = t("cite_shakabda", year=num(result["shakabda"]))

    if style == "full":
        return (
            f"{english} = {utkalabda}, {anka}\n{bara}, {lunar} | {solar} | {shakabda}"
        )
    if style == "compact":
        return " / ".join([english, utkalabda, anka, f"{bara}, {lunar}", solar])
    odia_date = lunar if style == "lunar" else solar
    return f"{bara}, {odia_date}, {utkalabda} ({anka})\n= {english}"


def citation(day: date, result: ConversionResult, style: str) -> str:
    """Citation text for the chosen style and language."""
    if style == JATAKA_STYLE:
        return jataka_citation(day, result)
    if is_odia():
        return odia_citation(day, result, style)
    return format_historical(day, style=style)  # type: ignore[arg-type]


# ---- Cached calculations --------------------------------------------------


@st.cache_data(show_spinner=False)
def cached_convert(day: date) -> ConversionResult:
    """Full English -> Odia conversion, including Anka."""
    return dict(convert(day))  # type: ignore[return-value]


@st.cache_data(show_spinner=False)
def cached_basic(day: date) -> ConversionResult:
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


def get_details(day: date) -> tuple[ConversionResult, bool]:
    """Return (conversion result, whether Anka data is available)."""
    has_anka = day >= EARLIEST_ANKA_DATE
    result = cached_convert(day) if has_anka else cached_basic(day)
    return result, has_anka


def today_defaults() -> ConversionResult:
    """Today's Odia date, used to seed the Odia -> English form."""
    result, _ = get_details(today_ist())
    return result


# ---- English-tab state ----------------------------------------------------


def set_en_date(day: date) -> None:
    """Write Day / Month / Year selectbox values for `day`."""
    st.session_state[SessionKey.EN_YEAR] = day.year
    st.session_state[SessionKey.EN_MONTH] = day.month
    st.session_state[SessionKey.EN_DAY] = day.day


def set_en_date_today() -> None:
    """Refresh button callback: jump to today."""
    set_en_date(today_ist())


def set_en_date_from_picker() -> None:
    """Calendar-picker callback: copy the picked date into the selectboxes."""
    set_en_date(st.session_state[SessionKey.EN_PICKER])


def current_en_date() -> date:
    """Date currently selected on the English tab."""
    return date(
        st.session_state[SessionKey.EN_YEAR],
        st.session_state[SessionKey.EN_MONTH],
        st.session_state[SessionKey.EN_DAY],
    )


# ---- Odia-tab state -------------------------------------------------------


def od_today_values() -> dict[str, Any]:
    """Today's values used to seed / reset the Odia -> English form."""
    today = today_defaults()
    has_anka = today.get("anka") is not None
    paksha = today["paksha"] if today["paksha"] in PAKSHAS else PAKSHAS[0]
    tithis = tithi_options(paksha)
    return {
        SessionKey.OD_UTKALABDA: min(
            max(today["utkalabda"], MIN_UTKALABDA), MAX_UTKALABDA
        ),
        SessionKey.OD_ANKA: today.get("anka", 2),
        SessionKey.OD_GAJAPATI: (
            today["gajapati"]
            if today.get("gajapati") in REIGN_NAMES
            else REIGN_NAMES[0]
        ),
        SessionKey.OD_RASHI: (
            today["solar_month"] if today["solar_month"] in RASHI else RASHI[0]
        ),
        SessionKey.OD_SOLAR_DAY: today["solar_day"],
        SessionKey.OD_LUNAR_MONTH: (
            today["lunar_month"]
            if today["lunar_month"] in LUNAR_MONTHS
            else LUNAR_MONTHS[0]
        ),
        SessionKey.LUNAR_PAKSHA: paksha,
        SessionKey.LUNAR_TITHI: (
            today["tithi"] if today["tithi"] in tithis else tithis[0]
        ),
        SessionKey.OD_ADHIKA: bool(today["adhika"]),
        SessionKey.OD_YEAR_TYPE: YEAR_ANKA if has_anka else YEAR_UTKALABDA,
        SessionKey.OD_DATE_TYPE: DATE_SOLAR,
    }


def init_od_inputs() -> None:
    """Fill the Odia form with today's values on first load."""
    for input_key, value in od_today_values().items():
        if input_key not in st.session_state:
            st.session_state[input_key] = value


def reset_od_to_today() -> None:
    """Refresh-button callback: reset the Odia form to today."""
    st.session_state.update(od_today_values())
