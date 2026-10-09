# AI Football Prediction Analysis

**An AI-integrated football prediction, match analysis, and betting research tool built with Python.**

This project collects football match information from an external prediction platform, processes published probability ratings, analyzes home and away teams, generates rule-based winner selections, and compares those selections against reference winner labels stored in CSV datasets.

It supports the collection of both scheduled and live football matches, the extraction of prediction-related information, and the organization of match data for further analysis and historical evaluation.

The project combines web scraping, probability-based comparison, football data processing, and automated CSV management into a reusable Python workflow.

---

## Overview

Football prediction platforms can use trained machine-learning models, statistical models, historical performance, and other analytical methods to estimate match outcomes.

This project interacts with an external football prediction platform, Soccer-Rating, to collect match information and published probability ratings. Python scripts then process the collected information to identify potential winners according to explicitly defined comparison rules.

The system is designed to support three main activities:

1. **Football data collection:** Collect information about scheduled and live matches, including team names and available odds or ratings.
2. **Prediction analysis:** Retrieve published probability values and compare the ratings associated with home and away teams.
3. **Prediction evaluation:** Store selected winners and compare them with reference winner labels to investigate prediction agreement.

The project uses Python, Requests, Beautiful Soup, Pandas, and supporting helper functions to automate these operations.

### AI integration

The AI-related component comes from working with prediction information supplied by an external platform that may use its own trained model or analytical system.

The Python scripts perform additional rule-based analysis on the collected information. They do not, in the implementation shown here, independently train a machine-learning model.

The project therefore focuses on **integrating external football prediction information with automated Python analysis**, rather than building a new AI model from scratch.

---

## Key Features

* **External prediction integration:** Works with published football prediction and probability information from Soccer-Rating.
* **Scheduled match collection:** Retrieves match information for a selected date.
* **Live match collection:** Extracts match information from the platform's live-tips page.
* **Probability extraction:** Parses published 1X2 probability values from the platform's calculator pages.
* **Home and away analysis:** Compares probability values associated with home and away team calculations.
* **Rule-based winner selection:** Selects a potential winner when the defined home-versus-away comparison conditions are satisfied.
* **Prediction agreement tracking:** Records whether the selected winner matches the reference winner label.
* **CSV data management:** Stores match information and analysis results in structured CSV files.
* **Team-name matching:** Uses Python's `difflib` to compare team names against a reference list of European teams.
* **Duplicate removal:** Uses helper functions to remove duplicate records.
* **Similar-match filtering:** Supports removal of records that appear to represent similar matches.
* **Automated data processing:** Reduces the need to manually copy match information into spreadsheets.
* **Reusable helper functions:** Separates common CSV and data-cleaning operations into `func.py`.

---

## Project Architecture

The project is organized around three main scripts and a shared helper module.

```text
Football Prediction Platform
             |
             v
     Match Data Collection
             |
       +-----+------+
       |            |
       v            v
 Scheduled Games  Live Games
       |            |
       v            v
DAY_MATCH_FILE  LIVE_MATCH_FILE
       |            |
       +------+-----+
              |
              v
      Prediction Analysis
              |
              v
   External Probability Retrieval
              |
              v
    Home vs Away Comparison
              |
              v
       Winner Selection
              |
              v
   Reference Winner Comparison
              |
              v
   CALCULATED_MATCH_FILE.csv
```

`func.py` provides shared functionality for saving, sorting, filtering, and cleaning datasets.

The exact behavior depends on the website's current HTML structure and the data available when the scripts execute.

---

## Repository Structure

A suggested organization for the project is:

```text
AI-Football-Prediction-Analysis/
│
├── CHECKING_WINNER.py
├── GET_DAY_GAME.py
├── GET_LIVE_GAMES.py
├── func.py
│
├── EUROPEAN_TEAMS.csv
├── DAY_MATCH_FILE.csv
├── LIVE_MATCH_FILE.csv
├── CALCULATED_MATCH_FILE.csv
│
├── requirements.txt
├── README.md
│
└── Additional files/
    └── Other project data and outputs
```

