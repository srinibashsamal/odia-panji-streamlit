"""Odia text for the Odia Panji Streamlit app.

Must define the same names and TEXT keys as ``app_text_en.py``.
NAMES maps the library's English terms to Odia; anything missing falls
back to the English term, so a new Gajapati or term never breaks the app.
"""

from __future__ import annotations

# Show every number in Odia digits (୧୪୩୪).
USE_ODIA_DIGITS: bool = True

# Rashi / Solar months
RASHI_NAMES: dict[str, str] = {  # (odia_panji.constants.RASHI)
    "Mesha": "ମେଷ",
    "Vrusha": "ବୃଷ",
    "Mithuna": "ମିଥୁନ",
    "Karkata": "କର୍କଟ",
    "Simha": "ସିଂହ",
    "Kanya": "କନ୍ୟା",
    "Tula": "ତୁଳା",
    "Bruschika": "ବିଛା",  # ବୃଶ୍ଚିକ
    "Dhanu": "ଧନୁ",
    "Makara": "ମକର",
    "Kumbha": "କୁମ୍ଭ",
    "Meena": "ମୀନ",
}

# Lunar months
LUNAR_MONTH_NAMES: dict[str, str] = {  # (LUNAR_MONTHS)
    "Chaitra": "ଚୈତ୍ର",
    "Baisakha": "ବୈଶାଖ",
    "Jyestha": "ଜ୍ୟେଷ୍ଠ",
    "Asadha": "ଆଷାଢ଼",
    "Srabana": "ଶ୍ରାବଣ",
    "Bhadraba": "ଭାଦ୍ରବ",
    "Aswina": "ଆଶ୍ୱିନ",
    "Kartika": "କାର୍ତ୍ତିକ",
    "Margasira": "ମାର୍ଗଶିର",
    "Pausa": "ପୌଷ",
    "Magha": "ମାଘ",
    "Phalguna": "ଫାଲ୍ଗୁନ",
}

# Paksha
PAKSHA_NAMES: dict[str, str] = {
    "Shukla": "ଶୁକ୍ଳ",
    "Krushna": "କୃଷ୍ଣ",
}

# Tithis
TITHI_NAMES_ODIA: dict[str, str] = {  # (TITHI_NAMES + Purnima / Amabasya)
    "Pratipada": "ପ୍ରତିପଦା",
    "Dwitiya": "ଦ୍ୱିତୀୟା",
    "Trutiya": "ତୃତୀୟା",
    "Chaturthi": "ଚତୁର୍ଥୀ",
    "Panchami": "ପଞ୍ଚମୀ",
    "Sasthi": "ଷଷ୍ଠୀ",
    "Saptami": "ସପ୍ତମୀ",
    "Astami": "ଅଷ୍ଟମୀ",
    "Nabami": "ନବମୀ",
    "Dasami": "ଦଶମୀ",
    "Ekadasi": "ଏକାଦଶୀ",
    "Dwadasi": "ଦ୍ୱାଦଶୀ",
    "Trayodasi": "ତ୍ରୟୋଦଶୀ",
    "Chaturdasi": "ଚତୁର୍ଦ୍ଦଶୀ",
    "Purnima": "ପୂର୍ଣ୍ଣିମା",
    "Amabasya": "ଅମାବାସ୍ୟା",
}

# Odia Bara
BARA_NAMES: dict[str, str] = {  # (ODIA_WEEKDAYS)
    "Somabara": "ସୋମବାର",
    "Mangalabara": "ମଙ୍ଗଳବାର",
    "Budhabara": "ବୁଧବାର",
    "Gurubara": "ଗୁରୁବାର",
    "Sukrabara": "ଶୁକ୍ରବାର",
    "Sanibara": "ଶନିବାର",
    "Rabibara": "ରବିବାର",
}

