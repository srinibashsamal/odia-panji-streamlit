"""Odia Panji converter: a Streamlit app for the odia-panji library.

This file draws the page; the logic lives in ``app_core.py``.

Run locally:
    py -m pip install -r requirements.txt
    py -m streamlit run app.py
"""

from __future__ import annotations

import calendar
import json
from datetime import date

import streamlit as st
from odia_panji import OdiaCalendarError, __version__, is_valid_anka
from odia_panji.constants import ENGLISH_WEEKDAYS, LUNAR_MONTHS, RASHI

from app_constants import (
    DATE_SOLAR,
    DATE_TYPES,
    EARLIEST_ANKA_DATE,
    EN_DATE_COLS,
    JATAKA_STYLE,
    LANGUAGE_TOGGLE_LABEL,
    LAYOUT_CSS,
    MAX_DATE,
    MAX_UTKALABDA,
    METRICS_COLS,
    MIN_DATE,
    MIN_UTKALABDA,
    OD_HEAD_COLS,
    PAKSHAS,
    REIGN_NAMES,
    STYLES,
    YEAR_TYPES,
    YEAR_UTKALABDA,
    YEARS,
    SessionKey,
)
from app_core import (
    ConversionResult,
    assert_text_keys_match,
    cached_to_english,
    citation,
    current_en_date,
    current_texts,
    get_details,
    init_od_inputs,
    language_radio,
    long_month,
    lunar_text,
    month_label,
    name,
    num,
    parse_date_param,
    required,
    reset_od_to_today,
    restore_selectbox_values,
    set_en_date,
    set_en_date_from_picker,
    set_en_date_today,
    style_label,
    t,
    tithi_options,
    today_ist,
)

# ---- Details view ---------------------------------------------------------


def render_metrics(result: ConversionResult, has_anka: bool, key: str) -> None:
    """Four metric cards: Utkalabda, Anka, Gajapati, Shakabda."""
    with st.container(key=f"{SessionKey.METRICS_PREFIX}{key}"):
        col_utkalabda, col_anka, col_gajapati, col_shakabda = st.columns(
            METRICS_COLS, gap="small"
        )
        col_utkalabda.metric(t("m_utkalabda"), num(result["utkalabda"]))
        if has_anka:
            col_anka.metric(t("m_anka"), num(result["anka"]))
            col_gajapati.metric(t("m_gajapati"), name(result["gajapati"]))
        else:
            col_anka.metric(t("m_anka"), "—")
            col_gajapati.metric(t("m_gajapati"), "—")
        col_shakabda.metric(t("m_shakabda"), num(result["shakabda"]))


def render_detail_lines(result: ConversionResult, has_anka: bool) -> None:
    """Day, lunar, solar, and (when available) Gajapati / year lines."""
    st.markdown(t("day_line", bara=name(result["bara"]), weekday=result["weekday"]))
    st.markdown(t("lunar_line", lunar=lunar_text(result)))
    st.markdown(
        t(
            "solar_line",
            day=num(result["solar_day"]),
            month=name(result["solar_month"]),
            equivalent=name(result["solar_month_lunar_equivalent"]),
        )
    )

    if not has_anka:
        return

    st.markdown(
        t(
            "gajapati_line",
            gajapati=name(result["gajapati"]),
            accession=num(result["gajapati_accession"]),
        )
    )
    st.markdown(
        t(
            "year_line",
            start=num(result["odia_year_start"]),
            end=num(result["odia_year_end"]),
            sunia=num(result["sunia_of_year"]),
        )
    )
    if result.get("is_accession_day"):
        st.info(t("accession_day"))


def render_citation_block(day: date, result: ConversionResult, key: str) -> None:
    """Citation-style radio + formatted citation text."""
    style = language_radio(
        t("citation_style"),
        [*STYLES, JATAKA_STYLE],
        f"{SessionKey.STYLE_PREFIX}{key}",
        format_func=style_label,
        horizontal=True,
    )
    st.code(citation(day, result, style), language=None, wrap_lines=True)


