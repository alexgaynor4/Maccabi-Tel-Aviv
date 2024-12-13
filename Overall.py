import subprocess
import time

# List of python scripts you want to run
scripts = ["ScrapeFromLeagueSites.py", "FindVolleybox.py", "FixUkrainians.py", "DownloadCSVs.py", "UpdateStatsFromCSVs.py"]

# Need to update file directories

start_time = time.time()

for script in scripts:
    start_script_time = time.time()  # Start time for each script
    subprocess.call(["python3", script])
    elapsed_time = time.time() - start_script_time  # Calculate elapsed time

print("Success!")