# English weekdays -> Odia
WEEKDAY_NAMES: dict[str, str] = {  # (ENGLISH_WEEKDAYS)
    "Monday": "ସୋମବାର",
    "Tuesday": "ମଙ୍ଗଳବାର",
    "Wednesday": "ବୁଧବାର",
    "Thursday": "ଗୁରୁବାର",
    "Friday": "ଶୁକ୍ରବାର",
    "Saturday": "ଶନିବାର",
    "Sunday": "ରବିବାର",
}

# Gajapatis (add entries when the library gains new reigns)
GAJAPATI_NAMES: dict[str, str] = {  # (GAJAPATI_REIGNS)
    "Ramachandra Deba IV": "ଚତୁର୍ଥ ରାମଚନ୍ଦ୍ର ଦେବ",
    "Birakisore Deva III": "ତୃତୀୟ ବୀରକିଶୋର ଦେବ",
    "Divyasingha Deva IV": "ଚତୁର୍ଥ ଦିବ୍ୟସିଂହ ଦେବ",
}

MONTHS: list[str] = [
    "ଜାନୁଆରୀ",
    "ଫେବୃଆରୀ",
    "ମାର୍ଚ୍ଚ",
    "ଏପ୍ରିଲ",
    "ମେ",
    "ଜୁନ",
    "ଜୁଲାଇ",
    "ଅଗଷ୍ଟ",
    "ସେପ୍ଟେମ୍ବର",
    "ଅକ୍ଟୋବର",
    "ନଭେମ୍ବର",
    "ଡିସେମ୍ବର",
]
MONTHS_LONG: list[str] = MONTHS

STYLE_LABELS: dict[str, str] = {
    "full": "ସମ୍ପୂର୍ଣ୍ଣ",
    "compact": "ସଂକ୍ଷିପ୍ତ (ଏକ ଧାଡ଼ି)",
    "lunar": "ଚାନ୍ଦ୍ର ପ୍ରଥମେ",
    "solar": "ସୌର ପ୍ରଥମେ",
    "jataka": "ଜାତକ",
}

GAJAPATI_UPADHI: str = (
    "ଶ୍ରୀ ଶ୍ରୀ ଶ୍ରୀ ବୀରଶ୍ରୀ ଗଜପତି ଗୌଡ଼େଶ୍ୱର "
    "ନବ କୋଟି କର୍ଣ୍ଣାଟୋତ୍କଳ କଳବର୍ଗେଶ୍ୱର ଅଭିରାୟ ଭୂତ ଭୈରବ "
    "ଦୁଃସହ ଦୁଃଶାସନ ଅନିକରଣେ ରାଉତରାୟ ଶାସନୋତ୍ତୀର୍ଣ୍ଣ "
    "ଅତୁଳବଳ ପରାକ୍ରମ ସଂଗ୍ରାମେ ସହସ୍ରବାହୁ କ୍ଷତ୍ରିୟକୁଳ ଧୂମକେତୁ "
    "ଅରି ଦଳଗଞ୍ଜନ ମତ୍ତ ଗଜ ବୀରାଧିବୀରବର "
    "ପ୍ରବଳ ପ୍ରତାପୀ ମହାରାଜାଧିରାଜ"
)

# Page / navigation
PAGE_TEXT: dict[str, str] = {
    "page_title": "ଓଡ଼ିଆ ପାଞ୍ଜି ରୂପାନ୍ତରକ",
    "title": "📅 ଓଡ଼ିଆ ପାଞ୍ଜି ରୂପାନ୍ତରକ",
    "caption": (
        "ଇଂରାଜୀ (ଗ୍ରେଗୋରିଆନ) ତାରିଖ ଓ ଓଡ଼ିଆ ପାଞ୍ଜି ମଧ୍ୟରେ ରୂପାନ୍ତର କରନ୍ତୁ: "
        "ଉତ୍କଳାବ୍ଦ, ଅଙ୍କ, ତିଥି, ସୌର ମାସ, ଶକାବ୍ଦ ଓ ବାର।"
    ),
    "tab_en": "ଇଂରାଜୀ → ଓଡ଼ିଆ",
    "tab_od": "ଓଡ଼ିଆ → ଇଂରାଜୀ",
    "tab_about": "ଏହା ବିଷୟରେ",
}