The CSV files may be generated or updated by the scripts. `CALCULATED_MATCH_FILE.csv` is the output file used by the winner-analysis script.

The actual repository may contain additional datasets and helper functions not shown in the provided code.

---

## Technologies Used

| Technology     | Purpose                                                   |
| -------------- | --------------------------------------------------------- |
| Python         | Main programming language                                 |
| Requests       | Sends HTTP requests to retrieve website content           |
| Beautiful Soup | Parses HTML and extracts relevant information             |
| Pandas         | Processes match data and manages CSV files                |
| difflib        | Matches team names approximately against a reference list |
| os             | Manages file paths and file operations                    |

Other standard Python modules may be used elsewhere in the complete project.

---

## Main Python Scripts

### 1. `GET_DAY_GAME.py`

This script collects information about scheduled football matches for a selected date.

It constructs a date-specific URL for the external prediction website, retrieves the page, extracts links, and visits relevant match pages to collect available information.

The script attempts to extract:

* Match date
* League or competition
* Home team
* Away team
* Opening odds or rating
* Available odds or rating
* A reference winner label derived from the opening rating

After collecting match records, it saves the information to `DAY_MATCH_FILE.csv`.

It then uses helper functions to remove similar match records and duplicates.

**Main function:** `get_day_games()`

**Output:** `DAY_MATCH_FILE.csv`

The function accepts a date offset. A value of `0` represents the current date, a positive value represents a future date, and a negative value represents a past date.

### 2. `GET_LIVE_GAMES.py`

This script collects match information from the platform's live-tips page.

It parses the page's table rows and attempts to identify the relevant fields for each match. Depending on the structure of a row, it extracts:

* Home team
* Away team
* Opening odds or rating
* Available odds or rating
* A reference winner label based on the opening rating

The extracted records are stored in `LIVE_MATCH_FILE.csv`.

The script subsequently applies similar-match filtering and duplicate removal.

**Main function:** `get_live_game()`

**Output:** `LIVE_MATCH_FILE.csv`

The script relies on the current structure of the website's HTML. If the platform changes its page layout or formatting, the extraction logic may require updates.

### 3. `CHECKING_WINNER.py`

This script performs additional analysis on the collected match records.

It reads the selected match dataset, retrieves probability information from external calculator pages, compares the available home and away probability values, selects a potential winner where the conditions are satisfied, and records the comparison result.

Its main operations include:

1. Loading the reference team list from `EUROPEAN_TEAMS.csv`.
2. Loading match records from `LIVE_MATCH_FILE.csv` or `DAY_MATCH_FILE.csv`.
3. Comparing team names against the reference list.
4. Constructing calculator URLs for home and away teams.
5. Retrieving probability values from the calculator pages.
6. Comparing the home and away probability values.
7. Assigning a selected winner or `NONE`.
8. Comparing the selected winner against the reference winner label.
9. Saving the analysis to `CALCULATED_MATCH_FILE.csv`.
10. Sorting the output by the `WIN REP` field when possible.

**Main function:** `search_calculate()`

**Output:** `CALCULATED_MATCH_FILE.csv`

The current script sets `user_input = 'live'`, so it selects the live-match dataset. The alternative day-match branch can be enabled by changing the selection logic.

### 4. `func.py`

This module contains helper functions imported by the other scripts.

The provided code uses the following helpers:

| Function           | Purpose                                                                         |
| ------------------ | ------------------------------------------------------------------------------- |
| `saving_files()`   | Saves new data to CSV and appends records when the destination file can be read |
| `sorting_values()` | Sorts records by a specified column and saves the result                        |
| `main_date()`      | Calculates a date from a specified offset                                       |
| `drop_similar()`   | Removes or filters similar match records according to the implementation        |
| `drop_duplicate()` | Removes duplicate records from a dataset                                        |

The exact behavior of `drop_similar()` and other helpers depends on their implementations in `func.py`.

Centralizing these operations avoids duplicating the same data-management logic across multiple scripts.

---

## How Winner Analysis Works

The winner-analysis process uses probability information collected from external calculator pages.

For each match, the script attempts to obtain four probability values:

