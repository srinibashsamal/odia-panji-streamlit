# Odia Panji Converter

A simple, mobile-friendly Streamlit application for converting between **Gregorian dates** and the **traditional Odia calendar**. The app is powered by the [`odia-panji`](https://pypi.org/project/odia-panji/) Python library.

<!-- Replace with a real screenshot when one is available. -->
<!-- ![Screenshot](docs/screenshot.png) -->

## Features

### English → Odia

Select a Gregorian date and view:

- Day of the week in English and Odia bara, for example `Sunday (Rabibara)`
- Utkalabda / Utkaliya San
- Anka year
- Reigning Gajapati
- Shakabda
- Purnimanta lunar month, paksha and tithi
- Odia solar month and day
- Sunia and Odia year boundaries
- Citation-style output for historical and archival use
- Optional Odia numerals for Utkalabda, Anka and Shakabda (shared toggle across both tabs)

### Odia → English

Convert an Odia date to its corresponding Gregorian date using either:

- Utkalabda + solar date
- Utkalabda + lunar date
- Anka + solar date
- Anka + lunar date

The interface uses dropdowns for solar months, lunar months, paksha and tithi to reduce spelling and input errors.

### Additional UI features

- Defaults to the current date in Indian Standard Time (IST)
- Responsive Day / Month / Year selector
- Calendar picker next to the Day / Month / Year selector
- Notification when a day is adjusted to fit the month (e.g. 31 → 28 Feb)
- **Today** (refresh) buttons on both tabs; on the Odia → English tab it also resets the year/date type to Utkalabda + Solar
- Shareable URL containing the selected Gregorian date
- Validation for skipped or invalid Anka numbers
- Support for adhika (intercalary) lunar months
- Four citation styles: `full`, `compact`, `lunar` and `solar`, plus a traditional `Jataka` style
- Cached calculations for faster repeat lookups
- Expandable full conversion details

## Example

For `14-10-2026`, the app displays values such as:

```text
Day: Budhabara (Wednesday)
Utkalabda: 1434
Anka: 71
Gajapati: Divyasingha Deva IV
Shakabda: 1948
Lunar date: Aswina Shukla Chaturthi
Solar date: 28 Kanya
```

<!--


Day: Mangalabara (Tuesday)
Lunar date: Kartika Krushna Pratipada
Solar date: 11 Tula (lunar equivalent: Kartika)
Gajapati: Divyasingha Deva IV (acceded 07-07-1970)
Odia year: 23-09-2026 to 11-09-2027 (Sunia: 23-09-2026) -->

A full historical citation can be shown as:

```text
Wednesday, 14 October 2026 = 1434 Utkalabda, Anka 71 of Divyasingha Deva IV
Budhabara, Aswina Shukla Chaturthi | 28 Kanya | Shakabda 1948
```

## Installation

### 1. Download or clone the application

If Git is installed:

```bash
git clone https://github.com/srinibashsamal/odia-panji-streamlit.git
cd odia-panji-streamlit
```

If Git is not installed, download the repository as a ZIP from GitHub, extract it and open PowerShell or Command Prompt inside the extracted folder.

### 2. Install the dependencies

On Windows:

```powershell
py -m pip install -r requirements.txt
```

On macOS or Linux:

```bash
python3 -m pip install -r requirements.txt
```

### 3. Run the application

On Windows:

```powershell
py -m streamlit run app.py
```

On macOS or Linux:

```bash
python3 -m streamlit run app.py
```

Streamlit normally opens the application automatically in the default browser.
If it does not, open the local address displayed in the terminal.

## Requirements

The `requirements.txt` file should contain:

```text
streamlit>=1.53
odia-panji>=0.3.2
```

The minimum `odia-panji` version is `0.3.2` because the app uses weekday and
bara details in conversion results and historical citations.

## Project structure

```text
odia-panji-streamlit/
├── app.py              # Streamlit application
├── app_constants.py    # Dates, labels, citation styles and layout CSS
├── requirements.txt    # Runtime dependencies
├── README.md           # Project documentation
└── LICENSE             # MIT licence
```

## Deploy on Streamlit Community Cloud

1. Create a public GitHub repository for this application.
2. Upload `app.py`, `app_constants.py`, `requirements.txt`, `README.md` and `LICENSE`.
3. Sign in to [Streamlit Community Cloud](https://share.streamlit.io/) with GitHub.
4. Create a new app and select the application repository.
5. Set the main file path to `app.py`.
6. Deploy the app.

When the repository is updated, Streamlit Community Cloud normally rebuilds
the app from the latest committed files. If a newly published `odia-panji`
version is not picked up immediately, reboot the app or clear its cache from
the app-management menu.

## Share a selected date

The English → Odia tab keeps the chosen Gregorian date in the URL as an ISO query parameter:

```text
?date=2026-10-14
```

This allows a visitor to copy the page URL and share a conversion for a specific date.

## Calendar conventions

- Sunia and tithis are calculated for **Puri, Odisha**, in **IST**.
- Odia lunar months use the **Purnimanta** convention.
- A tithi is assigned according to the tithi prevailing at sunrise.
- Anka is a Gajapati regnal count, not a continuous era year.
- The app supports Anka dates from `14-02-1926`, the earliest reign currently recorded in the library.
- The app limits selectable Gregorian dates to `1800-2100`, the trusted range stated by the underlying library.

## Limitations

- This is a date-conversion tool, not a complete Panchanga or Panji.
- Nakshatra, Yoga, Karana, Muhurta and festival rules are not included.
- Printed panjis can differ by a day near astronomical boundaries because of different constants, ayanamsa, sunrise definitions or locations.
- Some reverse conversions can be ambiguous. In those cases, the application shows an error message instead of silently choosing a date.

## Testing

This app has no test suite of its own; the astronomical and calendar
calculations are covered by the [`odia-panji` test suite](https://github.com/srinibashsamal/odia-panji).

## Library

The calculation engine is maintained separately:

- [`odia-panji` on PyPI](https://pypi.org/project/odia-panji/)
- [`odia-panji` source code](https://github.com/srinibashsamal/odia-panji)

## Purpose

The project was inspired by historical records, including Jataka (ଜାତକ) documents, that may record only a traditional Odia year and Anka. Converting such dates into corresponding Gregorian dates can be difficult without the right references.

This application aims to make Odia calendar conversion more accessible to historians, researchers, genealogists and anyone interested in Odisha's history, heritage and traditional calendar system.

## License

[MIT](LICENSE) © Srinibash Samal

## Author

**Srinibash Samal**

- [GitHub profile](https://github.com/srinibashsamal)
- [`odia-panji` project](https://github.com/srinibashsamal/odia-panji)
