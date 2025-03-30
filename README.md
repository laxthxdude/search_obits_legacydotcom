# Obituary Search Tool

This Python script searches for obituaries on Legacy.com using a list of names and locations from a CSV file. It processes each entry, checks for matches, and outputs an updated CSV with results indicating whether each person is likely deceased, along with the URL of any matching obituary. A summary table of total searches and positive matches is also displayed.

## Features
- Reads input from a CSV file with columns: `FirstName`, `MiddleName`, `LastName`, `City`, `State`, `ZipCode`, `DOBYear`.
- Searches Legacy.com for obituaries using first and last names.
- Matches results based on name and location (city and state).
- Outputs a CSV with two additional columns: `Likely Deceased` ("YES" or "NO") and `URL` (obituary link if found).
- Provides a summary table of total people searched and positive matches.

## Prerequisites
- A computer with internet access.
- Python 3 installed (see installation steps below if you don’t have it).
- Required Python libraries: `requests`, `beautifulsoup4`, and standard library modules (`csv`, `sys`, `json`, `re`, `time`).

## Installation

### Step 1: Install Python
If you don’t have Python installed, follow these steps based on your operating system:

#### macOS
1. **Check if Python is Installed**:
   - Open Terminal (Applications > Utilities > Terminal).
   - Run: `python3 --version`
   - If you see a version (e.g., `Python 3.9.6`), skip to Step 2. Otherwise, proceed.
2. **Install Homebrew (if not installed)**:
   - Run: `/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"`
   - Follow the prompts to install.
3. **Install Python**:
   - Run: `brew install python`
   - Verify: `python3 --version`

#### Windows
1. **Download Python**:
   - Visit [python.org/downloads](https://www.python.org/downloads/).
   - Download the latest Python 3 installer (e.g., Python 3.11.x).
2. **Run the Installer**:
   - Double-click the downloaded file.
   - Check "Add Python to PATH" at the bottom of the installer window.
   - Click "Install Now" and follow the prompts.
3. **Verify Installation**:
   - Open Command Prompt (search "cmd" in Start menu).
   - Run: `python --version`
   - You should see the version number.

#### Linux (Ubuntu/Debian)
1. **Update Package List**:
   - Open a terminal.
   - Run: `sudo apt update`
2. **Install Python**:
   - Run: `sudo apt install python3 python3-pip`
   - Verify: `python3 --version`

### Step 2: Install Dependencies
Once Python is installed, install the required libraries:

1. **Open a Terminal/Command Prompt**:
   - macOS: Terminal
   - Windows: Command Prompt
   - Linux: Terminal
2. **Install Libraries**:
   - Run: `python3 -m pip install requests beautifulsoup4`
   - On Windows, you might use `python -m pip install requests beautifulsoup4` if `python3` isn’t recognized.
   - This installs `requests` (for HTTP requests) and `beautifulsoup4` (for HTML parsing).

## Usage

1. **Prepare Your Input CSV**:
   - Create a CSV file (e.g., `input.csv`) with the following headers:
     ```
     FirstName,MiddleName,LastName,City,State,ZipCode,DOBYear
     ```
   - Example:
     ```
     FirstName,MiddleName,LastName,City,State,ZipCode,DOBYear
     Joanne,,Koeller,La Crescent,MN,55947,1935
     Seth,De Wayne,Aasen,La Crescent,MN,55947,1991
     ```

2. **Run the Script**:
   - Save the script as `search_obits_legacydotcom.py`.
   - Open a terminal in the directory containing the script and your CSV.
   - Run: `python3 search_obits_legacydotcom.py input.csv`
   - Replace `input.csv` with your CSV file’s name.

3. **Output**:
   - The script will:
     - Print processing details for each person.
     - Generate `output.csv` with results, including `Likely Deceased` and `URL` columns.
     - Display a summary table, e.g.:
       ```
       Summary Table:
       -----------------------------
       | Metric                | Count |
       -----------------------------
       | Total People Searched | 2     |
       | Positive Matches      | 1     |
       -----------------------------
       ```

## Example

### Input (`input.csv`):
```
FirstName,MiddleName,LastName,City,State,ZipCode,DOBYear
Joanne,,Koeller,La Crescent,MN,55947,1935
Seth,De Wayne,Aasen,La Crescent,MN,55947,1991
```

### Command:
```bash
python3 search_obits_legacydotcom.py input.csv
```

### Output (`output.csv`):
```
FirstName,MiddleName,LastName,City,State,ZipCode,DOBYear,Likely Deceased,URL
Joanne,,Koeller,La Crescent,MN,55947,1935,YES,https://www.legacy.com/us/obituaries/lacrossetribune/name/joanne-koeller-obituary?id=57868366
Seth,De Wayne,Aasen,La Crescent,MN,55947,1991,NO,
```

## Notes
- **Rate Limiting**: The script includes a 1-second delay between requests to avoid overwhelming Legacy.com. Adjust `time.sleep(1)` if needed.
- **Legal Considerations**: Ensure your use complies with Legacy.com’s terms of service. This tool is intended for personal, non-commercial use.
- **Error Handling**: The script handles basic errors (e.g., network issues, missing JSON), but complex failures may require manual debugging.

## Contributing
Feel free to fork this repository, submit issues, or create pull requests with improvements!

## License
This project is unlicensed and provided as-is for personal use. No warranty is implied.