| Field          | Meaning                                                                   |
| -------------- | ------------------------------------------------------------------------- |
| `HOME H PROBA` | Probability value retrieved for the home team's home-oriented calculation |
| `HOME A PROBA` | Probability value retrieved for the home team's away-oriented calculation |
| `AWAY H PROBA` | Probability value retrieved for the away team's home-oriented calculation |
| `AWAY A PROBA` | Probability value retrieved for the away team's away-oriented calculation |

These values are then compared according to the rules implemented in `CHECKING_WINNER.py`.

### Home-team selection

The script selects the home team when both of the following conditions are satisfied:

* The home team's home-oriented probability exceeds the away team's home-oriented probability.
* The home team's away-oriented probability exceeds the away team's away-oriented probability.

### Away-team selection

The script selects the away team when both of the following conditions are satisfied:

* The away team's home-oriented probability exceeds the home team's home-oriented probability.
* The away team's away-oriented probability exceeds the home team's away-oriented probability.

If neither condition is satisfied, the script records `NONE`.

This is a custom comparison rule. It is not, by itself, a trained machine-learning classifier or proof that the selected team will win.

---

## Understanding the Evaluation Output

The winner-analysis script stores a `WIN REP` value alongside the selected winner.

The intended interpretation is:

| Value | Intended meaning                                                   |
| ----- | ------------------------------------------------------------------ |
| `1`   | The selected winner agrees with the reference winner label         |
| `0`   | The selected winner does not agree with the reference winner label |

The script then attempts to sort the calculated output so that records with a higher `WIN REP` value appear first.

### Important evaluation limitation

The current implementation compares `MY WINNER` against `SOCCERVISTA WINNER`, which is populated from the existing CSV data. The shown code does not independently retrieve the final official match result.

Consequently, `WIN REP` should be interpreted as agreement with the reference winner label, not necessarily a verified match win or a measure of betting profitability.

To calculate actual predictive accuracy, the project should compare each selected winner with independently verified final match results. To assess betting performance, it should also account for odds, stake sizes, bookmaker margins, and any applicable settlement rules.

---

## CSV Files and Their Roles

### `EUROPEAN_TEAMS.csv`

Contains a `COUNTRY` column used by the winner-analysis script as a reference list for approximate team-name matching.

The current matching logic removes spaces from the entries before using `difflib.get_close_matches()`.

Despite the variable name used in the script, the file must contain values that are suitable for matching against the team names in the match datasets.

### `DAY_MATCH_FILE.csv`

Stores scheduled match records collected by `GET_DAY_GAME.py`.

Expected columns include:

* `DATE`
* `LEAGUE`
* `HOME TEAM`
* `AWAY TEAM`
* `OPEN ODD`
* `AVAL ODD`
* `WINNER`

### `LIVE_MATCH_FILE.csv`

Stores live-match records collected by `GET_LIVE_GAMES.py`.

Expected columns include:

* `HOME TEAM`
* `AWAY TEAM`
* `OPEN ODD`
* `AVAL ODD`
* `WINNER`

### `CALCULATED_MATCH_FILE.csv`

Stores the results produced by `CHECKING_WINNER.py`.

Its fields include match information, probability values, the selected winner, the reference winner label, and the `WIN REP` comparison value.

---

## Installation

### Requirements

Install a compatible Python version and the third-party packages required by the project.

Create a `requirements.txt` file containing:

```text
beautifulsoup4
pandas
requests
```

Install the packages:

```bash
python -m pip install -r requirements.txt
```

The `os` and `difflib` modules are included in Python's standard library.

### Clone the repository

```bash
git clone https://github.com/Ezee-Kits/AI-Football-Prediction-Analysis.git
```

### Navigate to the project folder

```bash
cd AI-Football-Prediction-Analysis
```

Make sure the required CSV files exist in the expected locations before running the analysis script.

---

## Running the Scripts

Run the scripts from the project directory so that local imports and expected file paths resolve correctly.

### Collect scheduled matches

```bash
python GET_DAY_GAME.py
```