# English -> Odia tab
EN_TO_ODIA_TEXT: dict[str, str] = {
    "en_date_heading": "**ଇଂରାଜୀ (ଗ୍ରେଗୋରିଆନ) ତାରିଖ**",
    "day": "ଦିନ",
    "month": "ମାସ",
    "year": "ବର୍ଷ",
    "today": "ଆଜି",
    "pick_date": "ତାରିଖ ବାଛନ୍ତୁ",
    "day_adjusted": "ଦିନ {old}ରୁ {new}କୁ ବଦଳାଗଲା ({month}ରେ {days} ଦିନ ଅଛି)।",
    "share_hint": "ତାରିଖ ସହିତ ପେଜ୍ ଲିଙ୍କ ବଦଳେ, ତେଣୁ ଏହାକୁ କପି କରି ସେୟାର କରିପାରିବେ।",
    "calculating": "ଗଣନା ଚାଲିଛି...",
}

# Odia -> English tab
ODIA_TO_EN_TEXT: dict[str, str] = {
    "year_given_as": "ବର୍ଷର ପ୍ରକାର",
    "date_given_as": "ତାରିଖର ପ୍ରକାର",
    "Utkalabda": "ଉତ୍କଳାବ୍ଦ",
    "Anka": "ଅଙ୍କ",
    "Solar": "ସୌର",
    "Lunar": "ଚାନ୍ଦ୍ର",
    "utkalabda_year": "ଉତ୍କଳାବ୍ଦ ବର୍ଷ",
    "anka": "ଅଙ୍କ",
    "gajapati": "ଗଜପତି",
    "invalid_anka": (
        "{anka} ଏକ ବୈଧ ଅଙ୍କ ନୁହେଁ। ଅଙ୍କ ଗଣନାରେ '୧' ଏବଂ '୬' କିମ୍ବା '୦'ରେ ଶେଷ "
        "ହେଉଥିବା ସଂଖ୍ୟା ('୧୦' ବ୍ୟତୀତ) ବାଦ ଦିଆଯାଏ।"
    ),
    "solar_month": "ସୌର ମାସ (ରାଶି)",
    "lunar_month": "ଚାନ୍ଦ୍ର ମାସ",
    "paksha": "ପକ୍ଷ",
    "tithi": "ତିଥି",
    "adhika_label": "ଅଧିକ (ମଳ) ମାସ",
    "adhika_help": "ପ୍ରଥମ ଥର ଆଜିର ତଥ୍ୟରୁ ସେଟ୍ ହୁଏ; ତା'ପରେ ଆପଣଙ୍କ ପସନ୍ଦ ରହେ।",
    "searching": "ଖୋଜା ଚାଲିଛି...",
    "result_date": "**{weekday}, {day} {month} {year}**",
}

# Panchanga / result details
DETAIL_TEXT: dict[str, str] = {
    "m_utkalabda": "ଉତ୍କଳାବ୍ଦ",
    "m_anka": "ଅଙ୍କ",
    "m_gajapati": "ଗଜପତି",
    "m_shakabda": "ଶକାବ୍ଦ",
    "adhika_prefix": "ଅଧିକ ",
    "day_line": "**ବାର:** {bara}",
    "lunar_line": "**ଚାନ୍ଦ୍ର ତିଥି:** {lunar}",
    "solar_line": "**ସୌର ତାରିଖ:** {month} {day} (ଚାନ୍ଦ୍ର ମାସ ଅନୁସାରେ: {equivalent})",
    "gajapati_line": "**ଗଜପତି:** {gajapati} ({accession}ରେ ସିଂହାସନାରୋହଣ)",
    "year_line": "**ଓଡ଼ିଆ ବର୍ଷ:** {start}ରୁ {end} (ସୁନିଆ: {sunia})",
    "accession_day": "ଏହା ଗଜପତିଙ୍କ ସିଂହାସନାରୋହଣ ଦିବସ; ଏହି ଦିନଟି ନୂତନ ମହାରାଜାଙ୍କ ଅଙ୍କରେ ଗଣାଯାଏ।",
    "citation_style": "ଉଲ୍ଲେଖ ଶୈଳୀ",
    "no_anka": "ଅଙ୍କ ବର୍ଷ {date}ରୁ ଉପଲବ୍ଧ (ଲାଇବ୍ରେରୀର ପ୍ରଥମ ଗଜପତି)।",
    "all_details": "ସମସ୍ତ ବିବରଣୀ",
    "error": "ତାରିଖ ରୂପାନ୍ତର ହୋଇପାରିଲା ନାହିଁ। ({error})",
}

