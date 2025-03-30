import csv
import sys
import requests
import json
from bs4 import BeautifulSoup
import time
import re

def search_obituary(first_name, middle_name, last_name, city, state, zip_code, dob_year):
    """Search Legacy.com for an obituary using firstName and lastName parameters."""
    full_name = " ".join(filter(None, [first_name, middle_name, last_name])).strip()
    print(f"Checking {full_name} on Legacy.com")
    
    url = f"https://www.legacy.com/obituaries/search?firstName={first_name}&lastName={last_name}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        script_tags = soup.find_all('script', text=re.compile('obituaryList'))
        if not script_tags:
            print("No obituaryList data found in the page")
            return "NO", ""
        
        script_content = script_tags[0].string
        json_match = re.search(r'<!--(.*)-->', script_content, re.DOTALL)
        if not json_match:
            print("Could not extract JSON from script tag")
            return "NO", ""
        
        json_str = json_match.group(1)
        data = json.loads(json_str)
        
        obituaries = data.get('obituaryList', {}).get('obituaries', [])
        print(f"Found {len(obituaries)} results")
        
        full_name_lower = full_name.lower()
        middle_initial = middle_name[0].lower() if middle_name else ""
        location = f"{city} {state}".lower() if city and state else ""
        
        for i, obit in enumerate(obituaries, 1):
            obit_name = obit['name']['fullName'].lower()
            obit_city = obit['location']['city']['fullName'].lower() if obit['location'].get('city') else ""
            obit_state = obit['location']['state']['code'].lower() if obit['location'].get('state') else ""
            obit_location = f"{obit_city} {obit_state}".strip()
            obituary_url = obit['links']['obituaryUrl']['href']
            
            print(f"Result {i}: {obit_name} - {obit_location}")
            print(f"Result {i} URL: {obituary_url}")
            
            name_match_full = full_name_lower == obit_name
            name_match_initial = f"{first_name.lower()} {middle_initial} {last_name.lower()}".strip() in obit_name
            name_match = name_match_full or name_match_initial
            location_match = (not location) or (location in obit_location)
            
            if name_match and location_match:
                print(f"Possible match found for {full_name} at {obituary_url}")
                return "YES", obituary_url
        
        print(f"No likely match found for {full_name}")
    except Exception as e:
        print(f"Error searching for {full_name}: {e}")
    
    time.sleep(1)
    return "NO", ""

def process_csv(input_csv, output_csv):
    """Process the input CSV, write results to an output CSV, and display a summary table."""
    total_searched = 0
    positive_matches = 0
    
    with open(input_csv, 'r') as infile:
        lines = (line for line in infile if line.strip())
        reader = csv.DictReader(lines)
        expected_headers = {'FirstName', 'MiddleName', 'LastName', 'City', 'State', 'ZipCode', 'DOBYear'}
        if not expected_headers.issubset(reader.fieldnames):
            print("Headers found:", reader.fieldnames)
            print("Missing headers:", expected_headers - set(reader.fieldnames))
            raise ValueError("Input CSV is missing one or more required headers")
        infile.seek(0)
        reader = csv.DictReader(infile)
        fieldnames = reader.fieldnames + ["Likely Deceased", "URL"]
        with open(output_csv, 'w', newline='') as outfile:
            writer = csv.DictWriter(outfile, fieldnames=fieldnames)
            writer.writeheader()
            for row in reader:
                total_searched += 1
                print(f"\nProcessing {row['FirstName']} {row['LastName']}...")
                likely_deceased, url = search_obituary(
                    row['FirstName'], row['MiddleName'], row['LastName'],
                    row['City'], row['State'], row['ZipCode'], row['DOBYear']
                )
                row["Likely Deceased"] = likely_deceased
                row["URL"] = url
                if likely_deceased == "YES":
                    positive_matches += 1
                writer.writerow(row)
    
    # Print summary table
    print("\nProcessing complete.")
    print("\nSummary Table:")
    print("-----------------------------")
    print(f"| {'Metric':<20} | {'Count':<5} |")
    print("-----------------------------")
    print(f"| {'Total People Searched':<20} | {total_searched:<5} |")
    print(f"| {'Positive Matches':<20} | {positive_matches:<5} |")
    print("-----------------------------")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 obit_search_houston_co.py <input_file>")
        sys.exit(1)
    input_csv = sys.argv[1]
    output_csv = 'output.csv'
    process_csv(input_csv, output_csv)