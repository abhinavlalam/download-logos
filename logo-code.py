import os
import pandas as pd
import requests

# Replace with your actual API key
API_KEY = "pk_EDewhj1GRoKhB0VOz0uFYQ"
API_URL = "https://api.logo.dev/search?q="

# File paths
input_file = "companies.xlsx"  # Path to your Excel file
output_folder = "logos"  # Folder to save the logos

# Create the output folder if it doesn't exist
os.makedirs(output_folder, exist_ok=True)

# Load the Excel file
companies_df = pd.read_excel(input_file)

# Ensure the column with company names is correctly labeled
# Replace 'CompanyName' with the actual column name in your Excel file
company_column = "Company"

# Iterate through the list of companies
for company_name in companies_df["Company"]:
    try:
        # Send request to logo.dev API
        response = requests.get(f"{API_URL}{company_name}", headers={"Authorization": f"Bearer: {API_KEY}"})
        
        if response.status_code != 200:
            print(f"Failed to fetch logo for {company_name}: {response.status_code}")
            continue

        # Parse the JSON response
        logos = response.json()

        if not logos:
            print(f"No logos found for {company_name}.")
            continue

        # Download the first logo from the response
        logo_url = logos[0].get("logo_url")

        if logo_url:
            logo_response = requests.get(logo_url)

            if logo_response.status_code == 200:
                # Save the logo as a file
                file_name = f"{company_name.replace(' ', '_')}.png"
                file_path = os.path.join(output_folder, file_name)

                with open(file_path, "wb") as file:
                    file.write(logo_response.content)

                print(f"Downloaded logo for {company_name}.")
            else:
                print(f"Failed to download logo for {company_name}: {logo_response.status_code}")
        else:
            print(f"No valid logo URL found for {company_name}.")

    except Exception as e:
        print(f"Error fetching logo for {company_name}: {e}")

print("Logo download process completed.")
