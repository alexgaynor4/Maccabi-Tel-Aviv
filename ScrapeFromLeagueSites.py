import csv
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

# Open the CSV file in append mode
with open("players.csv", "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    league_urls = ["https://ossrb-web.dataproject.com/CompetitionHome.aspx?ID=62", "https://hvl-web.dataproject.com/CompetitionHome.aspx?ID=42", "https://lnv-web.dataproject.com/CompetitionHome.aspx?ID=90", "https://lnv-web.dataproject.com/CompetitionHome.aspx?ID=89", "https://uvf-web.dataproject.com/CompetitionHome.aspx?ID=63", "https://hos-web.dataproject.com/CompetitionHome.aspx?ID=78", "https://mevza-web.dataproject.com/CompetitionHome.aspx?ID=43", "https://cvf-web.dataproject.com/CompetitionHome.aspx?ID=27", "https://ozs-web.dataproject.com/CompetitionHome.aspx?ID=88", "https://bvf-web.dataproject.com/CompetitionHome.aspx?ID=28", "https://tvf-web.dataproject.com/CompetitionHome.aspx?ID=78", "https://swi-web.dataproject.com/CompetitionHome.aspx?ID=50", "https://rfevb-web.dataproject.com/CompetitionHome.aspx?ID=111", "https://fpv-web.dataproject.com/CompetitionHome.aspx?ID=72", "https://frv-web.dataproject.com/CompetitionHome.aspx?ID=30", "https://lml-web.dataproject.com/CompetitionHome.aspx?ID=102", "https://hvf-web.dataproject.com/CompetitionHome.aspx?ID=33", "https://svbf-web.dataproject.com/CompetitionHome.aspx?ID=314"]
    nums = [0, 1, 2, 6, 7]
    names = []
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # Run Chrome in headless mode

    writer.writerow(
        ['Name','Date of Birth','Height','Position','Points per Set','Aces per Set','Blocks per Set','Reception Percentage','Attack Percentage','volleybox','Nationality','League Site'])
    for url in league_urls :
        driver = webdriver.Chrome(options=options)
        driver.get(url)
        lang_dropdown = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.ID, "RadComboCulture_Arrow")))
        lang_dropdown.click()
        # Find the option with the value "100" and click on it
        option_EN = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//li[text()='EN']")))
        option_EN.click()
        rows = []
        for i in nums:
            # Set up the Selenium webdriver
            driver.get(url)
            # Get the URL of the "Complete Ranking" page
            ranking_i = "#Content_Main_ctl05_RP_Ranking_Main_HYL_CompleteRanking_" + str(i)
            complete_ranking_url = driver.find_element(By.CSS_SELECTOR, ranking_i).get_attribute("href")
            # Navigate directly to the "Complete Ranking" page
            driver.get(complete_ranking_url)
            # Wait for the dropdown options to be available
            dropdown = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.ID, "ctl00_Content_Main_LV_Ranking_RDP2_ctl01_PageSizeComboBox_Arrow")))
            dropdown.click()
            # Find the option with the value "100" and click on it
            option_100 = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//li[text()='100']")))
            option_100.click()
            # Wait for the page to load and the table to update with the new page size
            time.sleep(0.5)  # Adjust the wait time as needed
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            player_divs = soup.find_all("div", id=lambda value: value and value.startswith("ctl00_Content_Main_LV_Ranking_ctrl"))
            # Write player data to CSV
            for div in player_divs:
                name_element = div.find("span", class_="Ranking_PlayerName")
                name = name_element.text.strip() if name_element else "N/A"
                data_element = div.find("span", class_="Ranking_PlayerData")
                data = data_element.text.strip() if data_element else "N/A"
                if name != "N/A":
                    # Check if the player's name already exists in the CSV file
                    if name in names:
                        # Update the stats for the duplicate player
                        for row in rows:
                            if name == row[0]:
                                if i in [0, 1, 2]:
                                    row[i + 4] = data
                                elif i in [6, 7]:
                                    row[i + 1] = data
                                break
                    else:
                        # Player's name does not exist, append a new row with name and data
                        row = ["N/A"] * 11
                        if i in [0, 1, 2]:
                            row[i + 3] = data
                        elif i in [6, 7]:
                            row[i] = data
                        rows.append([name] + row)
                        names.append(name)
        new_rows = []
        for row in rows:
            numNAs = 0
            for i in range (4,9) :
                if (row[i] == "N/A"):
                    numNAs += 1
            if (numNAs <= 3) :
                new_rows.append(row)
        for row in new_rows:
            driver.get(url.replace("Home", "PlayerSearch"))
            search = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.ID, "ctl00_Content_Main_RSB_SearchPlayerByText_Input")))
            search.send_keys(row[0].split(" ")[0])
            search.send_keys(Keys.ENTER)
            time.sleep(0.5)
            # Create a BeautifulSoup object to parse the HTML
            soup = BeautifulSoup(driver.page_source, "html.parser")
            # Find all the player rows in the HTML
            player_rows = soup.select('div[id*="PlayerRow"]')
            for player in player_rows:
                player_name_element = player.find("p", style="margin:1px 0;line-height:50px;text-align:left;font-weight:bold;")
                if player_name_element and player_name_element.text.strip() == row[0]:
                    player_link = player["onclick"]
                    player_id = player_link.split("PlayerID=")[1].split("&")[0]
                    team_id = player_link.split("TeamID=")[1].split("&")[0]
                    individual_site_url = f"{url.split('I')[0].replace('CompetitionHome', 'PlayerDetails')}TeamID={team_id}&PlayerID={player_id}&{url.split('?')[1]}"
                    driver.get(individual_site_url)
                    soup = BeautifulSoup(driver.page_source, "html.parser")
                    # Find the desired elements based on their IDs
                    position_element = soup.find("span", id="Content_Main_PlayerView_LBL_Position")
                    nationality_element = soup.find("span", id="Content_Main_PlayerView_Label10")
                    dob_element = soup.find("span", id="Content_Main_PlayerView_LBL_BirthDate")
                    # Extract the text values from the elements
                    row[1] = dob_element.text.strip() if position_element else None
                    row[10] = nationality_element.text.strip() if nationality_element else None
                    row[3] = position_element.text.strip() if dob_element else None
                    row[11] = individual_site_url
                    break
        # Write the updated data back to the CSV file
        writer.writerows(new_rows)
        # Close the webdriver
        driver.quit()
