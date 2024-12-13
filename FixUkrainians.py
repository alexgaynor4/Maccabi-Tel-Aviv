import csv
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

# Initialize the Chrome driver
options = webdriver.ChromeOptions()
options.add_argument('--headless')  # Run Chrome in headless mode
driver = webdriver.Chrome(options=options)

def get_ukr_link(name):
    driver.get('https://uvf-web.dataproject.com/CompetitionPlayerSearch.aspx?ID=63')

    # Find search bar and input first name
    search_bar = driver.find_element(By.ID, 'ctl00_Content_Main_RSB_SearchPlayerByText_Input')
    search_bar.send_keys(name.split(" ")[0])
    search_bar.send_keys(Keys.RETURN)
    # Wait for the results to load
    time.sleep(2)
    soup = BeautifulSoup(driver.page_source, "html.parser")
    # Find all the player rows in the HTML
    try:
        player = driver.find_element(By.ID, 'ctl00_Content_Main_PlayersListView_ctrl0_PlayerRow')
    except:
        return "none"
    else:
        player.click()
        time.sleep(1)
        return driver.current_url

players = []
with open('players.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        player = dict(row)
        # If the player is from UKR, update the "League Site"
        if player['Nationality'] == 'UKR':
            if (get_ukr_link(player['Name']) != "none"):
                player['League Site'] = get_ukr_link(player['Name'])
        players.append(player)

# Update the CSV file
with open('players.csv', 'w', newline='') as csvfile:
    fieldnames = ['Name', 'Date of Birth', 'Height', 'Position', 'Points per Set', 'Aces per Set', 'Blocks per Set', 'Reception Percentage', 'Attack Percentage', 'volleybox', 'Nationality', 'League Site']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for player in players:
        writer.writerow(player)

# Close the driver
driver.quit()