# Citation formats
CITATION_TEXT: dict[str, str] = {  # mirror the library's format_historical layouts
    "jataka": (
        "{titles} ଶ୍ରୀ ଶ୍ରୀ ୧୦୮ ଶ୍ରୀ {gajapati} "
        "ମହାରାଜାଙ୍କ ବିଜୟେ ଶୁଭ ରାଜ୍ୟ ବର୍ଦ୍ଧନେ "
        "ଅ{anka}ଙ୍କ ସନ {utkalabda} ସାଲ "
        "ଇଂରାଜୀ ତା- {date} ରିଖ "
        "ସୌରମାନ {solar_month} ମାସ "
        "ଦି{solar_day}ନ "
        "ଚାନ୍ଦ୍ରିୟମାନ {lunar} {bara}"
    ),
    "cite_english": "{day} {month} {year}",
    "cite_utkalabda": "{year} ଉତ୍କଳାବ୍ଦ",
    "cite_anka": "{gajapati}ଙ୍କ {anka} ଅଙ୍କ",
    "cite_shakabda": "ଶକାବ୍ଦ {year}",
    "cite_solar": "{month} {day}",
}

# Combined lookup for backward compatibility
NAMES: dict[str, str] = {
    **RASHI_NAMES,
    **LUNAR_MONTH_NAMES,
    **PAKSHA_NAMES,
    **TITHI_NAMES_ODIA,
    **BARA_NAMES,
    **WEEKDAY_NAMES,
    **GAJAPATI_NAMES,
}

TEXT: dict[str, str] = {
    **PAGE_TEXT,
    **EN_TO_ODIA_TEXT,
    **ODIA_TO_EN_TEXT,
    **DETAIL_TEXT,
    **CITATION_TEXT,
}

ABOUT: str = """
[**odia-panji**](https://pypi.org/project/odia-panji/) v{version} ଉପରେ ଆଧାରିତ,
ଶ୍ରୀନିବାସ ସାମଲଙ୍କ ଦ୍ୱାରା ନିର୍ମିତ ([GitHub](https://github.com/srinibashsamal/odia-panji))।

- ସୁନିଆ, ତିଥି ଓ ସଂକ୍ରାନ୍ତି ସୂର୍ଯ୍ୟ ଓ ଚନ୍ଦ୍ରର ଗତିରୁ ଗଣନା କରାଯାଏ, ପୁରୀରୁ
  ଦେଖାଯିବା ଅନୁସାରେ ଓ ଭାରତୀୟ ମାନକ ସମୟ (IST)ରେ।
- ଚାନ୍ଦ୍ର ମାସ ପୂର୍ଣ୍ଣିମାନ୍ତ; ଯେଉଁ ଦିନର ସୂର୍ଯ୍ୟୋଦୟ ସମୟରେ ତିଥି ଚାଲିଥାଏ, ସେହି
  ଦିନ ସେହି ତିଥିର।
- ଫଳାଫଳ ପ୍ରାୟ **{min_year}-{max_year}** ପର୍ଯ୍ୟନ୍ତ ବିଶ୍ୱସନୀୟ, ତେଣୁ ଏହି ଆପ୍
  ସେହି ସୀମା ମଧ୍ୟରେ ସୀମିତ।
- ଅଙ୍କ ବର୍ଷ ଗଣନା {earliest}ରୁ ଉପଲବ୍ଧ।
- ସୀମା ନିକଟରେ ଛପା ପାଞ୍ଜି ସହିତ ଗୋଟିଏ ଦିନର ପାର୍ଥକ୍ୟ ହୋଇପାରେ।
"""

