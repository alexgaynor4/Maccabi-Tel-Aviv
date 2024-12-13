import os
import pandas as pd
from urllib.parse import urlparse, parse_qs
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

# Set the download directory path
download_dir = '/Users/alexgaynor/Documents/Maccabi/CSVs'

# Configure Chrome options to set download directory
chrome_options = Options()
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument('--headless')
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_experimental_option('prefs', {
    'download.default_directory': download_dir,
    'download.prompt_for_download': False,
    'download.directory_upgrade': True,
    'safebrowsing.enabled': True
})

# Set the path to your Chrome driver executable
#chromedriver_path = '/Users/alexgaynor/Downloads/chromedriver_mac64/chromedriver'  # Update with your actual path

# Launch Chrome browser
driver = webdriver.Chrome(options=chrome_options)

urls = ["https://ossrb-web.dataproject.com/Statistics_AllPlayers.aspx?ID=62&PID=0","https://hvl-web.dataproject.com/Statistics_AllPlayers.aspx?ID=42&PID=58", "https://lnv-web.dataproject.com/Statistics_AllPlayers.aspx?ID=90&PID=0", "https://lnv-web.dataproject.com/Statistics_AllPlayers.aspx?ID=89&PID=0", "https://uvf-web.dataproject.com/Statistics_AllPlayers.aspx?ID=63&PID=0", "https://hos-web.dataproject.com/Statistics_AllPlayers.aspx?ID=78&PID=0", "https://cvf-web.dataproject.com/Statistics_AllPlayers.aspx?ID=27&PID=0", "https://bvf-web.dataproject.com/Statistics_AllPlayers.aspx?ID=28&PID=30", "https://tvf-web.dataproject.com/Statistics_AllPlayers.aspx?ID=78&PID=0", "https://rfevb-web.dataproject.com/Statistics_AllPlayers.aspx?ID=111&PID=137", "https://frv-web.dataproject.com/Statistics_AllPlayers.aspx?ID=30&PID=38", "https://lml-web.dataproject.com/Statistics_AllPlayers.aspx?ID=102&PID=111", "https://hvf-web.dataproject.com/Statistics_AllPlayers.aspx?ID=33&PID=39", "https://svbf-web.dataproject.com/Statistics_AllPlayers.aspx?ID=314&PID=0", "https://osbih-web.dataproject.com/Statistics_AllPlayers.aspx?ID=27&PID=37"]
# Open the website
driver.get('https://ossrb-web.dataproject.com/Statistics_AllPlayers.aspx?ID=62&PID=0')

for url in urls:
    # Open the website
    driver.get(url)

    # Find and click the button
    button = driver.find_element(By.ID, 'Content_Main_ImageButton1')
    button.click()

    # Wait for the download to complete (you may need to adjust the waiting time)
    time.sleep(2)

    # Get the filename from the URL
    parsed_url = urlparse(url)
    query_params = parse_qs(parsed_url.query)
    prefix = parsed_url.netloc.split('-')[0]
    competition_id = query_params['ID'][0]
    filename = f"{prefix}_Stats_All_Players_CompetitionID_{competition_id}.xls"
    new_filename = prefix + ".csv"
    file_path = os.path.join(download_dir, filename)
    new_file_path = os.path.join(download_dir, new_filename)
    data = pd.read_excel(file_path)
    data.to_csv(new_file_path, index=False)
    os.remove(file_path)
# Close the browser
driver.quit()
