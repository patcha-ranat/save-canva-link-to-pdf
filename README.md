# save-canva-link-to-pdf

*Patcharanat P.*

*Automated Saving Canva Link to PDF with Selenium*

# Installation

## Pre-requisites

- Python version `>=3.9,<=3.12` installed
- `chromedriver.exe` downloaded and placed in `./scripts/chromedriver.exe`
    - (chromedriver version must match with your current chrome version, more detail in this [link](https://developer.chrome.com/docs/chromedriver/downloads))

```bash
# preparing poetry environment
export POETRY_HOME="/c/Users/<user>/.poetry-env"
export VENV_PATH="${POETRY_HOME}/Scripts"
export PATH="${VENV_PATH}:${PATH}"
# exported variables available only within a session

python -m venv ~/.poetry-env

${VENV_PATH}/pip install poetry
# OR ${VENV_PATH}/python pip install poetry

poetry install
```

# Getting Started

You can change the paramaters in the script as needed, like url to scrape, element to extract image URL from, number of pages to iterate, etc.

```bash
poetry run python scripts/scrape.py
# output at ./output_example/output_scrape.pdf

poetry run python scripts/capture.py
# output at ./output_example/output_scrape.pdf
```

# Explanation

## 1. scrape.py

Using `selenium` to scrape thumbnail URLs from grid view to convert to image (through bytes) and export as pdf. This method is fast, but give low-resolution output due to using thumbnail image.
- In order to retrived all the thumbnail URLs, we need to scroll down the ***scroll element*** to the end to let the page be fully loaded
- URL pattern can not be iterated, so we need to keep order of retrieved URLs when extracting it by using custom method: `list_union` which work like `set` but keep ordering.

## 2. capture.py

Using `selenium` to automate slide changing then, use `pyautogui` to capture each slide, which give a better resolution compared with scraping approach.
- We iterate slides from the last to the first to avoid slide transition (or motion).
- If output pdf skip some pages, please set a higher wait time `(s)` between capturing, to give them some time for loading the screen.

*Note: please use with caution, scraping can increase unneccessary workload for the target website.*