INSPIRATION_TITLE: str = "💡 ପ୍ରେରଣା"
INSPIRATION: str = """
ଏହି ପ୍ରକଳ୍ପର ପ୍ରେରଣା ଆସିଥିଲା ଯେତେବେଳେ ମୁଁ ଏକ ଜାତକ ଦେଖିଲି, ଯେଉଁଥିରେ କେବଳ
ପାରମ୍ପରିକ ଓଡ଼ିଆ ବର୍ଷ ଓ ଅଙ୍କ ଲେଖାଥିଲା। ଏହି ତାରିଖଗୁଡ଼ିକୁ ଇଂରାଜୀ ତାରିଖ ଓ ବର୍ଷରେ
ରୂପାନ୍ତର କରିବାକୁ ଚେଷ୍ଟା କରିବା ବେଳେ ମୁଁ ଅନେକ ଅସୁବିଧାର ସମ୍ମୁଖୀନ ହେଲି।

ସେହି ଅନୁଭୂତି ମୋତେ ଭାବିବାକୁ ବାଧ୍ୟ କଲା: *ଏହି ରୂପାନ୍ତରକୁ ସହଜ ଓ ସୁଲଭ କରିବା ପାଇଁ
ଏକ ସରଳ ଉପକରଣ କାହିଁକି ତିଆରି ନ କରିବା?*

ସେହି ଚିନ୍ତାରୁ ଓଡ଼ିଆ ପାଞ୍ଜି ରୂପାନ୍ତର ପାଇଁ Python ଲାଇବ୍ରେରୀ **odia-panji** ଏବଂ
ତା' ଉପରେ ଆଧାରିତ ଏହି Streamlit ୱେବ୍ ଆପ୍ଲିକେସନର ସୃଷ୍ଟି ହେଲା।
"""

PURPOSE_TITLE: str = "🎯 ଉଦ୍ଦେଶ୍ୟ"
PURPOSE: str = """
ଓଡ଼ିଆ ପାଞ୍ଜି ତାରିଖ ରୂପାନ୍ତରକୁ ସମସ୍ତଙ୍କ ପାଇଁ ସହଜ ଓ ଝଞ୍ଝଟମୁକ୍ତ କରିବା ହିଁ ଏହାର
ଲକ୍ଷ୍ୟ। ମୁଁ ଆଶା କରେ ଏହି ଉପକରଣ ଐତିହାସିକ, ଗବେଷକ, ବଂଶାବଳୀ ଅନୁସନ୍ଧାନକାରୀ ଏବଂ
ଓଡ଼ିଶାର ଇତିହାସ, ଐତିହ୍ୟ ଓ ପାରମ୍ପରିକ ପାଞ୍ଜି ବିଷୟରେ ଜାଣିବାକୁ ଆଗ୍ରହୀ ସମସ୍ତଙ୍କ ପାଇଁ
ଉପଯୋଗୀ ହେବ।

ପାରମ୍ପରିକ ଓଡ଼ିଆ ତାରିଖକୁ ଇଂରାଜୀ ତାରିଖ ସହିତ ଯୋଡ଼ି, ମୁଁ ଐତିହାସିକ ଦଲିଲଗୁଡ଼ିକୁ ବୁଝିବା
ସହଜ କରିବାକୁ ଏବଂ ଲୋକମାନଙ୍କୁ ଓଡ଼ିଶାର ସମୃଦ୍ଧ ସାଂସ୍କୃତିକ ଅତୀତ ସହିତ ଯୋଡ଼ିବାକୁ ଚାହେଁ।
"""