The script calls `get_day_games()` when the file is executed. By default, the function targets the current date and writes records to `DAY_MATCH_FILE.csv`.

### Collect live matches

```bash
python GET_LIVE_GAMES.py
```

The script calls `get_live_game()` when executed and writes the collected records to `LIVE_MATCH_FILE.csv`.

### Analyze potential winners

```bash
python CHECKING_WINNER.py
```

The current implementation calls `search_calculate()` automatically. It uses the live-match dataset by default and attempts to create `CALCULATED_MATCH_FILE.csv`.

**Execution order:** Collect the relevant match data first, ensure the CSV files contain the expected columns, and then run the winner-analysis script.

The collection scripts depend on the availability and current structure of the external website.

---

## Data Collection and Reliability

The project relies on third-party web pages rather than a documented API in the code shown here.

This means the results may be affected by:

* Changes to website HTML elements or table structures
* Network failures or request timeouts
* Missing or incomplete probability values
* Team-name spelling differences
* Inconsistent odds formats
* Empty match datasets
* Website access restrictions or changes to its terms
* Differences between published predictions and final match outcomes

A more robust implementation can include request timeouts, HTTP status checks, retries with appropriate delays, validation of extracted values, and logging of failed records.

Users should also check the external website's terms and applicable rules before automating access to its content.

---

## Recommended Improvements

Potential development areas include:

* Replace brittle HTML parsing with selectors validated against the current website structure.
* Add request timeouts and explicit HTTP error handling.
* Validate the expected number and format of probability values before comparing them.
* Correct team-name matching so that home and away teams are checked independently.
* Normalize team names before matching.
* Add a configurable choice between live and scheduled match datasets.
* Separate data collection, probability analysis, and evaluation into reusable modules.
* Compare selected winners with independently verified final results.
* Track the collection timestamp and original source for each prediction.
* Evaluate performance over clearly defined historical periods.
* Calculate accuracy, precision, recall, and other appropriate classification metrics when the data supports them.
* If evaluating betting performance, calculate return on investment, profit and loss, drawdown, and other relevant metrics using realistic odds and settlement assumptions.
* Add automated tests for CSV handling, parsing, winner-selection rules, and evaluation logic.
* Store configuration options outside the main scripts.
* Improve logging so that failed matches can be reviewed without losing the rest of the processing run.

These improvements would make the system easier to maintain and would help distinguish agreement with an external prediction source from independently measured predictive performance.

---

## Responsible Use and Risk Disclaimer

This project is intended for software development, football data analysis, prediction research, and educational purposes.

Football matches are uncertain, and no prediction method guarantees a correct outcome or profitable betting strategy. External model-generated probabilities may be inaccurate, poorly calibrated, or based on assumptions that are not visible to the user.

Do not interpret the presence of an AI model or a high published probability as a guarantee of success. Before evaluating a strategy, use independently verified match results, suitable historical testing, and realistic betting assumptions.

The author does not guarantee prediction accuracy, financial returns, or the availability of external websites. Users are responsible for complying with applicable laws, website terms, and betting-platform rules.

---

## Future Development Roadmap

* [ ] Improve website data extraction and error handling.
* [ ] Add configuration for live and scheduled matches.
* [ ] Improve team-name normalization and matching.
* [ ] Validate probability values and missing data.
* [ ] Compare predictions with verified match results.
* [ ] Produce historical prediction-performance reports.
* [ ] Add automated tests for the core functions.
* [ ] Develop visual reports for exploring prediction outcomes.
* [ ] Evaluate betting strategies using realistic historical odds and costs.

---

## Author

**Ezee Kits**

Electrical and Electronics Engineer | Python Developer | Automation and Data Analysis

* **Portfolio:** https://ezee-kits-portfolio.onrender.com/
* **GitHub:** https://github.com/Ezee-Kits/
* **YouTube:** https://www.youtube.com/@EzeeKits

Explore my projects and tutorials covering Python programming, automation, data processing, machine learning, and other software development topics.



*AI Football Prediction Analysis — collecting football data, analyzing externally published probabilities, and evaluating rule-based winner selections with Python.*
