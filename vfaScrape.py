import requests
from bs4 import BeautifulSoup
import csv

output_csv = 'vfa_website_scrape.csv'

# Define the base URL
base_url = "https://ventureforamerica.org/community/page/"

# Start with the first page
page_number = 1

# Create a loop to scrape multiple pages
with open(output_csv, mode='w', newline='') as csv_file:
    csv_writer = csv.writer(csv_file)
    person_info_map = {} # name: [school, location, startup]
    csv_writer.writerow(["name", "school", "location", "vfa startup"])
    
    while page_number <= 96:
        url = f"{base_url}{page_number}/?is_alumni=true"
        response = requests.get(url)

        # Check if the request was successful (status code 200)
        if response.status_code != 200:
            print(f"Failed to retrieve page {page_number}")
            break  # Exit the loop if the page is not found or an error occurs

        soup = BeautifulSoup(response.content, 'lxml')
        
        all_cards = soup.find_all('div', class_='col-12 col-md-3 mbm')
        for card in all_cards:
            name_div = card.find('div', class_='card-name')
            school_div = card.find('div', class_='card-college mbxxs')
            
            output_row = ["","","",""]
            if name_div and school_div:
                name = name_div.get_text(strip=True)
                school = school_div.get_text(strip=True)
                output_row[0] = name
                output_row[1] = school
            
            spans = card.find_all('span')
            for span in spans:
                svg = span.find('svg')
                if svg and '<use xlink:href="#sym-location">' in str(svg):
                    # Extract the text content from the <span>
                    loc = span.get_text(strip=True)
                    output_row[2] = loc
            
                if svg and '<use xlink:href="#sym-startup">' in str(svg):
                    # Extract the text content from the <span>
                    startup = span.get_text(strip=True)
                    output_row[3] = startup
            
            csv_writer.writerow(output_row)

        page_number += 1