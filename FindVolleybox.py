import csv
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import time
from selenium import webdriver
from unidecode import unidecode
import os
import shutil


# Step 1: Modify the CSV file to include the "volleybox" header
csv_file = 'players.csv'
new_csv_file = 'players1.csv'

# Configure Selenium WebDriver
options = webdriver.ChromeOptions()
options.add_argument('--headless')  # Run Chrome in headless mode
driver = webdriver.Chrome(options=options)

with open(csv_file, 'r') as file:
    reader = csv.reader(file)
    header = next(reader)  # Read the header

    # Step 2: Loop through each row
    with open(new_csv_file, 'w', newline='') as new_file:
        writer = csv.writer(new_file)
        writer.writerow(header)  # Write the modified header

        for row in reader:
            name = row[0]
            first_name = name.split(" ")[0]
            search_url = f'https://volleybox.net/search?q={first_name}#players'
            driver.get(search_url)
            time.sleep(2)
            page_source = driver.page_source
            # Create a BeautifulSoup object from the page source
            soup = BeautifulSoup(page_source, 'html.parser')
            # Find all <div> elements with class "item_box" (players)
            player_divs = soup.find_all('div', class_='item_box')
            player_found = False

            # Check if the player's name matches
            for player_div in player_divs:
                player_name = unidecode(player_div.find('span', class_='fontSize12pt').text.strip())
                # Compare each word in the names
                name_words = unidecode(name).lower().split()
                player_name_words = player_name.lower().split()
                if all(word in player_name_words for word in name_words) or all(
                        word in name_words for word in player_name_words):
                    # Step 7: Append the search URL to the player's row in the CSV file
                    player_found = True
                    url_found = player_div.find('a')['href']
                    if len(row) <= header.index('volleybox'):
                        print(row)
                        print(len(row))
                        print(header.index('volleybox'))
                    else:
                        row[header.index('volleybox')] = url_found
                    response = requests.get(url_found)
                    soup = BeautifulSoup(response.content, 'html.parser')
                    height_dt = soup.find('dt', string="Height")
                    if height_dt:
                        height = height_dt.find_next('dd').text.strip()
                        row[header.index('Height')] = height
                    else:
                        row[header.index('Height')] = "N/A"
                    if row[header.index('Date of Birth')] == "-":
                        birthdate_dt = soup.find('dt', string="Birthdate")
                        if birthdate_dt:
                            birthdate = birthdate_dt.find_next('dd').text.strip()
                            birthdate = datetime.strptime(birthdate, '%Y-%m-%d').strftime('%d/%m/%Y')
                            row[1] = birthdate
                    if row[header.index('Position')] == "N/A" or row[header.index('Position')] == "-":
                        position_dt = soup.find('dt', string="Position")
                        if position_dt:
                            position = position_dt.find_next('dd').text.strip()
                            row[3] = position
                    break
            if not player_found:
                row[header.index('volleybox')] = " "
                row[header.index('Height')] = "N/A"
            writer.writerow(row)
driver.quit()

# remove the original file
os.remove('players.csv')
# rename the temporary file
shutil.move('players1.csv', 'players.csv')

print("Success!")
