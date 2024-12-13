import csv
import os
from glob import glob
def read_players_csv():
    players = {}
    with open('players.csv', 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            players[row['Name']] = row
    return players

def update_stats(csv_file, players):
    with open(csv_file, 'r', encoding="utf-8-sig") as file:
        file.readline()  # Skip the header row
        fieldnames = ['SurnameSorted ascSorted desc','NameSorted ascSorted desc','TeamSorted ascSorted desc','MatchesSorted ascSorted desc','SetsSorted ascSorted desc','PointsSorted ascSorted desc','BPSorted ascSorted desc','W-PSorted ascSorted desc','S =Sorted ascSorted desc','S !Sorted ascSorted desc','S /Sorted ascSorted desc','S -Sorted ascSorted desc','S +Sorted ascSorted desc','S #Sorted ascSorted desc','R =Sorted ascSorted desc','R !Sorted ascSorted desc','R /Sorted ascSorted desc','R -Sorted ascSorted desc','R +Sorted ascSorted desc','R #Sorted ascSorted desc','Pos%Sorted ascSorted desc','Exc.%Sorted ascSorted desc','A =Sorted ascSorted desc','A !Sorted ascSorted desc','A /Sorted ascSorted desc','A -Sorted ascSorted desc','A +Sorted ascSorted desc','A #Sorted ascSorted desc','Exc. %Sorted ascSorted desc','B =Sorted ascSorted desc','B !Sorted ascSorted desc','B /Sorted ascSorted desc','B -Sorted ascSorted desc','B +Sorted ascSorted desc','B #Sorted ascSorted desc']
        reader = csv.DictReader(file, fieldnames=fieldnames)
        for row in reader:
            name = row['SurnameSorted ascSorted desc'] + " " + row['NameSorted ascSorted desc']
            if name in players:
                if name == "SALLES ARAUJO Lucas":
                    print(row)
                player = players[name]
                if player['Points per Set'] == 'N/A':
                    newval = round(int(row['PointsSorted ascSorted desc']) / int(row['SetsSorted ascSorted desc']), 2)
                    player['Points per Set'] = f"{newval}({row['PointsSorted ascSorted desc']}/{int(row['SetsSorted ascSorted desc'])})"
                if player['Aces per Set'] == 'N/A':
                    newval = round(int(row['S #Sorted ascSorted desc']) / int(row['SetsSorted ascSorted desc']),2)
                    player['Aces per Set'] = f"{newval}({row['S #Sorted ascSorted desc']}/{int(row['SetsSorted ascSorted desc'])})"
                if player['Blocks per Set'] == 'N/A':
                    newval = round(int(row['B #Sorted ascSorted desc']) / int(row['SetsSorted ascSorted desc']),2)
                    player['Blocks per Set'] = f"{newval}({row['B #Sorted ascSorted desc']}/{int(row['SetsSorted ascSorted desc'])})"
                if player['Reception Percentage'] == 'N/A':
                    good = int(row['R #Sorted ascSorted desc']) + int(row['R #Sorted ascSorted desc'])
                    total = (int(row['R #Sorted ascSorted desc']) + int(row['R #Sorted ascSorted desc']) + int(row['R -Sorted ascSorted desc']) + int(row['R /Sorted ascSorted desc']) + int(row['R !Sorted ascSorted desc']) + int(row['R =Sorted ascSorted desc']))
                    if total != 0:
                        player['Reception Percentage'] = f"{int((good*100)/total)}%({good}/{total})"
                if player['Attack Percentage'] == 'N/A':
                    good = int(row['A #Sorted ascSorted desc']) + int(row['A #Sorted ascSorted desc'])
                    total = (int(row['A #Sorted ascSorted desc']) + int(row['A #Sorted ascSorted desc']) + int(row['A -Sorted ascSorted desc']) + int(row['A /Sorted ascSorted desc']) + int(row['A !Sorted ascSorted desc']) + int(row['A =Sorted ascSorted desc']))
                    if total != 0:
                        player['Attack Percentage'] = f"{int((good*100)/total)}%({good}/{total})"

def write_to_csv(players):
    fieldnames = ['Name','Date of Birth','Height','Position','Points per Set','Aces per Set','Blocks per Set','Reception Percentage','Attack Percentage','volleybox','Nationality','League Site']
    with open('players.csv', 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for player, stats in players.items():
            writer.writerow(stats)

def main():
    players = read_players_csv()
    csv_files = glob('/Users/alexgaynor/Documents/Maccabi/CSVs/*.csv')
    for csv_file in csv_files:
        update_stats(csv_file, players)
    # Now players dictionary contains the updated stats
    write_to_csv(players)
    csv_files = glob('/Users/alexgaynor/Documents/Maccabi/CSVs/*.csv')
    for csv_file in csv_files:
        os.remove(csv_file)

if __name__ == '__main__':
    main()