def render_details(
    day: date, result: ConversionResult, has_anka: bool, key: str
) -> None:
    """Full details panel: metrics, lines, citation (or no-Anka notice)."""
    render_metrics(result, has_anka, key)
    render_detail_lines(result, has_anka)

    if has_anka:
        render_citation_block(day, result, key)
    else:
        st.info(t("no_anka", date=num(f"{EARLIEST_ANKA_DATE:%d-%m-%Y}")))

    # Raw library output always shown as-is (English names / digits).
    with st.expander(t("all_details")):
        st.code(
            json.dumps(result, indent=4, ensure_ascii=False, default=str),
            language="json",
        )


def show_odia_details(day: date, key: str) -> None:
    """Fetch and display the Odia details for a Gregorian date."""
    result, has_anka = get_details(day)
    render_details(day, result, has_anka, key)


# ---- Page setup -----------------------------------------------------------

assert_text_keys_match()

st.set_page_config(page_title=t("page_title"), page_icon="📅", layout="centered")
st.markdown(LAYOUT_CSS, unsafe_allow_html=True)

st.title(t("title"))
st.caption(t("caption"))

st.toggle(LANGUAGE_TOGGLE_LABEL, key=SessionKey.ODIA_MODE)
restore_selectbox_values()

english_tab, odia_tab, about_tab = st.tabs([t("tab_en"), t("tab_od"), t("tab_about")])

# ---- English -> Odia -------------------------------------------------------

with english_tab:
    # First load: use the date from the URL, or today.
    if SessionKey.EN_YEAR not in st.session_state:
        initial = parse_date_param(st.query_params.get("date")) or today_ist()
        set_en_date(initial)

    st.markdown(t("en_date_heading"))

    with st.container(key=SessionKey.EN_DATE_ROW):
        col_day, col_month, col_year, col_today, col_pick = st.columns(
            EN_DATE_COLS, vertical_alignment="bottom"
        )

        # Clamp day when the month is shorter (e.g. 31 Jan -> Feb).
        days_in_month: int = calendar.monthrange(
            st.session_state[SessionKey.EN_YEAR],
            st.session_state[SessionKey.EN_MONTH],
        )[1]
        if st.session_state[SessionKey.EN_DAY] > days_in_month:
            st.session_state[SessionKey.CLAMPED_FROM] = st.session_state[
                SessionKey.EN_DAY
            ]
            st.session_state[SessionKey.EN_DAY] = days_in_month

        # Keep the calendar picker in sync with the selectboxes.
        st.session_state[SessionKey.EN_PICKER] = current_en_date()

        col_day.selectbox(
            t("day"),
            list(range(1, days_in_month + 1)),
            format_func=num,
            key=SessionKey.EN_DAY,
        )
        col_month.selectbox(
            t("month"),
            list(range(1, 13)),
            format_func=month_label,
            key=SessionKey.EN_MONTH,
        )
        col_year.selectbox(t("year"), YEARS, format_func=num, key=SessionKey.EN_YEAR)
        col_today.button(
            ":material/refresh:",
            on_click=set_en_date_today,
            key=SessionKey.BTN_TODAY,
            help=t("today"),
            width="stretch",
        )
        col_pick.date_input(
            t("pick_date"),
            min_value=MIN_DATE,
            max_value=MAX_DATE,
            format="DD/MM/YYYY",
            key=SessionKey.EN_PICKER,
            on_change=set_en_date_from_picker,
            label_visibility="collapsed",
            help=t("pick_date"),
        )

    if SessionKey.CLAMPED_FROM in st.session_state:
        clamped_from = st.session_state.pop(SessionKey.CLAMPED_FROM)
        st.toast(
            t(
                "day_adjusted",
                old=num(clamped_from),
                new=num(st.session_state[SessionKey.EN_DAY]),
                month=month_label(st.session_state[SessionKey.EN_MONTH]),
                days=num(days_in_month),
            )
        )

    picked: date = current_en_date()

    # Update the URL only when the date changes (avoids extra reruns).
    if st.query_params.get("date") != picked.isoformat():
        st.query_params["date"] = picked.isoformat()
    st.caption(t("share_hint"))

    try:
        with st.spinner(t("calculating")):
            show_odia_details(picked, key="en")
    except OdiaCalendarError as exc:
        st.error(t("error", error=exc))

# ---- Odia -> English -------------------------------------------------------

