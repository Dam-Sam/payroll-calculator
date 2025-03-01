import requests
from bs4 import BeautifulSoup
import json
import os

set_year = "2025"

cpp_url = "https://www.canada.ca/en/revenue-agency/services/tax/businesses/topics/payroll/payroll-deductions-contributions/canada-pension-plan-cpp/cpp-contribution-rates-maximums-exemptions.html"
ei_url = "https://www.canada.ca/en/revenue-agency/services/tax/businesses/topics/payroll/payroll-deductions-contributions/employment-insurance-ei/ei-premium-rates-maximums.html"
tax_rates_url = "https://www.canada.ca/en/revenue-agency/services/forms-publications/payroll/t4032-payroll-deductions-tables/t4032on-jan/t4032on-january-general-information.html"

# JSON file to store the extracted data
json_file = "yearly_rates.json"

def update_json_key(key, new_value):
    try:
        # Load existing JSON data
        with open(json_file, "r") as file:
            data = json.load(file)
        
        # Update the specific key if it exists
        if key in data:
            data[key] = new_value
            with open(json_file, "w") as file:
                json.dump(data, file, indent=4)
            print(f"Updated '{key}' to {new_value}")
        else:
            print(f"Key '{key}' not found in JSON file.")

    except FileNotFoundError:
        print("JSON file not found!")
    except json.JSONDecodeError:
        print("Error reading JSON file!")

def get_cpp_constants():
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(cpp_url, headers=headers)
        response.raise_for_status()

        # Parse the HTML content
        soup = BeautifulSoup(response.text, "html.parser")

        # Find the table containing CPP values (adjust this if needed)
        table = soup.find("table")

        # Extract rows from the table
        rows = table.find_all("tr")[1:]  # Skip header row

        cpp_constants = {}

        for row in rows:
            cols = row.find_all("td")
            year = cols[0].text.strip()  # Get the year (e.g., 2025)
            
            if set_year in year:
                cpp_constants = {
                    "year": int(set_year),
                    "maximum_earnings": float(cols[1].text.strip().replace("$", "").replace(",", "")),
                    "basic_exemption": float(cols[2].text.strip().replace("$", "").replace(",", "")),
                    "pensionable_earnings": float(cols[3].text.strip().replace("$", "").replace(",", "")),
                    "rate": float(cols[4].text.strip()),
                    "max_contribution_employee": float(cols[5].text.strip().replace("$", "").replace(",", "")),
                    "max_contribution_self_employed": float(cols[6].text.strip().replace("$", "").replace(",", ""))
                }
                break  # Stop after finding 2025

        # Store in JSON file
        if cpp_constants:
            update_json_key("cpp", cpp_constants)
            print(f"CPP constants for 2025 saved in {json_file}")
        else:
            print("Failed to extract 2025 CPP data.")

    except Exception as e:
        print(f"Error fetching CPP data: {e}")

def get_ei_constants():
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(ei_url, headers=headers)
        response.raise_for_status()

        # Parse the HTML content
        soup = BeautifulSoup(response.text, "html.parser")

        # Find the table containing CPP values (adjust this if needed)
        table = soup.find("table")
        
        # Extract rows from the table
        rows = table.find_all("tr")[1:]  # Skip header row

        ei_constants = {}

        for row in rows:
            cols = row.find_all("td")
            year = cols[0].text.strip()  # Get the year (e.g., 2025)
            print(year)
            if set_year in year:
                ei_constants = {
                    "year": int(set_year),
                    "maximum_earnings": float(cols[1].text.strip().replace("$", "").replace(",", "")),
                    "rate": float(cols[2].text.strip().replace("$", "").replace(",", "")),
                    "maximum_employee_premium": float(cols[3].text.strip().replace("$", "").replace(",", "")),
                    "maximum_employer_premium": float(cols[4].text.strip().replace("$", "").replace(",", ""))
                }
                break  # Stop after finding 2025

        # Store in JSON file
        if ei_constants:
            update_json_key("ei", ei_constants)
            print(f"EI constants for 2025 saved in {json_file}")
        else:
            print("Failed to extract 2025 EI data.")

    except Exception as e:
        print(f"Error fetching EI data: {e}")

def get_tax_rates():
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(tax_rates_url, headers=headers)
        response.raise_for_status()

        # Parse the HTML content
        soup = BeautifulSoup(response.text, "html.parser")

        # Find the table containing CPP values (adjust this if needed)
        tables = soup.find_all("table")
        
        for table in tables:
            if table.caption:
                if "federal tax rates" in table.caption.text.lower():
                    rows = table.find_all("tr")[1:]

                    federal_tax = {
                        "bracket": [],
                        "rates": [],
                        "constants": []
                    }
                    for row in rows:
                        cols = row.find_all("td")
                        federal_tax["bracket"].append(cols[0].text.strip().replace("$", "").replace(",", ""))
                        federal_tax["rates"].append(cols[2].text.strip().replace("$", "").replace(",", ""))
                        federal_tax["constants"].append(cols[3].text.strip().replace("$", "").replace(",", ""))

                if "ontario tax rates" in table.caption.text.lower():
                    rows = table.find_all("tr")[1:]

                    ontario_tax = {
                        "bracket": [],
                        "rates": [],
                        "constants": []
                    }
                    for row in rows:
                        cols = row.find_all("td")
                        ontario_tax["bracket"].append(cols[0].text.strip().replace("$", "").replace(",", ""))
                        ontario_tax["rates"].append(cols[2].text.strip().replace("$", "").replace(",", ""))
                        ontario_tax["constants"].append(cols[3].text.strip().replace("$", "").replace(",", ""))

        # Store in JSON file
        if federal_tax:
            update_json_key("federal_tax", federal_tax)
            print(f"federal tax constants for 2025 saved in {json_file}")
        else:
            print("Failed to extract 2025 federal tax constants.")

        if ontario_tax:
            update_json_key("ontario_tax", ontario_tax)
            print(f"ontario tax constants for 2025 saved in {json_file}")
        else:
            print("Failed to extract 2025 ontario tax constants.")

    except Exception as e:
        print(f"Error fetching CPP data: {e}")

#get_cpp_constants()
#get_ei_constants()
get_tax_rates()