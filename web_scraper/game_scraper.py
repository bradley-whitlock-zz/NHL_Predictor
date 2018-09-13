import requests
from bs4 import BeautifulSoup
import csv

from utils.logger import log


def list_to_file(body, header=None, out_file_name="unnamed_data.csv"):
    log.info("writing data to {}".format(out_file_name))

    with open("data/{}".format(out_file_name), "w+") as my_csv:
        csvWriter = csv.writer(my_csv, delimiter=',')
        if header is not None:
            csvWriter.writerow(header)
        csvWriter.writerows(body)


def get_player_data(content, out_file_name):
    # Navigate to the name table on the page
    table = content.find("table", {"id": "stats"})
    rows = table.findAll("tr")

    # Remove header in table, in the players table there is 2 header rows
    rows = rows[2:]

    facts = ["player", "age", "pos", "team_id", "games_played", "goals", "assists", "points",
             "plus_minus", "pen_min", "ps", "shots", "shot_pct", "time_on_ice_avg", "blocks", "hits",
             "faceoff_wins", "faceoff_losses", "faceoff_percentage"]

    # Itterate through rows in table
    player_data = []
    cnt = 0
    for row in rows:
        # In some cases there are rows that are not data
        if len(row.findAll("th")) > 1:
            continue

        player_data.append([])
        for fact in facts:
            val = row.find("td", {"data-stat": fact}).get_text()
            player_data[cnt].append(val)
        cnt += 1

    list_to_file(player_data, header=facts, out_file_name=out_file_name)


def get_game_data(content, out_file_name):
    # Navigate to the name table on the page
    table = content.find("table", {"id": "games"})
    rows = table.findAll("tr")

    # Remove header in table
    rows = rows[1:]

    facts = ["date_game", "visitor_team_name", "home_team_name", "visitor_goals", "home_goals", "overtimes"]

    # Itterate through rows in table
    game_data = []
    cnt = 0
    for row in rows:
        game_data.append([cnt])
        for fact in facts:
            if fact == "date_game":
                tag = "th"
            else:
                tag = "td"
            val = row.find(tag, {"data-stat": fact}).get_text()
            game_data[cnt].append(val)

        cnt += 1

    list_to_file(game_data, out_file_name=out_file_name, header=facts)

def get_standings_data(content, season, out_file_name):
    table = content.find("table", {"id": "standings"})
    rows = table.findAll("tr")
    rows = rows[1:]
    standing_data = []
    for row in rows:
        team = row.find("td", {"data-stat": "team_name"}).get_text()
        record_raw = row.find("td", {"data-stat": "Overall"}).get_text()
        record = record_raw.split('-')
        points = int(record[0])*2 + int(record[2])
        standing_data.append([team, season, points])

    list_to_file(standing_data, out_file_name=out_file_name, header=["team_name", "year", "points"])



def scrape_data(data, season=2018, num_seasons=10):
    data = data.lower()
    if data not in ["skaters", "games", "standings"]:
        raise ValueError("Only able to scrape player and game data, not {}".format(data))

    seasons = [season - i for i in range(num_seasons)]

    for curr_season in seasons:
        if data == "skaters":
            page = requests.get("https://www.hockey-reference.com/leagues/NHL_{}_skaters.html".format(curr_season))
            content = BeautifulSoup(page.content, 'html.parser')

            get_player_data(content, "players/{}.csv".format(curr_season))

        elif data == "games":
            page = requests.get("https://www.hockey-reference.com/leagues/NHL_{}_games.html".format(curr_season))
            content = BeautifulSoup(page.content, 'html.parser')

            get_game_data(content, "games/game_{}.csv".format(curr_season))
        
        else:
            page = requests.get("https://www.hockey-reference.com/leagues/NHL_{}_standings.html".format(curr_season))
            content = BeautifulSoup(page.content, 'html.parser')

            get_standings_data(content, season, "points/{}.csv".format(curr_season))


