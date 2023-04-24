import os
import csv
import sys
import time
import requests

def search_linkedin(query):
    print(f"Searching LinkedIn for: {query}")
    linkedin_links = []

    base_url = "https://www.googleapis.com/customsearch/v1"
    params = {
        "key": os.environ["GOOGLE_API_KEY"],
        "cx": os.environ["GOOGLE_CSE_ID"],
        "q": query,
        "num": 10,
    }
    response = requests.get(base_url, params=params)
    search_results = response.json()

    if 'items' in search_results:
        for result in search_results["items"]:
            url = result["link"]
            if "linkedin.com/in/" in url:
                linkedin_links.append(url)

    return linkedin_links

if len(sys.argv) < 2:
    print("Please provide an input file containing email addresses.")
    sys.exit(1)

input_file = sys.argv[1]
output_file = "linkedin_profiles.csv"

try:
    with open(input_file, newline="") as csvfile:
        reader = csv.reader(csvfile)
        with open(output_file, "w", newline="") as output_csvfile:
            writer = csv.writer(output_csvfile)
            for row in reader:
                if len(row) == 3:
                    name, surname, email = row
                    if name and surname:
                        profiles = search_linkedin(f"{name} {surname} site:linkedin.com/in/")
                    else:
                        name_and_surname = email.split("@")[0].replace(".", " ").replace("_", " ").replace("-", " ")
                        profiles = search_linkedin(f"{name_and_surname} site:linkedin.com/in/")
                elif len(row) == 1:
                    email = row[0]
                    name_and_surname = email.split("@")[0].replace(".", " ").replace("_", " ").replace("-", " ")
                    profiles = search_linkedin(f"{name_and_surname} site:linkedin.com/in/")
                else:
                    print("Invalid row format.")
                    continue

                for profile in profiles:
                    writer.writerow([profile])

                # Wait for 10 seconds before the next search to avoid potential rate limiting
                time.sleep(10)

    print(f"LinkedIn profiles saved to {output_file}")
except FileNotFoundError:
    print("Input file not found.")
    sys.exit(1)