with odia_tab:
    init_od_inputs()

    with st.container(key=SessionKey.OD_HEAD_ROW):
        col_year_type, col_date_type, col_od_today = st.columns(
            OD_HEAD_COLS, vertical_alignment="bottom"
        )
        with col_year_type:
            year_type = language_radio(
                t("year_given_as"),
                YEAR_TYPES,
                SessionKey.OD_YEAR_TYPE,
                format_func=t,
                horizontal=True,
            )
        with col_date_type:
            date_type = language_radio(
                t("date_given_as"),
                DATE_TYPES,
                SessionKey.OD_DATE_TYPE,
                format_func=t,
                horizontal=True,
            )
        col_od_today.button(
            ":material/refresh:",
            on_click=reset_od_to_today,
            key=SessionKey.BTN_OD_TODAY,
            help=t("today"),
            width="stretch",
        )

    utkalabda: int | None = None
    anka: int | None = None
    gajapati: str | None = None
    ready: bool = True

    if year_type == YEAR_UTKALABDA:
        utkalabda = int(
            st.number_input(
                t("utkalabda_year"),
                min_value=MIN_UTKALABDA,
                max_value=MAX_UTKALABDA,
                step=1,
                key=SessionKey.OD_UTKALABDA,
            )
        )
    else:
        col_anka, col_king = st.columns([1, 2])
        anka = int(
            col_anka.number_input(
                t("anka"), min_value=2, step=1, key=SessionKey.OD_ANKA
            )
        )
        gajapati = col_king.selectbox(
            t("gajapati"),
            REIGN_NAMES,
            format_func=name,
            key=SessionKey.OD_GAJAPATI,
        )
        if not is_valid_anka(anka):
            ready = False
            st.warning(t("invalid_anka", anka=num(anka)))

    month: str
    solar_day: int | None = None
    paksha: str | None = None
    tithi: str | None = None
    adhika: bool = False

    if date_type == DATE_SOLAR:
        col_rashi, col_solar_day = st.columns([2, 1])
        month = required(
            col_rashi.selectbox(
                t("solar_month"),
                RASHI,
                format_func=name,
                key=SessionKey.OD_RASHI,
            )
        )
        # Max 32 is intentional: Odia solar months can have up to 32 days.
        solar_day = int(
            col_solar_day.number_input(
                t("day"),
                min_value=1,
                max_value=32,
                step=1,
                key=SessionKey.OD_SOLAR_DAY,
            )
        )
    else:
        month = required(
            st.selectbox(
                t("lunar_month"),
                LUNAR_MONTHS,
                format_func=name,
                key=SessionKey.OD_LUNAR_MONTH,
            )
        )
        col_paksha, col_tithi = st.columns(2)
        paksha = required(
            col_paksha.selectbox(
                t("paksha"),
                PAKSHAS,
                format_func=name,
                key=SessionKey.LUNAR_PAKSHA,
            )
        )

        # When paksha changes, swap Purnima ↔ Amabasya instead of resetting.
        options: list[str] = tithi_options(paksha)
        current: str | None = st.session_state.get(SessionKey.LUNAR_TITHI)
        if current not in options:
            st.session_state[SessionKey.LUNAR_TITHI] = options[-1]
        tithi = required(
            col_tithi.selectbox(
                t("tithi"),
                options,
                format_func=name,
                key=SessionKey.LUNAR_TITHI,
            )
        )
        adhika = st.checkbox(
            t("adhika_label"),
            help=t("adhika_help"),
            key=SessionKey.OD_ADHIKA,
        )

    st.divider()

    if ready:
        try:
            with st.spinner(t("searching")):
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
            st.success(
                t(
                    "result_date",
                    weekday=name(ENGLISH_WEEKDAYS[result_date.weekday()]),
                    day=num(result_date.day),
                    month=long_month(result_date.month),
                    year=num(result_date.year),
                )
            )
            show_odia_details(result_date, key="od")
        except OdiaCalendarError as exc:
            st.error(t("error", error=exc))

# ---- About ----------------------------------------------------------------

with about_tab:
    texts = current_texts()
    st.markdown(
        texts.ABOUT.format(
            version=num(__version__),
            min_year=num(MIN_DATE.year),
            max_year=num(MAX_DATE.year),
            earliest=num(f"{EARLIEST_ANKA_DATE:%d-%m-%Y}"),
        )
    )
    with st.expander(texts.INSPIRATION_TITLE):
        st.markdown(texts.INSPIRATION)
    with st.expander(texts.PURPOSE_TITLE):
        st.markdown(texts.PURPOSE)
