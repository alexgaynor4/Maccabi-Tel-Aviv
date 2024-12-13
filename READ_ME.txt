The python files are used to scrape the various International volleyball league websites. Overall.py runs them in order. script.js and index.html are used to display the csv and have filters for different statistics. A recently updated version of the statistics is seen in players.csv

To view website:

Download Python: https://www.python.org/downloads/
From terminal/command prompt:
Make sure it is installed with: python -V or python3 -V or py -V
Navigate to directory Maccabi
Run python -m http.server or python3 -m http.server
Go to localhost:8000 in browser

To run the Web Scraper to update players:

Download chromedriver: https://chromedriver.chromium.org/downloads
Download Beautiful Soup: run: pip install beautifulsoup4 or pip3 install beautifulsoup4
Download Unidecode: run: pip install unidecode or pip3 install unidecode
Run Overall.py: Navigate to Maccabi
Then, from command line, use: python Overall.py or python3 Overall.py
It will take about 2.5 hours
Duplicate players.csv beforehand in case there is an issue
